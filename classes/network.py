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

import urllib2

class Network():

	def internet_on(self, url):
		""" Check if server is reachable """
		try:
			response=urllib2.urlopen(url,timeout=1)
			return True
		except urllib2.URLError as err: pass
		return False

	def check_protocol(self, url):
		""" Check if user is using http://, https:// or file:// """
		if (url[:7]!="http://") and (url[:7]!="file://") and (url[:8]!="https://"):
			return False
		return True

	def remove_protocol(self, url):
		""" Remove protocol from string """
		name = url.replace("http://","").replace("file://","").replace("https://","")

		return name 
