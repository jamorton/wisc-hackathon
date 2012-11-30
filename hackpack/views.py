
from app import app
from models import *
from flask import render_template

@app.route("/")
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



"""
@app.route("/hackathon/create")
def hackathon_Create():
"""


"""
	if request.method == "POST":
		form = HackathonForm(request.form)
		if form.validate():
			form.save()

	else:
		form = HackathForm()

	return render_template("dash_index", form = form)
"""
