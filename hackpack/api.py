
from flask import request, session, jsonify
from app import app
from models import *
from auth import auth
import functools, urllib2
from json import JSONDecoder
from util import get_object_or_404
from wtfpeewee.orm import model_form
import urllib, urllib2
from json import JSONDecoder
import datetime
from trivia import trivia_info

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


HackathonForm = model_form(Hackathon, exclude=("facebook_id", "owner"))

@api_route("create-hackathon", requires_login = True)
def ajax_create_hackathon():
	hack = Hackathon()

	form = HackathonForm(request.form)
	if form.validate():
		form.populate_obj(hack)
		hack.owner = auth.get_logged_in_user()
		data = urllib.urlencode({
				'access_token' : session["fb_token"],
				'name' : hack.title,
				'start_time' : datetime.date.isoformat(hack.start_date),
				'end_time' : datetime.date.isoformat(hack.end_date),
				'description' : hack.description,
				'location' : hack.location})
		print "data is " , data
		req = urllib2.Request("https://graph.facebook.com/"+str(hack.owner.facebook_id)+"/events", data)
		response = urllib2.urlopen(req)
		decoder = JSONDecoder()
		hack.facebook_id = decoder.decode(response.read())["id"]
		"""
		trivia_str = ""
		for question in trivia:
			trivia_str += question + ":" + trivia[question]

		hack.trivia = trivia_str"""

		hack.save()
		return {"hackathon_id": hack.id}

	else:
		for field in form:
			print field.label
			for error in field.errors:
				print error
		return {"status": "error", "error": "DERP"}

@api_route("post-shoutout", requires_login=True)
def ajax_post_shoutout():
	hackathon = get_object_or_404(Hackathon, id = request.form["hackathon_id"])
	so = Shoutout(user = auth.get_logged_in_user(), hackathon = hackathon, message = request.form["message"])
	so.save()

@api_route("updates", requires_login = True)
def ajax_updates():
	shoutouts_after = request.form["shoutouts_after"]
	hackathon = get_object_or_404(Hackathon, id = request.form["hackathon_id"])
	shoutouts = Shoutout.select().where(Shoutout.id > shoutouts_after, Shoutout.hackathon == hackathon).order_by(Shoutout.id)
	out = []
	for so in shoutouts:
		out.append({"message": so.message, "fbid": so.user.facebook_id, "id": so.id})
	last_id = shoutouts_after
	if len(out):
		last_id = out[-1]["id"]
	return {"shoutouts": out, "last_id": last_id}


@api_route("repo-stats", requires_login=True)
def ajax_get_repo_stats():
	repo_address = request.form["repo_address"]
	repo_address = repo_address.replace("https://", "").replace("http://", "").replace("git@github.com:", "").replace("github.com/", "").replace(".git", "")
	repo_owner = repo_address.split("/")[0]
	repo_name = repo_address.split("/")[1]
	req = urllib2.Request("https://api.github.com/repos/"+repo_owner+"/"+repo_name+"/commits?per_page=10000")
	response = urllib2.urlopen(req)
	decoder = JSONDecoder()
	commits = decoder.decode(response.read())
	user_commits = {}
	biggest = 0
	top_committer = ""
	for c in commits:
		committer = c["committer"]
		if committer == None:
			continue
		committer = committer["login"]
		if ( not user_commits.has_key(committer) ):
			user_commits[committer] = 0
		user_commits[committer] = user_commits[committer] + 1
		if ( user_commits[committer] > biggest ):
			top_committer = committer
	return {"commit-number" : len(commits), "top-committer" : top_committer}

@api_route("set-questions", requires_login=True)
def ajax_set_questions():
	hackathon = request.form["hackathon_id"]
	questions = request.form["questions"]

	hackathon = get_object_or_404(Hackathon, id = hackathon)
	hackathon.trivia = questions
	hackathon.save()
