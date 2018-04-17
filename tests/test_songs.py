import unittest
import json
from api import app, db
from api.config import app_config
from api.songs.models import Songs

class SongsTestCase(unittest.TestCase):
    """This represents the songs testcase"""

    def setUp(self):
        # binds the app to the current context
        self.client = app.test_client()
        self.song = {'title': 'queen of my heart', 'artist':'westlife boys'}
        with app.app_context():
            # create all database tables
            db.create_all()

    def test_songs_creation(self):
        """Test the API can create songs"""
        result = self.client.post('song/songs', data=self.song)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Song successfully created', str(result.data))

    def test_songs_fetching(self):
        """Test the API can get songs"""
        result = self.client.post('song/songs', data=self.song)
        result = self.client.get('song/songs')
        self.assertEqual(result.status_code, 200)

    def test_songs_can_be_got_by_id(self):
        """Test the API can get one song"""
        result = self.client.post('song/songs', data=self.song)
        result = self.client.get('song/songs/1')
        self.assertEqual(result.status_code, 200)

    def test_song_can_be_edited(self):
        """Test the API can allow edit"""
        result1 = self.client.post('song/songs', data=self.song)
        new_data = {'title':'kiwani', 'artist':'bobi'}
        result2 = self.client.post('song/songs', data=new_data)
        self.assertEqual(result2.status_code, 201)

    def test_song_can_be_deleted(self):
        """Test the API can allow delete of a song"""
        result = self.client.post('song/songs', data=self.song)
        result = self.client.delete('song/songs/1')
        self.assertEqual(result.status_code, 200)

    def test_song_to_be_deleted_is_not_found(self):
        """Test the API can not allow delete of a song"""
        result = self.client.delete('song/songs/1')
        self.assertEqual(result.status_code, 404)

    def test_song_to_be_edited_is_not_found(self):
        """Test the API can not allow edit of a song"""
        new_data = {'title':'kiwani', 'artist':'bobi'}
        result = self.client.put('song/songs/1', data=new_data)
        self.assertEqual(result.status_code, 404)

    def test_song_to_be_got_is_not_found(self):
        """Test the API can not allow getting of a song"""
        result = self.client.get('song/songs/1')
        self.assertEqual(result.status_code, 404)
    
    def tearDown(self):
        with app.app_context():
            # create all database tables
            db.session.remove()
            db.drop_all()