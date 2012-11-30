
from app import app
from models import *
from flask import render_template, request, url_for, redirect
from auth import auth
from wtfpeewee.orm import model_form
from util import get_object_or_404
import datetime
import urllib, urllib2

@app.route("/")
@auth.login_required
def index():
	return render_template("index.html")

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
			data = urllib.encode({
				'name' : hack.title,
				'start_time' : hack.start_time,
				'end_time' : hack.end_time,
				'description' : hack.description,
				'location' : hack.location})
			event_id = urllib2.urlopen(urllib2.Request("http://www.facebook.com/"+hack.owner+"/events", data))
			hack.facebook_id = event_id
			hack.save()
			return redirect(url_for("dash", event_id))
	else:
		form = HackathonForm()

	return render_template("hackathon-create.html", form = form)

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
			return redirect(url_for("dash", hackathon.id))
	else:
		form = HackForm()

	return render_template("hack-create.html", form = form, hackathon = hackathon)
