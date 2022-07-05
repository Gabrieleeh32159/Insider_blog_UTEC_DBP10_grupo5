import unittest
import base64
from random import randint
import string
import random

from server import create_app, setup_db
from models import setup_db, User, Post, Group, GroupUser
import json

length_of_string = 8


class TestProyecto(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'proyectotest'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            'postgres', '1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_user = {
            'username': ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)),
            'description': 'xd',
            'email': ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)),
            'image': base64.b64encode(
                open('server/imagenes/default.jpg', 'rb').read()).decode('utf-8'),
            'password': 'xd'
        }

        self.new_group = {
            'groupname': ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        }

        self.new_post = {
            'title': 'xd',
            'content': 'xd',
            'user_id': 1,
            'group_id': 1,
        }

        self.new_post_2 = {
            'user_id': 1,
            'group_id': 0,
        }

    #---------Users-----------#

    def test_get_users_success(self):
        self.client().post('/users', json=self.new_user)

        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['amount_users'])
        self.assertTrue(len(data['users']))

    def test_get_users_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/users?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_users_success(self):
        res = self.client().post('/users', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']))
        self.assertTrue(data['total_users'])

    def test_create_users_failed(self):
        res = self.client().post('/users', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_signup_success(self):
        res = self.client().post('/signup', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_signup_failed_unprocessable(self):
        res = self.client().post('/users', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_update_user_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        updated_id = data0['created']

        res = self.client().patch('/users/' + str(updated_id), json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], str(updated_id))

    def test_update_user_failed(self):
        res = self.client().patch('/users/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_user_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/users/' + str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(deleted_id))
        self.assertTrue(len(data['users']))
        self.assertTrue(data['total_users'])

    def test_delete_user_failed(self):
        res = self.client().delete('/users/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #---------Groups------------------#

    def test_get_group_success(self):
        res = self.client().get('/groups')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_groups'])
        self.assertTrue(len(data['grupos']))

    def test_get_groups_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/groups?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_group_success(self):
        res = self.client().post('/groups', json=self.new_group)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['groups']))
        self.assertTrue(data['total_groups'])

    def test_create_group_failed(self):
        res = self.client().post('/groups', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_group_success(self):
        res0 = self.client().post('/groups', json=self.new_group)
        data0 = json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/groups/' + str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], deleted_id)
        self.assertTrue(len(data['groups']))
        self.assertTrue(data['total_groups'])

    def test_delete_group_failed(self):
        res = self.client().delete('/groups/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_group_sucess(self):
        res0 = self.client().post('/groups', json=self.new_group)
        data0 = json.loads(res0.data)
        updated_id = data0['created']

        res = self.client().patch('/groups/' + str(updated_id), json=self.new_group)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], str(updated_id))

    def test_update_group_success(self):
        res = self.client().patch('/groups/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #-----------------POSTS---------------------#

    def test_create_post_sucess(self):
        res = self.client().post('/posts', json=self.new_post)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['posts'])

    def test_create_post_failed(self):
        res = self.client().post('/posts', json=self.new_post_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def tearDown(self):
        pass
