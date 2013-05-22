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

#import gi
#gi.require_version('Gtk', '3.0')
#gi.require_version('WebKit', '3.0')

from gi.repository import Soup, WebKit2, Gtk

import sys
import string
import os
COOKIEDIR = os.getenv('HOME') + "/.cookie/cookies.txt"

class GUI():
	def __init__(self, donotshow=False):

		self.window = Gtk.Window()
		#self.window.set_resizable(False)
		self.view = WebKit2.WebView()
		self.cookie = WebKit2.CookieManager()

		# Cookie support
		#self.cookie.set_persistent_storage(COOKIEDIR,)
		#cookiejar = Soup.CookieJarText.new(COOKIEDIR,False)
		#cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
		#session = WebKit2.get_default_session()
		#session.add_feature(cookiejar)

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
	if len(sys.argv) < 2:
		sys.exit("Usage: %s (URL) (width)x(height)" % sys.argv[0])

	size = string.split(sys.argv[2],'x')

	if size[0].isdigit() == False or size[1].isdigit() == False:
		sys.exit("%s isn't a valid size" % sys.argv[2])

	g = GUI()
	Gtk.main()