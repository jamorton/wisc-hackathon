
import os

class Config(object):
	DEBUG = False
	DATABASE = {
		'engine': 'peewee.SqliteDatabase',
		'name': 'hackpack.db'
	}
	UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
	SECRET_KEY = "none"

class DevelopmentConfig(Config):
	SECRET_KEY = 'yaoijetosihy4806uhy973hut089YH*(&^$$$$$$$$$$$w'
	DEBUG = True

def get_config():
	return DevelopmentConfig
