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

from gi.repository import Gtk, GObject

import classes.addappGUI
import classes.addapp

import os
import sys
import gmenu

if __name__ == "__main__":

	if sys.argv < 1:
		sys.exit("Usage: %s [cli|gtk]" % sys.argv[0])

	if sys.argv[1]=="cli":
		# CLI interface

		name = raw_input("Name: ")
		url = raw_input("URL: ")
		size = raw_input("size (NxN): ")

		print "Select a category: \n"

		addapp = classes.addapp.addapp()
		lst, dic = addapp.getcat()

		for i in range(0,len(lst)):
			print str(i) + ") " + lst[i]
			#print dic[lst[i]]

		cat = raw_input("your choice: ")

		categ = dic[lst[int(cat)]]

		if(addapp.createdesktop(name,url,size,dic[lst[i]])):
			print "Web application added to your desktop"

	if sys.argv[1]=="gtk":
		# GTK interface 

		g = classes.addappgui()
		Gtk.main()