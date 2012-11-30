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
		$("#winner").html(names[0][0]+" Wins!<BR /><br /><img src='"+names[0][1]+"' width='400' height='400'></img>");
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
        FB.login(loginResponse, {scope: "create_event user_photos"});
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
            if (data.error) {
                $("#ch-error").text("Invalid form data");
                $("#ch-error").show();
            } else {
                window.location = "/hackathon/" + String(data.hackathon_id);
            }
        });
        return false;
    });
});

function autocomplete(hackathons,urls){
        $( "#search" ).autocomplete({
            source: hackathonTitle,
   			 select: function( event, ui ) {
				 		var str = (ui.item.value);
						for (var i = 0; i<hackathonTitle.length; i++){
							if (hackathonTitle[i] == str){
								window.location = urls[i];
							}
						}
				}
        });
}
function tick(){
	seconds--;
	console.log(seconds);
	var secondstext = seconds%60+"";
	if (secondstext.length == 1){
		secondstext = "0" + secondstext;
	}
	$('#timer').html(Math.floor(seconds/60)+":"+secondstext);
	if (seconds == 0){
		alert("Time's up!");
		resetTimer();
	}
}
var going = false;
var seconds;
var timerinterval;
var defaultseconds = 120;
function countdown(){
	seconds = defaultseconds;
	if (!going){
		$("#countdownbutton").html("Reset Countdown");
		going = true;
		timerinterval = setInterval(tick,1000);
	} else {
		resetTimer();
	}
}
function resetTimer(){
		going = false;
		clearInterval(timerinterval);
		seconds = defaultseconds + 1;
		tick();
		$("#countdownbutton").html("Start Countdown");
}

var lastId = "-1";
function checkUpdates(hid) {

    $.post("/ajax/updates", {"hackathon_id": hid, "shoutouts_after": lastId}, function (data) {
        for (var i = 0; i < data.shoutouts.length; i++) {
            var so = data.shoutouts[i];
            var html = '<div class="shoutout"><img style="width: 40px; height: 40px;" src="https://graph.facebook.com/'+so.fbid+'/picture" /> <b><fb:name uid="'+so.fbid+'" capitalize="true" />:</b> ' + so.message + '</div>';
            $("#shoutout-area").prepend(html);
        }
        FB.XFBML.parse(document.getElementById("shoutout-area"));
        lastId = data.last_id;
    });
}

function shoutouts(hid) {
    $("#shoutout-form").submit(function() {
        var message = $("#shoutout-form input").val();
        $("#shoutout-form input").val("");
        $.post("/ajax/post-shoutout", {"hackathon_id": hid, "message": message}, function (data) {

        });
        return false;
    });
    setInterval("checkUpdates("+hid+")", 2000);
}
