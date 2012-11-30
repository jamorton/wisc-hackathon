
import datetime
from flask import url_for
from peewee import *

from app import db

__all__ = ["Hackathon", "User", "Team", "Membership", "create_tables"]

class BaseModel(db.Model):
	pass

class Hackathon(BaseModel):
	title = CharField()
	date = DateTimeField(default = datetime.datetime)
	facebook_id = IntegerField()

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
