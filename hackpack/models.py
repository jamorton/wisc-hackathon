
import datetime
from flask import url_for
from peewee import *

from app import db

__all__ = ["Hackathon", "User", "Hack", "create_tables"]

class BaseModel(db.Model):
	pass

class User(BaseModel):
	facebook_id = IntegerField(unique = True)
	active = BooleanField(default = True)

	@staticmethod
	def get_or_create(fbid):
		try:
			u = User.get(facebook_id = fbid)
		except User.DoesNotExist:
			u = User(facebook_id = fbid)
			u.save()
		return u

class Hackathon(BaseModel):
	title = CharField()
	description = TextField()
	start_date = DateTimeField(default = datetime.datetime.now)
	end_date = DateTimeField(default = datetime.datetime.now)
	location = CharField()
	facebook_id = IntegerField(default = 0)
	owner = ForeignKeyField(User)
	url_name = CharField(default = "")

class Hack(BaseModel):
	hackathon = ForeignKeyField(Hackathon)
	title = CharField()
	screenshot_url = TextField(default="")
	github_repo = TextField(default="")
	url = TextField(default = "")
	description = TextField(default = "")

def create_tables():
	Hackathon.create_table()
	User.create_table()
	Hack.create_table()
