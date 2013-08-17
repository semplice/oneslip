#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# oneslip - pywebkitgtk web applications viewer
# Copyright (C) 2013  Giuseppe "GsC_RuL3Z" Corti
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import addapp
import os
import time
import threading

from gi.repository import Gtk, GObject, Gdk

ADDAPP_FE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../frontend/add.glade")

GObject.threads_init()

class addappgui():
	def __init__(self, donotshow=False):
		
		# GUI setup
		self.builder = Gtk.Builder()
		self.builder.add_from_file(ADDAPP_FE)

		# Get objects
		self.main = self.builder.get_object("main")

		# Status
		self.eventbox = self.builder.get_object("eventbox")
		self.box_status = self.builder.get_object("box-status")
		self.image_status = self.builder.get_object("image-status")
		self.label_status = self.builder.get_object("label-status")

		# Window
		self.grid_inputs = self.builder.get_object("grid-inputs")
		self.name_entry = self.builder.get_object("name-entry")
		self.url_entry = self.builder.get_object("url-entry")
		self.width_entry = self.builder.get_object("width-entry")
		self.height_entry = self.builder.get_object("height-entry")
		self.cat_combo = self.builder.get_object("category-combo")

		self.dialog_action_area = self.builder.get_object("dialog-action-area")
		self.btn_save = self.builder.get_object("save-btn")
		self.btn_cancel = self.builder.get_object("cancel-btn")

		# Events
		self.btn_save.connect("clicked", self.save)
		self.btn_cancel.connect("clicked", self.cancel)

		# Show it
		self.setup()

		if not donotshow: self.main.show_all()

		self.eventbox.hide()

		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

	def save(self, opt = None):
		""" Verify the inputs and make the .desktop """

		threading.Thread(target=self.save_thread).start()


	def save_thread(self, opt = None):

		app = addapp.addapp() 

		# Set window sensitive False
		GObject.idle_add(self.grid_inputs.set_sensitive, False)
		GObject.idle_add(self.dialog_action_area.set_sensitive, False)

		# Get inputs
		name = self.name_entry.get_text()
		url = self.url_entry.get_text()
		width = self.width_entry.get_text()
		height = self.height_entry.get_text()
		catree = self.cat_combo.get_active_iter()

		size =width+"x"+height

		if catree != None:
			model = self.cat_combo.get_model()
			cat = model[catree][0]
		else:
			GObject.idle_add(self.status, "inputs")
			GObject.idle_add(self.grid_inputs.set_sensitive, True)
			GObject.idle_add(self.dialog_action_area.set_sensitive, True)

			return False

		if not app.check(name,url,size,3):
			GObject.idle_add(self.status, "inputs")
			GObject.idle_add(self.grid_inputs.set_sensitive, True)
			GObject.idle_add(self.dialog_action_area.set_sensitive, True)

			return False

		GObject.idle_add(self.status, "getfavicon")

		favicon = app.getFavicon(url)

		if favicon == "applications-internet":
			GObject.idle_add(self.status, "errfavicon")
		else:
			GObject.idle_add(self.status, "succfavicon")

		time.sleep(1)
		lst, dic = app.getcat()

		# Get english name for the category
		cateng = dic[cat]

		if app.createdesktop(name,url,size,app.getTruecat(cateng),favicon):
			GObject.idle_add(self.status, "success")
			GObject.idle_add(self.grid_inputs.set_sensitive, True)
			GObject.idle_add(self.dialog_action_area.set_sensitive, True)

		# close oneslip
		time.sleep(1)
		Gtk.main_quit()		

	def cancel(self, opt=None):
		""" cancel """
		self.main.destroy()
		Gtk.main_quit()

	def setup(self):
		""" initialize GUI """

		getcat = addapp.addapp()
		lst, dic = getcat.getcat()
		
		listmodel = Gtk.ListStore(GObject.TYPE_STRING)

		for item in lst:
			listmodel.append((item,))
		#listmodel.append(("Fare soldi spammando",))

		self.cat_combo.set_model(listmodel)
		cell = Gtk.CellRendererText()
		self.cat_combo.pack_start(cell, True)
		self.cat_combo.add_attribute(cell, "text", 0)
		
		self.cat_combo.set_active(0)

	def status(self, type):
		""" Status bar """

		if type=="inputs":
			self.eventbox.show()
			self.eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#F07568"))
			self.image_status.set_from_icon_name("gtk-dialog-error", Gtk.IconSize(6))
			self.label_status.set_text("Error: invalid inputs or server unreachable")

		elif type=="getfavicon":
			self.eventbox.show()
			self.eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#729fcf"))
			self.image_status.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...")

		elif type=="errfavicon":
			self.eventbox.show()
			self.eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#F07568"))
			self.image_status.set_from_icon_name("gtk-dialog-error", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...Failed!")

		elif type=="succfavicon":
			self.eventbox.show()
			self.eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#73d216"))
			self.image_status.set_from_icon_name("gtk-info", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...Success!")

		elif type=="success":
			self.eventbox.show()
			self.eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#73d216"))
			self.image_status.set_from_icon_name("gtk-info", Gtk.IconSize(6))
			self.label_status.set_text("Web application added to your menu!")
