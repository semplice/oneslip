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

import os
import gmenu
import string
import  urllib2
import time

import t3rdparty.Win32IconImagePlugin

from gi.repository import Gtk, GObject
from BeautifulSoup import BeautifulSoup 
from PIL import Image

DESKTOPDIR = os.getenv("HOME") + "/.local/share/applications"
FAVICONDIR = os.getenv("HOME") + "/.oneslip/favicons/"
ADDAPP_FE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../frontend/add.glade")

class addapp:

	def getFavicon(self,url):
		""" Try to get favicon from website """

		if url[-1:] == "/":
			# Remove last char if it is "/"
			url = url[:-1]
			#print url

		# Add http:// to url
		if url[:7]=="http://":
			name = url[7:]
		elif url[:8]=="https://":
			name = url[8:]
		else:
			name = url
			url = "http://" + url
		#print url

		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read())

		if soup.find("link", rel="shortcut icon"):
			# Generic favicon
			icon_link = soup.find("link", rel="shortcut icon")

		elif soup.find("link", rel="icon"):
			# Some website like github use rel="icon"
			icon_link = soup.find("link", rel="icon")

		else:
			if urllib2.urlopen(url + "/favicon.ico"):
				# Try to find favicon
				icon_link = {}
				icon_link['href'] = url + "/favicon.ico"
			else:
				# fallback icon 
				return "applications-internet"

		#print icon_link

		if icon_link['href'][:2]=="//": # URL Fix
			icon_link['href']="http:"+icon_link['href']

		elif icon_link['href'][:1]=="/": # <link rel="icon" type="image/x-icon" href="/icon.ico">
			icon_link['href']=url+icon_link['href']

		#print icon_link['href']

		icon = urllib2.urlopen(icon_link['href'])
		icostr = "/tmp/" + name + ".ico"
		pngstr = FAVICONDIR + name + ".png"
		with open(icostr, "wb") as f:
			f.write(icon.read())

		# Convert favicon to png
		img = Image.open(icostr)
		img.convert('RGBA')
		img.save(pngstr)

		return pngstr

	def getcat(self):
		""" Return a dictionary with the applications categories available """

		lst =[]
		dic ={}
		contents = gmenu.lookup_tree("semplice-applications.menu", gmenu.FLAGS_SHOW_EMPTY|gmenu.FLAGS_INCLUDE_EXCLUDED|gmenu.FLAGS_INCLUDE_NODISPLAY).get_root_directory().get_contents()

		for itm in contents:
			dic[itm.name] = itm.menu_id
			lst.append(itm.name)

		return lst,dic;

	def getTruecat(self, cat):
		""" Return a dictionary with all name of applications categories"""

		dic = {"Accessories":"Application;Utility;",
		"Multimedia":"Application;AudioVideo;",
		"Games":"Application;Game;",
		"Graphics":"Application;Graphics;",
		"Internet":"Application;Network;",
		"Development":"Application;Development;",
		"System":"Application;System;",
		"Office":"Application;Office;",
		"Education":"Application;Education;",
		"Science":"Application;Science",
		"Universal Access":"Application;Accessibility;",
		"Other":"Application;Other;"
		}

		return dic[cat]

	def check(self, name, url, size, cat):
		""" check user input """

		name.replace(" ", "")

		if name == "":
			return False

		if url[:7]!="http://":
			url = "http://" + url

		# decode size
		sized = string.split(size,'x')

		if len(sized)!=2:
			return False

		if int(sized[0])<0 and int(sized[1])<0:
			return False

		if int(cat)<0 and int(cat)>11:
			return False

		return True

	def createdesktop(self, name, url, size, cat, icon):
		""" Create a .desktop in DESKTOPDIR """

		with open(os.path.join(DESKTOPDIR, "oneslip-" + name +".desktop"), "w") as target:

			execute = "oneslip " + url + " " + size

			target.write("""[Desktop Entry]
Version=1.0
Name=%(name)s
Exec=%(exec)s
Terminal=false
Type=Application
Icon=%(icon)s
Categories=%(cat)s""" % {"name":name, "exec":execute, "cat":cat, "icon":icon})

		return True

class addappgui():
	def __init__(self, donotshow=False):
		
		# GUI setup
		self.builder = Gtk.Builder()
		self.builder.add_from_file(ADDAPP_FE)

		# Get objects
		self.main = self.builder.get_object("main")

		# Status
		self.box_status = self.builder.get_object("box-status")
		self.image_status = self.builder.get_object("image-status")
		self.label_status = self.builder.get_object("label-status")

		# Window
		self.name_entry = self.builder.get_object("name-entry")
		self.url_entry = self.builder.get_object("url-entry")
		self.width_entry = self.builder.get_object("width-entry")
		self.height_entry = self.builder.get_object("height-entry")
		self.cat_combo = self.builder.get_object("category-combo")
		self.btn_save = self.builder.get_object("save-btn")
		self.btn_cancel = self.builder.get_object("cancel-btn")

		# Events
		self.btn_save.connect("clicked", self.save)
		self.btn_cancel.connect("clicked", self.cancel)

		# Show it
		self.setup()

		if not donotshow: self.main.show_all()

		self.box_status.hide()

		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

	def save(self, opt = None):
		""" Verify the inputs and make the .desktop """

		app = addapp() 

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
			self.status("inputs")
			return False

		if not app.check(name,url,size,3):
			self.status("inputs")
			return False

		self.status("getfavicon")

		time.sleep(1)
		favicon = app.getFavicon(url)

		if favicon == "applications-internet":
			self.status("errfavicon")
		else:
			self.status("succfavicon")

		lst, dic = app.getcat()

		# Get english name for the category
		cateng = dic[cat]

		if app.createdesktop(name,url,size,app.getTruecat(cateng),favicon):
			self.status("success")		

	def cancel(self):
		""" cancel """

	def setup(self):
		""" initialize GUI """

		getcat = addapp()
		lst, dic = getcat.getcat()
		
		listmodel = Gtk.ListStore(GObject.TYPE_STRING)

		for item in lst:
			listmodel.append((item,))

		self.cat_combo.set_model(listmodel)
		cell = Gtk.CellRendererText()
		self.cat_combo.pack_start(cell, True)
		self.cat_combo.add_attribute(cell, "text", 0)

	def status(self, type):
		""" Status bar """

		if type=="inputs":
			self.box_status.show()
			self.image_status.set_from_icon_name("gtk-dialog-error", Gtk.IconSize(6))
			self.label_status.set_text("Error: invalid inputs")

		if type=="getfavicon":
			self.box_status.show()
			self.image_status.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...")

		if type=="errfavicon":
			self.box_status.show()
			self.image_status.set_from_icon_name("gtk-dialog-error", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...Failed!")

		if type=="succfavicon":
			self.box_status.show()
			self.image_status.set_from_icon_name("gtk-info", Gtk.IconSize(6))
			self.label_status.set_text("Trying to get favicon...Success!")

		if type=="success":
			self.box_status.show()
			self.image_status.set_from_icon_name("gtk-info", Gtk.IconSize(6))
			self.label_status.set_text("Web application added to your menu!")




