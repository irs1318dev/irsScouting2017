function setEvent() {
					var event = document.getElementById('event').value;
					window.location = "/eventcurrent?event=" + event;
}
function getEvent() {
					var event = document.getElementById('event').value;
					window.location = "/eventfind?event=" + event;
}