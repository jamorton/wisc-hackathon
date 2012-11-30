
import datetime
from flask import url_for
from peewee import *

from app import db

__all__ = ["Hackathon", "User", "Team", "Membership", "create_tables"]

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

class Team(BaseModel):
	hackathon = ForeignKeyField(Hackathon)

class Membership(BaseModel):
	user = ForeignKeyField(User)
	team = ForeignKeyField(Team)

def create_tables():
	Hackathon.create_table()
	User.create_table()
	Team.create_table()
	Membership.create_table()
