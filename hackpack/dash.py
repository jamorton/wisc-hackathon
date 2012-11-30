
from app import app
from models import *
from flask import render_template

@app.route("/")
def dash_index():
	return render_template("dash-index.html")
