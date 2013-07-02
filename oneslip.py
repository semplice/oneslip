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

from gi.repository import WebKit2, Gtk, GObject

import classes.GUI

import sys
import string
import os
import urllib2

APPDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./applications")

if __name__ == "__main__":

	def internet_on(page):
		try:
			response=urllib2.urlopen(page,timeout=1)
			return True
		except urllib2.URLError as err: pass
		return False

	if len(sys.argv) < 3:
		sys.exit("Usage: %s (URL) (width)x(height)" % sys.argv[0])

	# decode size
	size = string.split(sys.argv[2],'x')
	# decode protocol
	protocol = sys.argv[1][:4] 

	# Verify size
	if size[0].isdigit() == False or size[1].isdigit() == False:
		sys.exit("%s isn't a valid size" % sys.argv[2])

	# check protocol
	if protocol == "file":
		# Check if file exist
		if os.path.exists(sys.argv[1][7:])==False:
			sys.argv[1] = "file://" + APPDIR + "/messages/errors/nofile.html" # Web application not found

	else:
		# Check if server is reachable
		if internet_on(sys.argv[1])==False:
			#print "no connection"
			sys.argv[1] = "file://" + APPDIR + "/messages/errors/noconnection.html" # No network connection

	g = classes.GUI.GUI(size[0],size[1],sys.argv[1])
	Gtk.main()
