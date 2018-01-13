function showTeam() {
					var team = document.getElementById('team').value;
					window.location = "/view/teamplan?team=" + team;
}

var request = new XMLHttpRequest();

function loadTeam() {
	var team = document.getElementById('team').value;
	
	request.open('GET', "/view/teamplan?team=" + team, true)
	request.send();
	
	request.onreadystatechange = processData;
	document.getElementById('matches').innerHTML = "Loading";
}

function processData(e) {
	if(request.readyState == 4 && request.status == 200) {
		document.getElementById('matches').innerHTML = request.responseText;
	}
}