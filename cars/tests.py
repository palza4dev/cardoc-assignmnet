import jwt, bcrypt, re

from django.test     import TestCase, Client, client

from cars.models     import Trim, UserTrim, Car, FrontTire, RearTire
from users.models    import User
from users.utils     import login_decorator
from cardoc.settings import SECRET_KEY

class TrimListTest(TestCase):
    def setUp(self):
        password = 'TestTest!@'
        user     = User.objects.create(
            id       = 1,
            username = 'firstuser',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        global access_token
        access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        
        Car.objects.create(id=1, brand_name='기아', model_name='오피러스', submodel_name='오피러스', grade_name='2.7 가솔린')
        Trim.objects.create(id=1, name='테스트', car_id=1)
        Trim.objects.create(id=5000, name='GH270 고급형', car_id=1)
        UserTrim.objects.create(id=1, user_id=1, trim_id=5000)
        FrontTire.objects.create(id=1, name='타이어 전', value='225/60R16', unit='', multi_values='', width='225', profile='60', diameter='16', trim_id=5000)
        RearTire.objects.create(id=1, name='타이어 후', value='225/60R16', unit='', multi_values='', width='225', profile='60', diameter='16', trim_id=5000)
        
    def tearDown(self):
        User.objects.all().delete()
        Trim.objects.all().delete()
        UserTrim.objects.all().delete()
        Car.objects.all().delete()
        FrontTire.objects.all().delete()
        RearTire.objects.all().delete()
    
    def test_trim_list_post_success(self):
        client = Client()
        
        data = [{
                    "id": "firstuser",
                    "trimId": 1,
                    "frontTire" : 
                    {
                        "name": "타이어 전",
                        "value": "205/60R16",
                        "unit": "",
                        "multiValues": ""
                    },
                    "rearTire" :
                    {
                        "name": "타이어 후",
                        "value": "205/60R16",
                        "unit": "",
                        "multiValues": ""
                    }
                }]
        
        response = client.post('/cars/trim', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'created'})

    def test_trim_list_post_trim_does_not_exist_fail(self):
        client = Client()
        
        data = [{
                    "id": "firstuser",
                    "trimId": 999999,
                    "frontTire" : 
                    {
                        "name": "타이어 전",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    },
                    "rearTire" :
                    {
                        "name": "타이어 후",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    }
                }]
        
        response = client.post('/cars/trim', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'TRIM_DOES_NOT_EXIST'})

    def test_trim_list_post_user_does_not_exist_fail(self):
        client = Client()
        
        data = [{
                    "id": "no_user",
                    "trimId": 5000,
                    "frontTire" : 
                    {
                        "name": "타이어 전",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    },
                    "rearTire" :
                    {
                        "name": "타이어 후",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    }
                }]
        
        response = client.post('/cars/trim', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'USER_DOES_NOT_EXIST'})

    def test_trim_list_post_duplicated_fail(self):
        client = Client()
        
        data = [{
                    "id": "firstuser",
                    "trimId": 5000,
                    "frontTire" : 
                    {
                        "name": "타이어 전",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    },
                    "rearTire" :
                    {
                        "name": "타이어 후",
                        "value": "225/60R16",
                        "unit": "",
                        "multiValues": ""
                    }
                }]
        
        response = client.post('/cars/trim', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'ALREADY_EXISTS_DATA'})
    
    
    def test_trim_list_get_success(self):
        client  = Client()
        headers = {'HTTP_Authorization': access_token}
        
        response = client.get('/cars/trim', content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data": [
                {
                    "brandName": "기아",
                    "submodelName": "오피러스",
                    "gradeName": "2.7 가솔린",
                    "trimId": 5000,
                    "trimName": "GH270 고급형",
                    "frontTire": [
                        {
                            "name": "타이어 전",
                            "value": "225/60R16",
                            "unit" : "",
                            "multi_values": "",
                            "width": "225",
                            "profile": "60",
                            "diameter": "16"
                        }
                    ],
                    "rearTire": [
                        {
                            "name": "타이어 후",
                            "value": "225/60R16",
                            "unit" : "",
                            "multi_values": "",
                            "width": "225",
                            "profile": "60",
                            "diameter": "16"
                        }
                    ]
                }
            ]
        })
        
    def test_trim_list_get_invalid_token_fail(self):
        client  = Client()
        headers = {'HTTP_Authorization': 'wrong token'}
        
        response = client.get('/cars/trim', content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'INVALID_TOKEN'})

class TrimDetailTest(TestCase):
    def setUp(self):   
        Car.objects.create(id=1, brand_name='기아', model_name='오피러스', submodel_name='오피러스', grade_name='2.7 가솔린')
        Trim.objects.create(id=5000, name='GH270 고급형', car_id=1)
        FrontTire.objects.create(id=1, name='타이어 전', value='225/60R16', unit='', multi_values='', width='225', profile='60', diameter='16', trim_id=5000)
        RearTire.objects.create(id=1, name='타이어 후', value='225/60R16', unit='', multi_values='', width='225', profile='60', diameter='16', trim_id=5000)
        
    def tearDown(self):
        Car.objects.all().delete()
        Trim.objects.all().delete()
        FrontTire.objects.all().delete()
        RearTire.objects.all().delete()

    def test_trim_detail_get_success(self):
        client = Client()
        
        response = client.get('/cars/trim/5000', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data": {
                "brandName": "기아",
                "submodelName": "오피러스",
                "gradeName": "2.7 가솔린",
                "trimId": 5000,
                "trimName": "GH270 고급형",
                "frontTire": {
                    "name": "타이어 전",
                    "value": "225/60R16",
                    "unit" : "",
                    "multi_values": ""
                },
                "rearTire": {
                    "name": "타이어 후",
                    "value": "225/60R16",
                    "unit" : "",
                    "multi_values": ""
                }
            }
        })
        
    def test_trim_detail_get_trim_not_exist_fail(self):
        client = Client()
        
        response = client.get('/cars/trim/999', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'TRIM_DOES_NOT_EXIST'})
