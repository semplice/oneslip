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
from BeautifulSoup import BeautifulSoup 
from PIL import Image

#DESKTOPDIR = "/usr/share/applications"
DESKTOPDIR = os.getenv("HOME") + "/.local/share/applications"
#DESKTOPDIR = os.getenv("HOME")
FAVICONDIR = os.getenv("HOME") + "/.oneslip/favicons/"


class addapp:

	def getFavicon(self,url):
		""" Try to get favicon from website """

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