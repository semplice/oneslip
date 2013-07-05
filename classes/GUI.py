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

COOKIEDIR = os.getenv('HOME') + "/.oneslip/cookies/cookies.txt"

class GUI():

	def __init__(self, width, height, url):

		self.window = Gtk.Window()
		#self.window.set_resizable(False)
		self.view = WebKit2.WebView()

		# Cookie support
		context = self.view.get_context()
		cookie = context.get_cookie_manager()
		cookie.set_persistent_storage(COOKIEDIR,WebKit2.CookiePersistentStorage.TEXT)
		cookie.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

		self.view.load_uri(url)
		
		self.window.add(self.view)
		self.view.set_size_request(int(width), int(height))

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