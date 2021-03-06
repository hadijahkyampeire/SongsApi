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

    def register_user(self, username="haddie", email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'username':username,
            'email': email,
            'password': password
        }
        return self.client.post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/auth/login', data=user_data)

    def test_songs_creation(self):
        """Test the API can create songs"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token), data=self.song)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Song successfully created', str(result.data))

    def test_songs_fetching(self):
        """Test the API can get songs"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/song/songs', headers=dict(Authorization="Bearer " + access_token),data=self.song)
        result = self.client.get('/song/songs', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_songs_can_be_got_by_id(self):
        """Test the API can get one song"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/song/songs', headers=dict(Authorization="Bearer " + access_token),data=self.song)
        result = self.client.get('/song/songs/1', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_song_can_be_edited(self):
        """Test the API can allow edit"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/song/songs',headers=dict(Authorization="Bearer " + access_token), data=self.song)
        new_data = {'title':'kiwani', 'artist':'bobi'}
        result2 = self.client.put('/song/songs/1',headers=dict(Authorization="Bearer " + access_token), data=new_data)
        self.assertEqual(result2.status_code, 201)

    def test_song_can_be_deleted(self):
        """Test the API can allow delete of a song"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token), data=self.song)
        result = self.client.delete('/song/songs/1', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_song_to_be_deleted_is_not_found(self):
        """Test the API can not allow delete of a song"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.delete('song/songs/1', 
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_song_to_be_edited_is_not_found(self):
        """Test the API can not allow edit of a song"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        new_data = {'title':'kiwani', 'artist':'bobi'}
        result = self.client.put('/song/songs/1',
            headers=dict(Authorization="Bearer " + access_token), data=new_data)
        self.assertEqual(result.status_code, 404)

    def test_song_to_be_got_is_not_found(self):
        """Test the API can not allow getting of a song"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.get('/song/songs/1', 
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)
    
    def test_user_cannot_add_songs_with_no_token(self):
        """Test APi handles error when posting with no token"""
        result = self.client.post('/song/songs', data=self.song)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_songs_with_no_token(self):
        """Test APi handles error when getting songs with no token"""
        add = self.client.post('/song/songs', data=self.song)
        result = self.client.get('/song/songs')
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_edit_songs_with_no_token(self):
        """Test APi handles error when puting with no token"""
        res = self.client.post('/song/songs', data=self.song)
        new_data={'title':'one step','artist':'beyonce'}
        result = self.client.put('/song/songs/1', data=new_data)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_song_by_id_with_no_token(self):
        """Test APi handles error when getting a song with no token"""
        result1 = self.client.post('/song/songs', data=self.song)
        result = self.client.get('/song/songs/1', data=self.song)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_delete_songs_with_no_token(self):
        """Test APi handles error when delete with no token"""
        result1 = self.client.post('/song/songs', data=self.song)
        result = self.client.delete('/song/songs/1')
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_add_songs_with_invalid_token(self):
        """Test APi handles error when posting with invalid token"""
        access_token="zbncymk"
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token),
             data=self.song)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_edit_songs_with_invalid_token(self):
        """Test APi handles error when editing with invalid token"""
        access_token="zbncymk"
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token),
             data=self.song)
        new_song={"title":"one step at a time", "artist":"benyonce"}
        result = self.client.put('/song/songs/1',
            headers=dict(Authorization="Bearer " + access_token),
             data=new_song)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_one_songs_with_invalid_token(self):
        """Test APi handles error when viewing one song with invalid token"""
        access_token="zbncymk"
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token),
             data=self.song)
        result = self.client.get('/song/songs',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_songs_with_invalid_token(self):
        """Test APi handles error when viewing with invalid token"""
        access_token="zbncymk"
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token),
             data=self.song)
        result = self.client.get('/song/songs/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_delete_songs_with_invalid_token(self):
        """Test APi handles error when deleting with invalid token"""
        access_token="zbncymk"
        result = self.client.post('/song/songs',
            headers=dict(Authorization="Bearer " + access_token),
             data=self.song)
        result = self.client.delete('/song/songs/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 401)

    def tearDown(self):
        with app.app_context():
            # create all database tables
            db.session.remove()
            db.drop_all()