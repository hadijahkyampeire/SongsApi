from webargs import fields, validate
from flask import make_response, jsonify
from functools import wraps
from .models import User

songs_args = {
    #required arguments and their validations
    'title':fields.Str(required=True, validate=validate.Length(3)),
    'artist':fields.Str(required=True, validate=validate.Length(3))
}

songs_id_arg = {
    'id':fields.Int()
}
user_args ={
    'username':fields.Str(required=True, validate=validate.Length(5)),
    'email':fields.Str(required=True, validate=validate.Email()),
    'password':fields.Str(required=True, validate=validate.Length(7))
}
login_args ={
    'email':fields.Str(required=True, validate=validate.Email()),
    'password':fields.Str(required=True, validate=validate.Length(7))
}
