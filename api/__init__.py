import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api.config import app_config

app = Flask(__name__)
config_name = os.environ.get('APP_SETTINGS', 'development')
app.config.from_object(app_config.get(config_name))

db = SQLAlchemy(app) 

from api.songs import song
app.register_blueprint(song)