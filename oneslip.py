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

import classes.oneslip
import classes.network
import classes.lib

import sys
import string
import os
import subprocess

APPDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./applications")

net = classes.network.Network()

GObject.threads_init()


if __name__ == "__main__":

	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	if len(sys.argv) < 3:
		sys.exit("Usage: %s (URL) (width)x(height) <Initial Title>" % sys.argv[0])

	# decode size
	size = string.split(sys.argv[2],'x')
	# decode protocol
	protocol = sys.argv[1][:4]
	# get intial title
	if len(sys.argv) > 3:
		title = " ".join(sys.argv[3:])
	else:
		title = None

	# Verify size
	if size[0].isdigit() == False or size[1].isdigit() == False:
		sys.exit("%s isn't a valid size" % sys.argv[2])

	nodelib = False # Set nodelib False  (There aren't nodejs processes)

	# Check protocol
	if protocol == "file":
		# Check if file exist
		if os.path.exists(sys.argv[1][7:])==False:
			sys.argv[1] = "file://" + APPDIR + "/messages/errors/nofile.html" # Web application not found

		# NodeJS test
		else:
			# Check and execute libs
			 lib = classes.lib.lib()
			 pidlist = lib.load(sys.argv[1])
			 nodelib = True # Set nodelib True (there are nodejs processes)


	g = classes.oneslip.GUI(size[0],size[1],sys.argv[1],title=title)
	Gtk.main()

	if nodelib:
		# kill nodejs
		for pid in pidlist:
			#print pidlist[0]
			os.system("kill -9 "+str(pid))
