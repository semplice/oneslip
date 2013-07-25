/*
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
*/

var sys = require('sys')
var exec = require('child_process').exec;
var WebSocketServer = require('ws').Server
, wss = new WebSocketServer({port: 4001});
wss.on('connection', function(ws) {
	ws.on('message', function(message) {
		//console.log('received: %s', message);
		exec("notify-send "+ message, puts);

	});
	ws.send('something');
});

function puts(error, stdout, stderr) { sys.puts(stdout) }

