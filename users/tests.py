import jwt, bcrypt

from django.test     import TestCase, Client

from cardoc.settings import SECRET_KEY
from users.models    import User

class SingUpTest(TestCase):
    def setUp(self):
        password = 'TestTest!@'
        user     = User.objects.create(
            id       = 1,
            username = 'firstuser',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
                
    def tearDown(self):
        User.objects.all().delete()
    
    def test_sign_up_post_success(self):
        client = Client()
        data   = {
            'id'       : 'newuser',
            'password' : 'TestTest12!@'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        
    def test_sign_up_post_username_duplicated_fail(self):
        client = Client()
        data   = {
            'id'       : 'firstuser',
            'password' : 'Test12345!@'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'USERNAME_ALREADY_EXIST'})
        
    def test_sign_up_post_invalid_username_fail(self):
        client = Client()
        data   = {
            'id'       : 'UserIDisTooLong',
            'password' : 'Test12345!@'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'INVALID_USERNAME'})

    def test_sign_up_post_invalid_password_fail(self):
        client = Client()
        data   = {
            'id'       : 'newuser',
            'password' : 'wrongpassword'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})

    def test_sign_up_post_key_error_fail(self):
        client = Client()
        data   = {
            'password' : 'without_id'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

class SingInTest(TestCase):
    def setUp(self):
        password = 'Test12345!@'
        user     = User.objects.create(
            id       = 1,
            username = 'firstuser',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        global access_token
        access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        
    def tearDown(self):
        User.objects.all().delete()
    
    def test_sign_in_post_success(self):
        client = Client()
        data   = {
            'id'       : 'firstuser',
            'password' : 'Test12345!@'
        }
        response = client.post('/users/signin', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'access_token' : access_token})

    def test_sign_in_post_invalid_username_fail(self):
        client = Client()
        data   = {
            'id'       : 'wrongusername',
            'password' : 'Test12345!@'
        }
        response = client.post('/users/signin', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message':'INVALID_USERNAME'})

    def test_sign_in_post_invalid_password_fail(self):
        client = Client()
        data   = {
            'id'       : 'firstuser',
            'password' : 'wrong!!!'
        }
        response = client.post('/users/signin', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message':'INVALID_PASSWORD'})

    def test_sign_in_post_key_error_fail(self):
        client = Client()
        data   = {
            'password' : 'without_id'
        }
        response = client.post('/users/signin', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'KEY_ERROR'})