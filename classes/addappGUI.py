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

ADDAPP_FE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "frontend/add.glade")

class addappgui():
	def __init__(self, donotshow=False):
		
		# GUI setup
		self.builder = Gtk.Builder()
		self.builder.add_from_file(ADDAPP_FE)

		# Get objects
		self.main = self.builder.get_object("main")
		self.name_entry = self.builder.get_object("name-entry")
		self.url_entry = self.builder.get_object("url-entry")
		self.width_entry = self.builder.get_object("with-entry")
		self.height_entry = self.builder.get_object("height-entry")
		self.cat_combo = self.builder.get_object("category-combo")
		self.btn_save = self.builder.get_object("save-btn")
		self.btn_cancel = slef.builder.get_object("cancel-btn")

		self.btn_save.connect("clicked", self.save)
		self.btn_cancel.connect("clicked", self.cancel)

		# Show it
		if not donotshow: self.main.show_all()

	def save(self):
		""" call addapp """