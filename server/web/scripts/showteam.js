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


function update_graph() {
    fetch('http://localhost:8080/view/updateAllGraphs').then(function(response) {
    alert("Update Successful");
    }).catch(error => console.error(error));
}

function getMatch() {
	var match = document.getElementById('match').value;
	window.location = "/view/matchplan?match=" + match;
}

function customMatch() {
	out = '/view/customplan'

	out += '?red1=' + document.getElementById('Red1').value;
	out += '&red2=' + document.getElementById('Red2').value;
	out += '&red3=' + document.getElementById('Red3').value;

	out += '&blue1=' + document.getElementById('Blue1').value;
	out += '&blue2=' + document.getElementById('Blue2').value;
	out += '&blue3=' + document.getElementById('Blue3').value;

	window.location = out
}