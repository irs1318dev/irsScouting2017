var request = new XMLHttpRequest();
request.onreadystatechange = processData;

function createMatch() {	
	var match = document.getElementById('match').value;
	var data = "/matchcreate?match=" + match;

	data += "&red1=" + document.getElementById('red1').value;
	data += "&red2=" + document.getElementById('red2').value;
	data += "&red3=" + document.getElementById('red3').value;

	data += "&blue1=" + document.getElementById('blue1').value;
	data += "&blue2=" + document.getElementById('blue2').value;
	data += "&blue3=" + document.getElementById('blue3').value;

	request.open('GET', data, true);
	request.send();
}

function processData(e) {
	if(request.readyState == 4 && request.status == 200) { 

	}
}

function nextMatch() {
	var match = document.getElementById('match').value;
	window.location = "/matchenter?match=" + match;
}