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
            'group_id': 1,
        }

        self.new_groupuser = {
            'group_id': 1
        }

        res = self.client().get('/users')
        data = json.loads(res.data)

        if data['success'] != True:
            self.client().post('/users', json=self.new_user)
            self.client().post('/groups', json=self.new_group)

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
        self.client().post('/users', json=self.new_user)
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
        res = self.client().post('/groups', json=self.new_group)
        res = self.client().get('/groups')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_groups'])
        self.assertTrue(len(data['grupos']))

    def test_get_groups_sent_requesting_beyond_valid_page_404(self):
        res = self.client().post('/groups', json=self.new_group)
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

    def test_update_group_failed(self):
        res = self.client().patch('/groups/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #-----------------POSTS---------------------#

    def test_get_posts_success(self):
        res = self.client().post('/posts', json=self.new_post)
        res = self.client().get('/posts')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['amount_posts'])
        self.assertTrue(len(data['posts']))

    def test_get_posts_sent_requesting_beyond_valid_page_404(self):
        res = self.client().post('/posts', json=self.new_post)
        res = self.client().get('/posts?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

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

    def test_update_post_success(self):
        res0 = self.client().post('/posts', json=self.new_post)
        data0 = json.loads(res0.data)
        updated_id = data0['created']

        res = self.client().patch('/posts/' + str(updated_id), json=self.new_post)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], updated_id)

    def test_update_post_failed(self):
        res = self.client().patch('/posts/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_post_success(self):
        res0 = self.client().post('/posts', json=self.new_post)
        data0 = json.loads(res0.data)
        deleted_id = data0['created']

        res = self.client().delete('/posts/' + str(deleted_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], deleted_id)
        self.assertTrue(len(data['posts']))
        self.assertTrue(data['amount_posts'])

    def test_delete_post_failed(self):
        res = self.client().delete('/posts/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #-------------------GroupUser---------------------#

    def test_get_user_group_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        created_user = data0['created']

        res1 = self.client().post('/groups', json=self.new_group)
        data1 = json.loads(res1.data)
        created_group = data1['created']

        res = self.client().post('/user/' + str(created_user) +
                                 '/group/' + str(created_group))

        res = self.client().get('/groupusers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_groupusers'])
        self.assertTrue(len(data['groupusers']))

    def test_get_user_group_sent_requesting_beyond_valid_page_404(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        created_user = data0['created']

        res1 = self.client().post('/groups', json=self.new_group)
        data1 = json.loads(res1.data)
        created_group = data1['created']

        res = self.client().post('/user/' + str(created_user) +
                                 '/group/' + str(created_group))

        res = self.client().get('/groupusers?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_join_user_group_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        created_user = data0['created']

        res1 = self.client().post('/groups', json=self.new_group)
        data1 = json.loads(res1.data)
        created_group = data1['created']

        res = self.client().post('/user/' + str(created_user) +
                                 '/group/' + str(created_group))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_join_user_group_failed(self):
        res = self.client().post('/user/10000/group/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_user_group_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        created_user = data0['created']

        res1 = self.client().post('/groups', json=self.new_group)
        data1 = json.loads(res1.data)
        created_group = data1['created']

        res = self.client().post('/user/' + str(created_user) +
                                 '/group/' + str(created_group))

        res3 = self.client().delete('/group/' + str(created_group) +
                                    '/user/' + str(created_user))
        data = json.loads(res3.data)

        self.assertEqual(res3.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_user_group_failed(self):
        res = self.client().delete('/group/10000/user/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_group_user_success(self):
        res0 = self.client().post('/users', json=self.new_user)
        data0 = json.loads(res0.data)
        created_user = data0['created']

        res1 = self.client().post('/groups', json=self.new_group)
        data1 = json.loads(res1.data)
        created_group = data1['created']

        res = self.client().post('/user/' + str(created_user) +
                                 '/group/' + str(created_group))

        res = self.client().patch('/group/' + str(created_group) + "/user/" +
                                  str(created_user),  json=self.new_groupuser)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_update_group_user_failed(self):
        res = self.client().patch('/group/10000/user/1000', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def tearDown(self):
        pass
