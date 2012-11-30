
from flask import Flask
from flask_peewee.db import Database

import config
app = Flask(__name__)
app.config.from_object(config.get_config())

db = Database(app)
