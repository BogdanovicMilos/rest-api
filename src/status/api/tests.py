import os
import shutil
import tempfile
from PIL import Image

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from status.models import Status
from django.conf import settings

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class StatusAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='testuser@gmail.com')
        user.set_password('testing321')
        user.save()

        status_obj = Status.objects.create(user=user, content='Hello')

    def test_statuses(self):
        self.assertEqual(Status.objects.count(), 1)

    def status_user_token(self):
        auth_url = api_reverse('api-auth:login')
        auth_data = {
            'username': 'testuser',
            'password': 'testing321',
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data.get('token', None)
        if token is not None:
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    def test_empty_create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content': None,
            'image': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response.data

    def test_status_create_with_image(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        image_item = Image.new('RGB', (800, 1290), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': 'testing',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)
            img_data = response.data.get('image')
            self.assertNotEqual(img_data, None)
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    def test_status_create_with_image_and_desc(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        image_item = Image.new('RGB', (800, 1290), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': None,
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print(response.data)
            self.assertEqual(Status.objects.count(), 2)
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    def test_status_create(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'another testing'
        }

        '''
        get
        '''

        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_status_update(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'another testing'
        }

        '''
        put / update

        '''
        put_response = self.client.put(rud_url, rud_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        rud_response_data = put_response.data
        self.assertEqual(rud_response_data['content'], rud_data['content'])

    def test_status_delete(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'another testing'
        }

        '''
        delete
        '''

        delete_response = self.client.delete(rud_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        '''
        Not Found
        '''

        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_no_token_create(self):
        url = api_reverse('api-status:list')
        data = {
            'content': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_other_user_permissions_api(self):
        data = self.create_item()
        data_id = data.get('id')
        user = User.objects.create(username='testmilos')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        rud_url = api_reverse('api-status:detail', kwargs={'id': data_id})
        rud_data = {
            'content': 'smash'
        }
        get_ = self.client.get(rud_url, format='json')
        put_ = self.client.put(rud_url, rud_data, format='json')
        delete_ = self.client.delete(rud_url, format='json')
        self.assertEqual(get_.status_code, status.HTTP_200_OK)
        self.assertEqual(put_.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_.status_code, status.HTTP_403_FORBIDDEN)
