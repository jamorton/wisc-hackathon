
from app import app
from models import *
from flask import render_template, request
from auth import auth
from wtfpeewee.orm import model_form

@app.route("/")
@auth.login_required
def dash_index():
	return render_template("index.html")

@app.route("/dash-past")
def dash_past():
	return render_template("dash-past.html")

@app.route("/dash-present")
def dash_present():
	return render_template("dash-present.html")

@app.route("/dash-future")
def dash_future():
	return render_template("dash-future.html")



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
			hack.save()
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
