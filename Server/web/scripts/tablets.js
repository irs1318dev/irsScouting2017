var request = new XMLHttpRequest();
request.onreadystatechange = processData;

loadTablets();
setInterval(loadTablets, 5000);

function loadTablets() {	
	request.open('GET', "/tablets", true)
	request.send();
}

function processData(e) {
	if(request.readyState == 4 && request.status == 200) { 
		document.getElementById('tablets').innerHTML = request.responseText;
		
		var match = request.split('"')[1];
		document.body.innerHTML = document.body.innerHTML.replace('{Match}', match);
	}
}

function setMatch() {
	var match = document.getElementById('match').value;
	window.location = "/matchcurrent?match=" + match;
}