function setMatch() {
					var match = document.getElementById('match').value;
					window.location = "/matchcurrent?match=" + match;
}
function setEvent() {
					var event = document.getElementById('event').value;
					window.location = "/eventcurrent?event=" + event;
}