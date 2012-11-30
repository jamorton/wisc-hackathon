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

function loginResponse(response) {
    if (response.status == "connected") {
        $.post("/ajax/login",
               {"token": response.authResponse.accessToken, "fbid": response.authResponse.userID},
               function (data) {
                   window.location = window.REDIRECT_URL;
               });
    }
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '502160453150596', // App ID from the App Dashboard
        channelUrl : '//WWW.YOUR_DOMAIN.COM/channel.html', // Channel File for x-domain communication
        status     : true, // check the login status upon init?
        cookie     : true, // set sessions cookies to allow your server to access the session?
        xfbml      : true  // parse XFBML tags on this page?
    });
};

(function(d, debug){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all" + (debug ? "/debug" : "") + ".js";
    ref.parentNode.insertBefore(js, ref);
}(document, true));
