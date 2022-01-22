# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database says I need to add this file

import os
basedir = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
	# I'm not really sure what this does lol - Will
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False