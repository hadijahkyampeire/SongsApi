from flask import request, jsonify, make_response
from flask_restful import Resource
from webargs.flaskparser import use_args
from .args import songs_args, songs_id_arg
from .models import Songs

class SongsListView(Resource):
    """songs view"""
    @use_args(songs_args, locations={'json', 'form'})
    def post(self, args):
        new_song=Songs(
            title=args['title'],
            artist=args['artist']
        )
        new_song.save()
        response = {'message':'Song successfully created'}
        return make_response(jsonify(response), 201)


    def get(self):
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



