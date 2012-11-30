
import datetime
from flask import url_for
from peewee import *

from app import db

__all__ = ["Hackathon", "User", "Hack", "Shoutout", "Announcement", "create_tables"]

def deftime():
	print datetime.datetime.now()
	return datetime.datetime.now()

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
	start_date = DateTimeField(default = deftime)
	end_date = DateTimeField(default = deftime)
	location = CharField()
	facebook_id = IntegerField(default = 0)
	owner = ForeignKeyField(User)
	url_name = CharField(default = "")
	calculated = BooleanField(default=False)
	stats = TextField(default="")
	trivia = TextField(default="")

class Hack(BaseModel):
	hackathon = ForeignKeyField(Hackathon)
	description = TextField()
	title = CharField()
	screenshot_url = TextField(default="")
	github_repo = TextField(default="")
	url = TextField(default = "")
	description = TextField(default = "")

class Shoutout(BaseModel):
	user = ForeignKeyField(User)
	hackathon = ForeignKeyField(Hackathon)
	message = TextField()

class Announcement(BaseModel):
	hackathon = ForeignKeyField(Hackathon)
	time = DateTimeField(default = deftime)
	message = TextField()

def create_tables():
	Hackathon.create_table()
	User.create_table()
	Hack.create_table()
	Shoutout.create_table()
	Announcement.create_table()
