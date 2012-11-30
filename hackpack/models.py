
import datetime
from flask import url_for
from peewee import *

from app import db

class BaseModel(db.Model):
	pass

class User(BaseModel):
	facebook_id = IntegerField(unique = True)

	@staticmethod
	def get_or_create(fbid):
		try:
			u = User.get(facebook_id = fbid)
		except User.DoesNotExist:
			u = User(facebook_id = fbid)
			u.save()
		return u

def create_tables():
	User.create_table()
