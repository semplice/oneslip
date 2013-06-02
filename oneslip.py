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

import sys
import string
import os
import urllib2

COOKIEDIR = os.getenv('HOME') + "/.cookie/cookies.txt"
APPDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./applications")

class GUI():
	def __init__(self, donotshow=False):

		self.window = Gtk.Window()
		#self.window.set_resizable(False)
		self.view = WebKit2.WebView()

		# Cookie support
		context = self.view.get_context()
		cookie = context.get_cookie_manager()
		cookie.set_persistent_storage(COOKIEDIR,WebKit2.CookiePersistentStorage.TEXT)
		cookie.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

		self.view.load_uri(sys.argv[1])
		
		self.window.add(self.view)
		self.view.set_size_request(int(size[0]), int(size[1]))

		self.window.show_all()
		self.view.connect("load-changed", self.load_finished)
		self.view.connect("load-failed", self.load_failed)
		
		self.window.connect('delete-event', lambda window, event: Gtk.main_quit())


	def load_failed(self, view, frame):
		self.window.set_title("Error!")
		#self.view.load.uri()

	def load_finished(self, view, frame):
		title = self.view.get_title()
		if not title:
			title = self.view.get_uri()
		if title:
			# Set web page title as Gtk Window title
			self.window.set_title(title)

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

	g = GUI()
	Gtk.main()
