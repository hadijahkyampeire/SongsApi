from flask import Blueprint
from flask_restful import Api
from .views import RegisterView, LoginView

auth = Blueprint('auth', __name__, url_prefix='/auth')
song_api = Api(auth)

song_api.add_resource(RegisterView, '/register')
song_api.add_resource(LoginView, '/login')