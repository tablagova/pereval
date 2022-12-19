from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from app import views
import json
from .models import PerevalAdded


class TestPerevalAddAndList(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PerevalAPIView.as_view({'get': 'get_user_records', 'post': 'post'})
        self.uri = '/submitData/'

    def test_create(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        response = self.client.post(self.uri, params, format='json')
        print(type(response.data))
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
        response_message = response.data['message']
        response_id = response.data['id']
        self.assertEqual([response_message, response_id], [None, 1],
                         f"Expected Response is {{'message': None, 'id': 1}}, "
                         f"received {{'message': {response_message}, 'id': {response_id}}} instead.")

    def test_empty_list(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        self.client.post(self.uri, params, format='json')
        request = self.factory.get(self.uri)
        response = self.view(request)
        print(response.data)
        print(PerevalAdded.objects.get(id=2))
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received{0}instead.'.format(response.status_code))
        self.assertEqual(response.data, [], "Expected Response.data must be an empty list")

    def test_list_for_email(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        self.client.post(self.uri, params, format='json')
        response = self.client.get('/submitData/', data={'user_email': '1234@1234.com'}, format='json')
        print(response.data)
        print(PerevalAdded.objects.get(id=3))
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))


class TestPerevalGetOneAndEdit(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PerevalAPIView.as_view({'patch': 'edit_one_record', 'get': 'get_one'})
        # self.uri = '/submitData/'

    def test_get_one_not_exists(self):
        response = self.client.get('/submitData/1')
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'.format(response.status_code))

    def test_get_one(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        self.client.post('/submitData/', params, format='json')
        response = self.client.get('/submitData/4')
        print(response.data)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_patch(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        self.client.post('/submitData/', params, format='json')
        response = self.client.patch('/submitData/5', params, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 202,
                         'Expected Response Code 202, received {0} instead.'.format(response.status_code))
        self.assertEqual(response.data['state'], 1,
                         'Expected Response state 1, received {0} instead.'.format(response.status_code))

    def test_patch_no_record(self):
        with open('app/test_pereval.json', 'r',  encoding='utf-8') as f:
            params = json.load(f)
        self.client.post('/submitData/', params, format='json')
        response = self.client.patch('/submitData/1', params, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'.format(response.status_code))
        self.assertEqual(response.data['state'], 0,
                         'Expected Response state 0, received {0} instead.'.format(response.status_code))
