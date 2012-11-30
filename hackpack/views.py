
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

		print "existing hackathons", h.start_date, " and ", h.end_date

		if now < h.start_date:
			hackathons_future.append(h)
		elif now < h.end_date:
			hackathons_now.append(h)

	return render_template("index.html",
						   hackathons_now = hackathons_now,
						   hackathons_future = hackathons_future,
						   active = "home")


@app.route("/hackathon/<int:hackathon_id>")
def dash(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)
	now = datetime.datetime.now()

	hacks = []

	hack_q = Hack.select().where(hackathon = hackathon)
	for h in hack_q:
		hacks.append(h)

	if now < hackathon.start_date:
		return render_template("dash-future.html", hackathon = hackathon)
	elif now < hackathon.end_date:
		return render_template("dash-present.html", hackathon = hackathon, hacks = hacks)
	else:
		return render_template("dash-past.html", hackathon = hackathon, hacks = hacks)

HackForm = model_form(Hack, exclude=("hackathon",))

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
