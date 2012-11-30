
from flask import request, session, jsonify
from app import app
from models import *
from auth import auth
import functools, urllib2
from json import JSONDecoder
from util import get_object_or_404

def api_route(action, **options):
	requires_login = options.get("requires_login", False)
	def decorator(fn):
		@functools.wraps(fn)
		def wrapper(*args, **kwargs):
			if requires_login and not auth.get_logged_in_user():
				return jsonify({"error": "login_required", "status": "error"})
			ret = fn(*args, **kwargs)
			obj = {"status": "success"}
			if ret:
				obj.update(ret)
			return jsonify(obj)
		return app.route("/ajax/" + action, methods=["POST"])(wrapper)
	return decorator


@api_route("login")
def ajax_login():
	fbid = request.form["fbid"]
	user = User.get_or_create(fbid)
	auth.login_user(user)
	session["fb_token"] = request.form["token"]

@api_route("attendees", requires_login=True)
def ajax_get_event_attendees():
	hackathon = get_object_or_404(Hackathon, id = request.form["hackathon_id"])
	req = urllib2.Request("https://graph.facebook.com/"+str(hackathon.facebook_id)+"/attending?access_token="+session["fb_token"])
	print "https://graph.facebook.com/"+str(hackathon.facebook_id)+"/attending?access_token="+session["fb_token"]
	response = urllib2.urlopen(req)
	decoder = JSONDecoder()
	attending = decoder.decode(response.read())["data"]
	return {"attending": attending}

#@api_route("create-hackathon", requires
