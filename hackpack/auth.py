
from flask import render_template, g, session
from flask_peewee.auth import Auth
from app import app, db
from models import *

class CustomAuth(Auth):

	def get_user_model(self):
		return User

	def login(self):
		return render_template("login.html")

	def login_user(self, user):
		session['logged_in'] = True
		session['user_pk'] = user.get_id()
		session.permanent = True
		g.user = user

	def logout_user(self, user):
		if self.clear_session:
			session.clear()
		else:
			session.pop('logged_in', None)
			g.user = None

auth = CustomAuth(app, db)
