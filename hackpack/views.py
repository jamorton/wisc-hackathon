
from app import app
from models import *
from flask import render_template, request, url_for, redirect, session, flash, jsonify
from auth import auth
from wtfpeewee.orm import model_form
from util import get_object_or_404
import datetime
import urllib, urllib2
from json import JSONDecoder
import json
import os

@app.route("/")
@auth.login_required
def index():
	hackathon_q = Hackathon.select()

	hackathons_now = []
	hackathons_future = []
	hackathon_query = []
	now = datetime.datetime.now()
	for h in hackathon_q:

		if now < h.start_date:
			hackathons_future.append(h)
		elif now < h.end_date:
			hackathons_now.append(h)
		hackathon_query.append(h)

	return render_template("index.html",
						   hackathons_now = hackathons_now,
						   hackathons_future = hackathons_future,
						   hackathon_query = hackathon_query,
						   active = "home")


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

def walk(current_dir, languages):
	for root, dirs, files in os.walk(current_dir):
		for dire in dirs:
			if dire == "." or dire == "..":
				continue
			languages = walk(dire, languages)
		for name in files:
			if name == "." or name == "..":
				continue
			if ".js" in name:
				if ( not languages.has_key("javascript") ):
					languages["javascript"] = 0
				languages["javascript"] = languages["javascript"] + 1
			elif ".html" in name:
				if ( not languages.has_key("html") ):
					languages["html"] = 0
				languages["html"] = languages["html"] + 1
			elif ".py" in name:
				if ( not languages.has_key("python") ):
					languages["python"] = 0
				languages["python"] = languages["python"] + 1
			elif ".java" in name:
				if ( not languages.has_key("java") ):
					languages["java"] = 0
				languages["java"] = languages["java"] + 1
			elif name.endswith(".c") or name.endswith(".C"):
				if ( not languages.has_key("c") ):
					languages["c"] = 0
				languages["c"] = languages["c"] + 1
			elif name.endswith(".cpp") or name.endswith(".CPP"):
				if ( not languages.has_key("c++") ):
					languages["c++"] = 0
				languages["c++"] = languages["c++"] + 1
			elif "Android" in name or "android" in name:
				if ( not languages.has_key("android") ):
					languages["android"] = 0
				languages["android"] = languages["android"] + 1
			elif ".css" in name:
				if ( not languages.has_key("css") ):
					languages["css"] = 0
				languages["css"] = languages["css"] + 1
			elif ".erb" in name:
				if ( not languages.has_key("ruby") ):
					languages["ruby"] = 0
				languages["ruby"] = languages["ruby"] + 1
			elif name.endswith(".m"):
				if ( not languages.has_key("objective-c") ):
					languages["objective-c"] = 0
				languages["objective-c"] = languages["objective-c"] + 1
	return languages

def hack_get_all_time_stats(hackathon, hacks):

	if hackathon.calculated:
		print hackathon.stats
		return render_template("dash-past.html", hackathon = hackathon, stats = JSONDecoder().decode(hackathon.stats), hacks = hacks)

	hack_q = Hack.select().where(Hack.hackathon==hackathon)

	user_commits = {}
	biggest = 0
	top_committer = ""
	max_num_commits = 0

	languages = {}

	for h in hack_q:
		if len(h.github_repo) == "":
			continue
		repo_address = h.github_repo
		original = repo_address
		repo_address = repo_address.replace("https://", "").replace("http://", "").replace("git@github.com:", "").replace("github.com/", "").replace(".git", "")
		repo_owner = repo_address.split("/")[0]
		repo_name = repo_address.split("/")[1]
		req = urllib2.Request("https://api.github.com/repos/"+repo_owner+"/"+repo_name+"/commits?per_page=10000")
		response = urllib2.urlopen(req)
		decoder = JSONDecoder()
		commits = decoder.decode(response.read())
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

		max_num_commits += len(commits)

		os.system("git clone "+original)
		before = os.getcwd()
		os.chdir(repo_name)

		repo_languages = walk(os.getcwd(), {})

		for language in repo_languages.keys():
			if ( not languages.has_key(language) ):
				languages[language] = 0
			languages[language] = languages[language] + 1

		os.chdir(before)
		os.system("rm -rf "+repo_name)

	first = ""
	st1 = 0
	second = ""
	nd2 = 0
	third = ""
	rd3 = 0
	for k in languages.keys():
		if ( languages[k] > st1 ):
			third = second
			rd3 = nd2
			second = first
			nd2 = st1
			first = k
			st1 = languages[k]
		elif ( languages[k] > nd2 ):
			third = second
			rd3 = nd2
			second = k
			nd2 = languages[k]
		elif ( languages[k] > rd3 ):
			third = k
			rd3 = languages[k]

	top3 = first + ", " + second + ", " + third

	hackathon.calculated = True
	hackathon.stats = json.dumps({"max-number-commits" : max_num_commits, "top-committer" : top_committer, "top3-languages" : top3 })
	hackathon.save()
	return render_template("dash-past.html", hackathon = hackathon, stats = JSONDecoder().decode(hackathon.stats), hacks = hacks)


@app.route("/hackathon/<int:hackathon_id>/manage", methods=["GET", "POST"])
def manage_hackathon(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)

	if request.method == "POST":
		ann = Announcement(hackathon = hackathon, message = request.form["message"])
		ann.save()
		return redirect(url_for("dash", hackathon_id = hackathon.id))

	return render_template("manage.html", hackathon = hackathon)

@app.route("/hackathon/<int:hackathon_id>")
def dash(hackathon_id):
	hackathon = get_object_or_404(Hackathon, id = hackathon_id)
	now = datetime.datetime.now()

	hacks = []

	hack_q = Hack.select().where(Hack.hackathon==hackathon)
	for h in hack_q:
		hacks.append(h)

	if now < hackathon.start_date:
		return render_template("dash-future.html", hackathon = hackathon)
	elif now < hackathon.end_date:
		anns = Announcement.select().where(Announcement.hackathon == hackathon).order_by(Announcement.time)
		return render_template("dash-present.html", hackathon = hackathon, hacks = hacks, anns = anns)
	else:
		return hack_get_all_time_stats(hackathon, hacks)

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
