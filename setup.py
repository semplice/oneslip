#!/usr/bin/env python
# pylaivng setup (using distutils)
# Copyright (C) 2013 Eugenio "g7" Paolantonio. All rights reserved.
# Work released under the GNU GPL license, version 3.

from distutils.core import setup
import glob, os
import commands

tree = []
current_dir = commands.getoutput("pwd")

def generate_tree(directory, where):
	""" Generates a directory tree to be used with data_files.
	SYNTAX: generate_tree(directory, where)
	directory = directory to 'tree-ize'
	where = location to install the tree
	
	Examples:
	generate_tree("data","/var/www/pylaivng") - will generate a tree that will copy data/ directory in /var/www/pylaivng
	generate_tree("config/distributions", "/etc/pylaivng") - will generate a tree that will copy config/distributions in /etc/pylaivng/distributions """
	
	# Enter in the directory before the one that we should make the tree...
	if os.path.dirname(directory): os.chdir(os.path.dirname(directory))
	
	for root, dirs, files in os.walk(os.path.basename(directory)):
		filelist = []
		# adjust root
		if os.path.dirname(directory):
			root_real = os.path.join(os.path.dirname(directory), root)
		else:
			root_real = root

		if files:
			for filename in files:
				filelist.append(os.path.join(root_real, filename))
			if filelist:
				tree.append((os.path.join(where, root), filelist))
	
	# Return into current_dir
	os.chdir(current_dir)

# Generate data_files tree :)
generate_tree("frontend", "/usr/share/oneslip")
generate_tree("applications", "/usr/share/oneslip")
generate_tree("lib", "/usr/share/oneslip")

setup(name='oneslip',
	version='1.0.0',
	description='Debian-based distributions development utilities',
	author='Giuseppe Corti and the Semplice Team',
	author_email='giuseppe@infiniteloop.pro',
	url='http://github.com/semplice/oneslip',
	scripts=['oneslip.py', 'oneslip-add-app.py'],
	packages=[
		"t3rdparty",
		"classes"
	],
	data_files=tree,
	requires=['gi.repository.Gtk', 'gi.repository.GObject', 'gi.repository.Gdk', 'git.repository.WebKit2', 'os', 'sys', 'urllib2', 'string', 'subprocess', 'ConfigParser', 'gmenu', 'BeautifulSoup', 'PIL', 'threading' ],
)
