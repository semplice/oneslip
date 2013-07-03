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

#DESKTOPDIR = os.getenv("HOME") + "/.local/share/applications"
DESKTOPDIR = os.getenv("HOME")
class addapp:

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


	def createdesktop(self, name, url, size, cat):
		""" Create a .desktop in DESKTOPDIR """

		with open(os.path.join(DESKTOPDIR, name +".desktop"), "a") as target:

			execute = "oneslip " + url + " " + size

			target.write("""[Desktop Entry]
Version=1.0
Name=%(name)s
Exec=%(exec)s
Terminal=false
Type=Application
Categories=%(cat)s""" % {"name":name, "exec":execute, "cat":cat})

		return true