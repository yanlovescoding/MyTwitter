from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.createUser(
            username='unitTest',
            email='unitTest@gmail.com',
            password='test123',
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login_successfully(self):
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test123',
        })
        self.assertEqual(response.status_code, 200)
        # Confirm login status is true
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_login_but_use_wrong_http_method(self):
        # case one: get
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': self.user.password,
        })
        self.assertEqual(response.status_code, 405)

    def test_login_with_wrong_password(self):
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': "test12345890",
        })

        self.assertEqual(response.json(), {'success': False, 'message': 'username and password does not match'})
        self.assertEqual(response.status_code, 400)

    def test_login_with_username_not_existed(self):
        response = self.client.post(LOGIN_URL, {
            'username': "fake_username",
            'password': "test12345890",
        })

        self.assertEqual(response.json(), {
            "success": False,
            "message": "Please check input.",
            "errors": {
                "username": [
                    "User does not exist."
                ]
            }
        })
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        # login
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test123',
        })
        # confirm login successful
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # case 1: get method
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # case 2: post method
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'testAccount1',
            'email': 'testAccount1@gmail.com',
            'password': 'test121',
        }
        # case 1: get method
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # case 2: not validate email
        response = self.client.post(SIGNUP_URL, {
            'username': 'testAccount2',
            'email': 'email@@@',
            'password': 'test12'
        })
        self.assertEqual(response.status_code, 400)

        # case 3: long user name
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong))))))0000000000000000',
            'email': 'test@gmail.com',
            'password': 'test123',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # case 4: sign up successful
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], 'testaccount1')
        # Confirm log in successfully after signing up
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
