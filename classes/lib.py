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

import string
import subprocess
import os

LIBDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../lib/")

class lib():
	""" Local web applications lib engine """
	def __init__(self, location):
		location = location.replace("file://","").replace("index.html","").replace("index.htm","")
		
		try:
			with open(location + ".oneslip"): pass
			libtoexec = self.readConf(location + ".oneslip")

			for lib in libtoexec:
				self.execLib(lib)

		except IOError:
			""" Do nothing :) """

	def readConf(self, location):
		""" Read .oneslip file """
		libs=[]
		for line in open(location):
			if line.startswith("exec"): # exec "notify"
				line = line.replace("exec","").replace("\"","").replace(" ","")
				libs.append(line)
		return libs

	def execLib(self,lib):
		""" run nodejs lib """
		subprocess.Popen(["node", LIBDIR+lib+".js"])

