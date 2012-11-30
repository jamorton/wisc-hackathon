
/* script */
var timeout;
function clock(seconds) {
	var secondsleft = seconds;
	now = new Date;
	end = new Date(now.getTime()+parseInt(seconds)*1000); 
	timeout = setInterval('updateClock()', 100);
}
var now;
var end;
function updateClock(){
	now = new Date;
	var seconds = (Math.abs(end - now)/1000);
	seconds = Math.round(seconds);
	
	var output = Math.floor(seconds/3600) + " hrs " + Math.floor(seconds/60)%60 + " min " + (seconds % 60) + " sec";
	$("#clock").text(output);
	
	if (seconds == 0){
		alert("The hackathon is over!");
		clearInterval(timeout);
	}
}