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
var faces;
var names;
var raffleInterval;

function finishRaffle(){
		$("#winner").html(names[0][0]+"<BR /><br /><img src='"+names[0][1]+"' width='400' height='400'></img>");
		$('.face').hide();
}

function runRaffle(){
	if (faces.length!=1){
		var total = Math.floor(faces.length/2);
		for (var j = total;j>0;j--){
		 var i = Math.floor((faces.length)*Math.random());
		$(faces[i]).fadeOut(2000,function(){});
		console.log("chose:"+i+" length:"+faces.length);
		 faces.splice(i,1);
		 names.splice(i,1);
		}
	} else {
		finishRaffle();
	}
}

function setupRaffle(hid) {
    var people = [];
    $.post("/ajax/attendees", {"hackathon_id": hid}, function (data) {
        for (var i = 0; i < data.attending.length; i++) {
            var person = data.attending[i];
            var p = {
                name: person.name,
                picture: "http://graph.facebook.com/" + String(person.id) + "/picture?type=large"
            };
            people.push(p);
        }
        console.log(people);
	    $("#faces").empty();
	    $("#winner").empty();
	    clearInterval(raffleInterval);
	    faces = new Array();
	    names = new Array();
	    var i = 0;
	    var x = Math.floor(Math.sqrt(500*1000/people.length));
	    x-=2;//for padding
	    $.each(people, function() {
		    console.log("test");
		    $("#faces").append("<div class='pull-left' style='margin:1px; width:"+x+"px; height:"+x+"px;'><div class='face' id='face"+i+"'><img src='"+this.picture+"' style='width: "+x+"px; height: "+x+"px;' /></div></div></div>");
		    names[i] = [this.name,this.picture];
		    faces[i] = $("#face"+i);
		    i++;
        });
	    raffleInterval = setInterval('runRaffle()', 2000);
    });
}

function fbLogin() {
    $("#login-button").click(function() {
        FB.login(loginResponse, {scope: "create_event"});
    });
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

$(function () {
    $("#create-hackathon-form").submit(function() {
        $.post("/ajax/create-hackathon", $(this).serialize(), function(data) {

        });
    });
});
