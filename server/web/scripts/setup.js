function setEvent() {
					var event = document.getElementById('event').value;
					var year = document.getElementById('year').value;
					window.location = "/eventcurrent?event=" + event + "&year=" + year;
}
function getEvent() {
					var event = document.getElementById('event').value;
					var year = document.getElementById('year').value;
					window.location = "/eventfind?event=" + event + "&year=" + year;
}