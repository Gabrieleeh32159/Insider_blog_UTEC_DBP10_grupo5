import unittest
import base64

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
            'username': 'xd',
            'description': 'xd',
            'email': 'xd',
            'image': base64.b64encode(
                open('server/imagenes/default.jpg', 'rb').read()).decode('utf-8'),
            'password': 'xd'
        }

    #---------Users-----------#

    def test_get_users_success(self):

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

    def tearDown(self):
        pass
