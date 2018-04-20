from flask import jsonify, make_response, request
from flask_restful import Resource
from webargs.flaskparser import use_args
from api.songs.args import songs_args
from api.songs.models import Songs, User

class SongsListView(Resource):
    """songs view"""
    @use_args(songs_args, locations={'json', 'form'})
    def post(self, args):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                new_song=Songs(
                    title=args['title'],
                    artist=args['artist']
                )
                new_song.save()
                response = {'message':'Song successfully created'}
                return make_response(jsonify(response), 201)
            return make_response(jsonify({'message': user_id}),401)

    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                songs = Songs.query.all()
                items=[]
                for song in songs:
                    song_data={}
                    song_data['id']=song.id
                    song_data['title']=song.title
                    song_data['artist']=song.artist
                    items.append(song_data)

                response={'song_items':items}
                return make_response(jsonify(response), 200)
            return make_response(jsonify({'message': user_id}),401)

class SongDetailsView(Resource):
    """song details"""
    def get(self, song_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                song= Songs.query.filter_by(id=song_id).first()
                if not song:
                    return make_response(jsonify({
                        'message':'no song found by id'
                    }), 404)
                response = {
                    'song':{
                        'id':song.id,
                        'title':song.title,
                        'artist':song.artist
                    }
                }
                return make_response(jsonify(response), 200)
            return make_response(jsonify({'message': user_id}),401)

    def delete(self, song_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                song = Songs.query.filter_by(id=song_id).first()
                if not song:
                    return make_response(jsonify({
                        'message':'no song found by id'
                    }), 404)
                song.delete()
                return make_response(jsonify({
                    'message':'Song successfully deleted'
                }), 200)
            return make_response(jsonify({'message': user_id}),401)

    @use_args(songs_args, locations={'json', 'form'})
    def put(self, args, song_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                song = Songs.query.filter_by(id=song_id).first()
                if not song:
                    return make_response(jsonify({
                        'message':'no song found by id'
                    }), 404)
                song.title=args['title']
                song.artist= args['artist']
                song.save()
                response = {
                    'song':{
                        'id':song.id,
                        'title':song.title,
                        'artist':song.artist
                    }
                }
                return make_response(jsonify(response), 201)
            return make_response(jsonify({'message': user_id}),401)

