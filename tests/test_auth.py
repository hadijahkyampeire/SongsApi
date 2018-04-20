import unittest
import json
from api import app, db
from api.config import app_config
from api.songs.models import User

class AuthTestCase(unittest.TestCase):
    """This represents the authentication testcase"""

    def setUp(self):
        # binds the app to the current context
        self.client = app.test_client()
        self.user = {
            'username': 'haddie',
            'email': 'test@example.com',
            'password': 'test_password'}
        with app.app_context():
            # create all database tables
            db.create_all()
    def test_successful_registration(self):
        """Test when user registers with right credentials"""
        res = self.client.post('auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client.post('auth/register',data=self.user)
        second_res = self.client.post('auth/register',
        data=self.user)
        self.assertEqual(second_res.status_code, 409)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists please login")
    
    def test_user_login(self):
        """Test registered user can login."""
        res = self.client.post('/auth/register',data=self.user)
        login_res = self.client.post('/auth/login',
        data=self.user)
        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def tearDown(self):
        with app.app_context():
            # create all database tables
            db.session.remove()
            db.drop_all()