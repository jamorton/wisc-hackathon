
import sys; sys.dont_write_bytecode = True

from app import app, db
from models import *
from views import *
from api import *

if __name__ == "__main__":
	app.run()
