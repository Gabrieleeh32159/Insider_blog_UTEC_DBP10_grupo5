from argparse import _AttributeHolder
from datetime import datetime, timedelta
import json
from pickle import TRUE
import uuid
import psycopg2
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    request
)
import jwt
from functools import wraps
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import setup_db, User, Post, GroupUser, Group

default_image = 'default.jpg'

items_per_page = 5


def pagination(request, selection, decreasing=False):
    page = request.args.get('page', None, type=int)
    if page is None and not decreasing:
        start = 0
        end = 5
    elif page == 0:
        start = 0
        end = len(selection)
    elif decreasing:
        start = len(selection) - items_per_page
        end = len(selection)
        items = [item.format() for item in selection]
        current = items[start:end]
        return current[::-1]
    else:
        start = (page - 1)*items_per_page
        end = (start + items_per_page)
    items = [item.format() for item in selection]
    current = items[start:end]
    return current


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origin=['http://127.0.0.1:3000/'], max_age=1000)

    @app.after_request
    def after_request(response):
        #response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    #*USERS

    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.filter_by(
                    public_id=data['public_id']).first()
                if current_user is None:
                    return jsonify({'message': 'token is invalid'})
            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)
        return decorator

    @app.route('/users', methods=['GET'])
    def get_users():
        users = [user.format() for user in User.query.order_by('id').all()]

        if len(users) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'users': users,
            'amount_users': len(users)
        })

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        body = request.get_json()

        username = body.get('username', None)
        description = body.get('description', '')
        email = body.get('email', None)
        password = body.get('password', None)
        image = body.get('image', default_image)

        if username is None or email is None or password is None:
            abort(422)

        hashed_password = generate_password_hash(
            body['password'], method='sha256')

        user = User(public_id=str(uuid.uuid4()), username=username, description=description,
                    email=email, password=hashed_password, image_file=image)

        user.insert()
        return jsonify({
            'success': True
        })

    @app.route('/users', methods=['POST'])
    def create_user():
        body = request.get_json()

        if body is None:
            abort(422)

        username = body.get('username', None)
        description = body.get('description', '')
        email = body.get('email', None)
        password = body.get('password', None)
        image = body.get('image', default_image)

        if username is None or email is None or password is None:
            abort(422)

        if username is "" or email is "" or password is "":
            abort(422)

        hashed_password = generate_password_hash(
            body['password'], method='sha256')

        user = User(public_id=str(uuid.uuid4()), username=username, description=description,
                    email=email, password=hashed_password, image_file=image)

        new_user_id = user.insert()
        group_user = GroupUser(group_id=0, user_id=new_user_id)
        group_user.insert()

        selection = User.query.order_by('id').all()
        current_users = pagination(request, selection, True)

        return jsonify({
            'success': True,
            'created': new_user_id,
            'total_users': len(selection),
            'user': user.format()
        })

    @app.route('/user', methods=['GET'])
    def verify():
        auth = request.headers['Authorization']
        if auth is None:
            return make_response('No auth', 403, {'WWW.Authentication': 'Token Required'})

        token = auth.replace('Bearer ', '')

        print(token)

        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = User.query.filter_by(
            public_id=data['public_id']).first()
        if current_user is None:
            return jsonify({'message': 'token is invalid'})

        return current_user.format()

    @app.route('/login', methods=['GET', 'POST'])
    def login_user():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = User.query.filter_by(username=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({
                'token': token,
                'user': user.format()
            })

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    @app.route('/users/<user_id>', methods=['PATCH'])
    def update_user(user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()

            if user is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'username' in body:
                if body.get('username') != "":
                    user.username = body.get('username')
            if 'email' in body:
                if body.get('email') != "":
                    user.email = body.get('email')
            if 'password' in body:
                if body.get('password') != "":
                    user.password = body.get('password')
            if 'description' in body:
                if body.get('description') != "":
                    user.description = body.get('description')

            if body.get('username') == "" and body.get('email') == "" and body.get('password') == "" and body.get('description') == "":
                abort(422)

            user.update()

            return jsonify({
                'success': True,
                'id': user_id
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()

            if user is None:
                error_404 = True
                abort(404)

            user.delete()

            selection = User.query.order_by('id').all()
            users = pagination(request, selection)

            return jsonify({
                "success": True,
                "deleted": user_id,
                "users": users,
                "total_users": len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* GROUPS

    @app.route('/groups', methods=['POST'])
    #@token_required
    def create_group():
        error_422 = False
        try:
            body = request.get_json()

            groupname = body.get('groupname', None)

            if groupname is None:
                error_422 = True
                abort(422)

            if groupname is "":
                error_422 = True
                abort(422)

            group = Group(group_name=groupname)

            group_id = group.insert()
            print(group_id)

            selection = Group.query.order_by('id').all()
            current_groups = pagination(request, selection)

            return jsonify({
                'success': True,
                'created': group_id,
                'groups': current_groups,
                'total_groups': len(selection)
            })
        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            else:
                abort(500)

    @app.route('/groups', methods=['GET'])
    def get_groups():
        error_404 = False
        try:
            groups = [group.format() for group in Group.query.order_by("id").all()]

            if len(groups) == 0:
                error_404 = True
                abort(404)

            return jsonify({
                'success': True,
                'grupos': groups,
                'total_groups': len(groups)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)

    @app.route('/groups/<int:group_id>', methods=['DELETE'])
    def delete_group(group_id):
        error_404 = False
        try:
            group = Group.query.filter(Group.id == group_id).one_or_none()
            if group is None:
                error_404 = True
                abort(404)

            group.delete()

            selection = Group.query.order_by('id').all()
            groups = pagination(request, selection)

            return jsonify({
                "success": True,
                "deleted": group_id,
                "groups": groups,
                "total_groups": len(selection)
            })

        except Exception as e:
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/groups/<group_id>', methods=['PATCH'])
    def update_group(group_id):
        error_404 = False
        try:
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if group is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'groupname' in body:
                group.group_name = body.get('groupname')

            group.update()

            return jsonify({
                'success': True,
                'id': group_id
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* POSTS
    @app.route('/posts', methods=['POST'])
    def create_post():
        body = request.get_json()
        user_id = body.get('user_id', None)
        group_id = body.get('group_id', None)
        title = body.get('title', None)
        content = body.get('content', None)

        user = User.query.filter(User.id == user_id).one_or_none()
        group = Group.query.filter(Group.id == group_id).one_or_none()

        if title is None or content is None:
            abort(422)

        if user is None or group is None:
            abort(404)

        if title is "" or content is "":
            abort(422)

        if user is "" or group is "":
            abort(404)

        post = Post(title=title, content=content,
                    user_id=user_id, group_id=group_id)

        post_id = post.insert()

        selection = Post.query.filter(
            Post.group_id == group_id and Post.user_id == user_id).order_by('id').all()
        current_posts = pagination(
            request=request, selection=selection, decreasing=True)
        return jsonify({
            'success': True,
            'id': post_id,
            'posts': current_posts,
            'created': post_id
        })

    @app.route('/posts', methods=['GET'])
    def get_posts():
        user_id = request.args.get('user_id', None, type=int)
        user = User.query.filter(User.id == user_id).one_or_none()

        group_id = request.args.get('group_id', None, type=int)
        group = Group.query.filter(Group.id == group_id).one_or_none()

        if (user_id is not None and user is None) or (group_id is not None and group is None):
            abort(404)

        #* Obtener posts en un grupo
        if user_id is None and group_id is not None:
            selection = Post.query.filter(
                Post.group_id == group_id).order_by('id').all()
        #* Obtener posts de una persona
        elif group_id is None and user_id is not None:
            selection = Post.query.filter(
                Post.user_id == user_id).order_by('id').all()
        #* Obtener posts de un usuario en un grupo
        elif group_id is not None and user_id is not None:
            selection = Post.query.filter(
                Post.user_id == user_id and Post.group_id == group_id).order_by('id').all()
        #* Obtener todos los posts
        elif group_id is None and user_id is None:
            selection = Post.query.order_by('id').all()

        posts = pagination(
            request=request, selection=selection, decreasing=True)
        posts2 = pagination(request, selection)

        if len(posts) == 0 or len(posts2) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'posts': posts,
            'amount_posts': len(selection)
        })

    @app.route('/posts/<int:post_id>', methods=['PATCH'])
    def update_post(post_id):
        error_404 = False
        try:
            post = Post.query.filter(Post.id == post_id).one_or_none()

            if post is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'title' in body:
                post.title = body.get('title')
            if 'content' in body:
                post.content = body.get('content')
            post.update()

            return jsonify({
                'success': True,
                'id': post_id
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    def delete_post(post_id):
        error_404 = False
        try:
            post = Post.query.filter(Post.id == post_id).one_or_none()

            if post is None:
                error_404 = True
                abort(404)

            post.delete()

            selection = Post.query.order_by('id').all()
            current_posts = pagination(
                request=request, selection=selection, decreasing=True)

            return jsonify({
                'success': True,
                'id': post_id,
                'posts': current_posts,
                'amount_posts': len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #TODO
    #* UNIR USUARIOS A GRUPOS
    @app.route('/user/<int:user_id>/group/<int:group_id>', methods=['POST'])
    def join_user_group(user_id, group_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if user is None or group is None:
                error_404 = True
                abort(404)

            groupuser = GroupUser(user_id=user_id, group_id=group_id)
            groupuser.insert()

            return jsonify({
                'success': True
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* BORRAR USUARIOS DE UN GRUPO
    @app.route('/group/<int:group_id>/user/<int:user_id>', methods=['DELETE'])
    def delete_user_from_group(group_id, user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if user is None or group is None:
                error_404 = True
                abort(404)

            groupuser = GroupUser.query.filter(
                GroupUser.user_id == user_id and GroupUser.group_id == group_id).one_or_none()
            groupuser.delete()

            return jsonify({
                'success': True
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/groupusers', methods=['GET'])
    def get_groupusers():
        selection = GroupUser.query.order_by('user_id').all()
        groupusers = pagination(request, selection)

        if len(groupusers) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'groupusers': groupusers,
            'total_groupusers': len(selection)
        })

    @app.route('/group/<group_id>/user/<user_id>', methods=['PATCH'])
    def update_group_user(group_id, user_id):
        error_404 = False
        try:
            gropuser = GroupUser.query.filter(
                GroupUser.user_id == user_id).one_or_none()

            if gropuser is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'group_id' in body:
                group_new_id = body.get('group_id')
                gropuser.group_id = body.get('group_id')

            gropuser.update()

            return jsonify({
                'success': True,
                'id': group_new_id
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    # ! ERROR HANDLERS

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server error'
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    @app.route('/')
    def index():
        return "Insider's blog API"

    return app
