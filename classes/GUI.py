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
import threading
import subprocess

# Debugging
#import pdb
#pdb.set_trace()

COOKIEDIR = os.getenv('HOME') + "/.oneslip/cookies/cookies.txt"
FAVICONDIR = os.getenv('HOME') + "/.oneslip/favicons/"
APPDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./applications")

GObject.threads_init()

class GUI():

	def __init__(self, width, height, url):

		self.window = Gtk.Window()
		#self.window.set_resizable(False)
		self.view = WebKit2.WebView()
		self.policy = WebKit2.NavigationPolicyDecision()

		# Favicon

		icon = self.getIcon(url)

		if not icon: 
			# Set fallback icon
			self.window.set_icon_name("applications-internet")

		else:
			# Set favicon as icon
			self.window.set_icon_from_file(icon)

		# Cookie support
		context = self.view.get_context()
		cookie = context.get_cookie_manager()
		cookie.set_persistent_storage(COOKIEDIR,WebKit2.CookiePersistentStorage.TEXT)
		cookie.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

		self.view.load_uri(url)
		self.url = url
		self.baseurl = url.replace("http://","").replace("file://","").replace("https://","").split("/")[0]
		
		self.window.add(self.view)
		self.view.set_size_request(int(width), int(height))

		self.window.show_all()
		self.view.connect("load-changed", self.load_changed)
		self.view.connect("decide-policy", self.decide_policy)
		self.view.connect("load-failed", self.load_failed)
		
		self.window.connect('delete-event', lambda window, event: Gtk.main_quit())

	def decide_policy(self, decision, test, NavType):
		#if self.policy == self.policy.LINK_CLICKED:
		#if WebKit2.NavigationType.LINK_CLICKED:
		print WebKit2.NavigationPolicyDecision.NavigationType
		print self.policy.get_mouse_button()

	def load_failed(self, view, frame):
		""" if load fail """
		self.window.set_title("Error!")
		self.view.load_uri("file://" + APPDIR + "/messages/errors/error.html")

	def load_changed(self, view, event):
		
		if event == WebKit2.LoadEvent.STARTED:
			urlz = self.view.get_uri()
			baseurlz = urlz.replace("http://","").replace("file://","").replace("https://","").split("/")[0]

			# Check if we are already at the same website
			#if not baseurlz.startswith(self.baseurl):
				# Ensure we do not load the next page

				# Open link in browser
				#browser = subprocess.call(["x-www-browser", urlz])

		if event == WebKit2.LoadEvent.FINISHED:

			title = self.view.get_title()
			if not title:
				title = self.view.get_uri()
			if title:
				# Set web page title as Gtk Window title
				self.window.set_title(title)

	def getIcon(self, url):
		""" Get icon from FAVICONDIR """
		if url[-1:] == "/":
			# Remove last char if it is "/"
			name = url[:-1]
			
		# Remove http:// to url
		if url[:7]=="http://":
			name = url[7:]
		elif url[:8]=="https://":
			name = url[8:]
		else:
			name = url

		name = name.replace('/','.')

		iconstr = FAVICONDIR + name + ".png"

		try:
   			with open(iconstr): pass
		except IOError:
   			return False

   		return iconstr

   	#def thread(self, cmd):
   	#	os.system(cmd)
