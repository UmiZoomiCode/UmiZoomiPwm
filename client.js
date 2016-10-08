var net = require('net');
var client = net.connect({port: 9999}, () => {
	client.write('Hello World\r\n');
});

client.on('data', (data) => {
	console.log(data.toString());
	//client.end();
});

client.on('end', () => {
	console.log("disconnected");
});