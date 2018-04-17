from flask import Blueprint
from flask_restful import Api
from .views import SongsListView, SongDetailsView

song = Blueprint('song', __name__, url_prefix='/song')
song_api = Api(song)

song_api.add_resource(SongsListView, '/songs')
song_api.add_resource(SongDetailsView, '/songs/<int:song_id>')