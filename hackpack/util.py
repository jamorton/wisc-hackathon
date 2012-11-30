
from flask import abort

def get_object_or_404(model, **kwargs):
	try:
		return model.get(**kwargs)
	except model.DoesNotExist:
		abort(404)
