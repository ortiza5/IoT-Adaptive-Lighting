$(document).ready(function() {

	var socket = io.connect('http://0.0.0.0:5000');

	socket.on('connect', function() {
		socket.send('User has connected!');
	});

	socket.on('mqtt_rec', function(data) {
		$("#log_data").append('<p> Received on: ['+data['topic']+'] Data: '+data['payload']+'</p>');
		console.log(data['payload'])
	});

	socket.on('mqtt_pub', function(data) {
		$("#log_data").append('<p> Published data: '+ data +'</p>');
		console.log(data['payload'])
	});

});