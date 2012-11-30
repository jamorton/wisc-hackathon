
from app import app
from models import *
from flask import render_template, request, url_for, redirect, session, flash
from auth import auth
from wtfpeewee.orm import model_form
from util import get_object_or_404
import datetime
import urllib, urllib2
from json import JSONDecoder


@app.route("/")
@auth.login_required
def index():
	hackathon_q = Hackathon.select()

	hackathons_now = []
	hackathons_future = []
	now = datetime.datetime.now()
	for h in hackathon_q:

		hd = {
			'title' : h.title,
			'description' : h.description,
			'start_time' : h.start_date,
			'end_time' : end_date,
			'location' : location
		}

		if now < h.start_date:
			hackathons_future.append(hd)
		elif now < h.end_date:
			hackathons_now.append(hd)

	return render_template("index.html",
						   hackathons_now = hackathons_now,
						   hackathons_future = hackathons_future,
						   active = "home")


@app.route("/hackathon/<int:hackathon_id>")
def dash(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)
	now = datetime.datetime.now()

	req = urllib2.Request("https://graph.facebook.com/"+str(hackathon.facebook_id)+"/attending?access_token="+session["fb_token"])
	response = urllib2.urlopen(req)
	decoder = JSONDecoder()
	attending = decoder.decode(response.read())["data"]

	if now < hackathon.start_date:
		return render_template("dash-future.html", hackathon = hackathon, attending = attending)
	elif now < hackathon.end_date:
		return render_template("dash-present.html", hackathon = hackathon, attending = attending)
	else:
		return render_template("dash-past.html", hackathon = hackathon, attending = attending)

HackathonForm = model_form(Hackathon, exclude=("facebook_id", "owner"))
HackForm = model_form(Hack, exclude=("hackathon",))

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
				'start_time' : datetime.date.isoformat(hack.start_date),
				'end_time' : datetime.date.isoformat(hack.end_date),
				'description' : hack.description,
				'location' : hack.location})
			req = urllib2.Request("https://graph.facebook.com/"+str(hack.owner.facebook_id)+"/events", data)
			response = urllib2.urlopen(req)
			decoder = JSONDecoder()
			hack.facebook_id = decoder.decode(response.read())["id"]
			hack.save()
			return redirect(url_for("dash", hackathon_id = hack.id))
	else:
		form = HackathonForm()

	return render_template("hackathon-create.html", form = form, active = "create")

@app.route("/hackathon/<int:hackathon_id>/addhack", methods=["GET", "POST"])
def hack_create(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)
	hack = Hack()

	if request.method == "POST":
		form = HackForm(request.form)
		if form.validate():
			form.populate_obj(hack)
			hack.hackathon = hackathon
			hack.save()
			flash("Your hack was successfully added", "success")
			return redirect(url_for("dash", hackathon_id = hackathon.id))
	else:
		form = HackForm()

	return render_template("hack-create.html", form = form, hackathon = hackathon)
