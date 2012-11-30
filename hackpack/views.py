
from app import app
from models import *
from flask import render_template, request, url_for, redirect, session
from auth import auth
from wtfpeewee.orm import model_form
from util import get_object_or_404
import datetime, urllib, urllib2
from datetime import date

@app.route("/")
@auth.login_required
def index():

	hackathon_q = Hackathon.select()
	
	hackathons = []
	for h in hackathon_q:

		end_date = "NONE"
		if ( h.end_date != "" ):
			end_date = h.end_date
		location = "NONE"
		if ( h.location != "" ):
			location = h.location

		hackathons.append({
			'title' : h.title,
			'description' : h.description,
			'start_time' : h.start_date,
			'end_time' : end_date,
			'location' : location
			})

	return render_template("index.html", hackathons = hackathons)

@app.route("/hackathon/<int:hackathon_id>")
def dash(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)
	now = datetime.datetime.now()

	if now < hackathon.start_date:
		return render_template("dash-future.html", hackathon = hackathon)
	elif now < hackathon.end_date:
		return render_template("dash-present.html", hackathon = hackathon)
	else:
		return render_template("dash-past.html", hackathon = hackathon)

HackathonForm = model_form(Hackathon, exclude=("facebook_id", "owner"))

@app.route("/hackathon/create", methods=["GET", "POST"])
@auth.login_required
def hackathon_create():
	hack = Hackathon()

	if request.method == "POST":
		form = HackathonForm(request.form)
		if form.validate():
			form.populate_obj(hack)
			hack.owner = auth.get_logged_in_user()
			data = urllib.urlencode({
				'access_token' : session["fb_token"],
				'name' : hack.title,
				'start_time' : date.isoformat(hack.start_date),
				'end_time' : date.isoformat(hack.end_date),
				'description' : hack.description,
				'location' : hack.location})
			req = urllib2.Request("https://graph.facebook.com/"+str(hack.owner.facebook_id)+"/events", data)
			response = urllib2.urlopen(req)
			event_id = response.read()
			event_id = event_id.replace("{\"id\":\"", "")
			event_id = event_id.replace("\"}", "")
			hack.facebook_id = int(event_id)
			hack.save()
			return redirect(url_for("dash", hackathon_id = hack.id))
	else:
		form = HackathonForm()

	return render_template("hackathon-create.html", form = form)


"""
	if request.method == "POST":
		form = HackathonForm(request.form)
		if form.validate():
			form.save()

	else:
		form = HackathForm()

	return render_template("dash_index", form = form)
"""
