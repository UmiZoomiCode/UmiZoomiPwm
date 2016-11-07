var buttonHandler = (function(){
	var socket = new WebSocket("ws://localhost:8000");

    socket.onopen = function(){
        console.log('connnected to server');
    }

	socket.onmessage = function(msg){
		console.log(msg);
	}

	socket.onclose = function(){
		console.log('socket closed');
	}

	return function(type){
		switch (type) {
			case 'get':
				socket.send('getProfile');
				break;
			case 'change':
				socket.send('changeProfile');
				break;
			case 'save':
				socket.send('saveProfile');
				break;
			case 'control':
				socket.send('control');
				break;
			case 'ChangeSpeed':
				socket.send(JSON.stringify({
					msg: "ChangeSpeed",
					speed: getSliderValue()
				}));
				break;
			case 'Stop':
				document.getElementById('slider1').value=0;
				socket.send({
					msg: "ChangeSpeed",
					speed: 0
				});
				break;
			default:
				break;
		}
	}
})();

function getSliderValue(){
	var value = document.getElementById('slider1').value;
	if(value==0) return 0;
	value = (value * 10)
	return value;
}
