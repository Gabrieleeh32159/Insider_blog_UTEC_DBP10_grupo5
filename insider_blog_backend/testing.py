import unittest
import base64
from random import randint

from server import create_app, setup_db
from models import setup_db, User, Post, Group, GroupUser
import json


class TestProyecto(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'proyectotest'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            'postgres', '1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_user = {
            'username': "".join([str(randint(0, 100)) for _ in range(10)]),
            'description': 'xd',
            'email': "".join([str(randint(0, 100)) for _ in range(10)]),
            'image': base64.b64encode(
                open('server/imagenes/default.jpg', 'rb').read()).decode('utf-8'),
            'password': 'xd'
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

        res = self.client().patch('/users/' + str(updated_id),
                                  json={"username": "xd2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], str(updated_id))

    def test_update_user_failed(self):
        res = self.client().delete('/users/10000')
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

    def tearDown(self):
        pass
