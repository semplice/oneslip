function notify(message)
{
	socket= new WebSocket('ws://localhost:4001');
	socket.onopen= function() {
    	socket.send('notify '+message);
	}

}
function network(command)
{
	socket= new WebSocket('ws://localhost:4001');
	socket.onopen= function() {
		socket.send('network '+command);
	}
	socket.onmessage=function (evt) 
	{ 
		alert(evt.data);
	}
}
function mixer(command)
{
	socket= new WebSocket('ws://localhost:4001');
	socket.onopen= function() {
		socket.send('mixer '+command);
	}

}
