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

import network

# Debug
#import pdb
#pdb.set_trace()

COOKIEDIR = os.getenv('HOME') + "/.oneslip/cookies/"
FAVICONDIR = os.getenv('HOME') + "/.oneslip/favicons/"
APPDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./applications")

GObject.threads_init()
net = network.Network()


class GUI():
	def __init__(self, width, height, url):

		self.window = Gtk.Window()
		#self.window.set_resizable(False)
		self.view = WebKit2.WebView()
		#self.policy = WebKit2.NavigationPolicyDecision()
		self.download = WebKit2.Download()

		# Favicon

		icon = self.getIcon(url)

		self.window.set_title("Loading...")

		if not icon: 
			# Set fallback icon
			self.window.set_icon_name("applications-internet")

		else:
			# Set favicon as icon
			self.window.set_icon_from_file(icon)

		# Cookie support
		cookie_file = self.getCookie(url)

		context = self.view.get_context()
		cookie = context.get_cookie_manager()
		cookie.set_persistent_storage(cookie_file,WebKit2.CookiePersistentStorage.TEXT)
		cookie.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

		# Downloads support
		#self.download.set_destination("~/Downloads/") # To be fixed

		self.view.load_uri(url)
		self.url = url
		self.baseurl = url.replace("http://","").replace("file://","").replace("https://","").split("/")[0]
		
		self.window.add(self.view)
		self.view.set_size_request(int(width), int(height))

		self.window.show_all()
		self.view.connect("load-changed", self.load_changed)
		self.view.connect("decide-policy", self.decide_policy)
		self.view.connect("load-failed", self.load_failed)

		
		self.window.connect('destroy', Gtk.main_quit)

	def decide_policy(self, view, decision, decision_type):
		""" Fired when something happened (e.g. a link has been clicked) """
				
		if (decision.__info__ == WebKit2.NavigationPolicyDecision.__info__ and decision.get_navigation_type() == WebKit2.NavigationType.LINK_CLICKED) and (
			decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION):
			urlz = decision.get_request().get_uri()
			baseurlz = urlz.replace("http://","").replace("file://","").replace("https://","").split("/")[0]

			# Check if we are already at the same website
			if not baseurlz.startswith(self.baseurl):
				# Open link in browser
				browser = subprocess.Popen(["x-www-browser", urlz])
				
				# Do not even try to load the page
				decision.ignore()

	def load_failed(self, view, frame):
		""" if load fail """
		self.window.set_title("Error!")
		self.view.load_uri("file://" + APPDIR + "/messages/errors/error.html")

	def load_changed(self, view, event):
		
		if event == WebKit2.LoadEvent.STARTED:
			title = self.view.get_title()
			if not title:
				title = "Loading..."
			else:
				title = title + " (Loading...)"
			
			self.window.set_title(title)
		
		elif event == WebKit2.LoadEvent.FINISHED:

			title = self.view.get_title()
			if not title:
				title = self.view.get_uri()

			self.window.set_title(title)
			
	def getIcon(self, url):
		""" Get icon from FAVICONDIR """
		name = url
		if url[-1:] == "/":
			# Remove last char if it is "/"
			name = url[:-1]
			
		name = net.remove_protocol(name)
		name = name.replace('/','.')
		iconstr = FAVICONDIR + name + ".png"

		try:
   			with open(iconstr): pass
		except IOError:
   			return False

   		return iconstr

   	def getCookie(self, url):
   		""" Get cookie from COOKIEDIR """
   		name = url

   		if url[-1:] == "/":
			# Remove last char if it is "/"
			name = url[:-1]
			
		name = net.remove_protocol(name)
		name = name.replace('/','.')
		cookiestr = COOKIEDIR + name

		try:
   			with open(cookiestr): pass
		except IOError:
   			open(cookiestr,'w')

   		return cookiestr
