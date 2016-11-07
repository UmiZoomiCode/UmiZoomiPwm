var net = require('net');

var client = net.connect({port: 9999}, () => {
	interval = setInterval(()=>{
		randomNumber = ((Math.random() * 2) + 1).toFixed(2)
		console.log(randomNumber);

		client.write(JSON.stringify({
			msg: "ChangeSpeed",
			speed: randomNumber
		}) + "\r\n");
	},4000)
});

client.on('data', (data) => {
	console.log(data.toString());
});

client.on('close', () => {
	console.log("disconnected");
});