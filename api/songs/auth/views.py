from flask import jsonify, make_response
from flask_restful import Resource
from webargs.flaskparser import use_args
from api.songs.args import user_args, login_args
from api.songs.models import User


class RegisterView(Resource):
    """Register view"""
    @use_args(user_args, locations={'json', 'form'})
    def post(self, args):
        try:
            new_user =User(
                username=args['username'],
                email=args['email'],
                password=args['password']
            )
            user= User.query.filter_by(email=args['email']).first()
            if user:
                return make_response(jsonify({
                    'message':'User already exists please login'
                }), 409)
            new_user.save()
            response = {'message':'You successfully registered'}
            return make_response(jsonify(response), 201)
        except Exception as e:  # pragma: no cover
            # An error occured, then return a message containing the error
            return make_response(jsonify({'message': 'Invalid data,'
                            ' something is wrong'}), 400)
    
class LoginView(Resource):
    """Login view"""
    @use_args(login_args, locations={'json', 'form'})
    def post(self, args):
        try:
            user= User.query.filter_by(email=args['email']).first()
            if user and user.password_is_valid(args['password']):
                # Generate the access token to be used as the header
                access_token = user.generate_token(user.id)
                if access_token:
                    return make_response(jsonify({'message': 
                        'You logged in successfully.',
                        'access_token': access_token,
                        'user_email': user.email,
                        'username': user.username,
                        'Id': user.id}
                        ), 200)

            return make_response(jsonify({'message': 'Invalid email or password,'
                            ' Please try again'}), 401)
        except Exception as e:  # pragma: no cover
            # Create a response containing an string error message
            return make_response(jsonify({'message': 
                'An error occured'
                ' ensure proper login'}), 401)