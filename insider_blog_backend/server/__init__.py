from sre_constants import SUCCESS
from flask import (
    Flask,
    abort,
    jsonify,
    request
)
from flask_cors import CORS
from models import setup_db, User, Post, GroupUser, Group
import base64

default_image = base64.b64encode(open('server/imagenes/default.jpg', 'rb').read()).decode('utf-8')

items_per_page = 5

def pagination(request, selection, decreasing = False):
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
    else: 
        start = (page - 1)*items_per_page
        end = (start + items_per_page)
    items = [item.format() for item in selection]
    current = items[start:end]
    return current

def encriptar(palabra):
    return base64.b64encode(palabra.encode('UTF-8'))

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app,origin=['https://utec.edu.pe'], max_age=10)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,OPTIONS')
        return response
    
    #*USERS

    @app.route('/users', methods=['GET'])
    def get_users():
        selection = User.query.order_by('id').all()
        users = pagination(request, selection)

        if len(users) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'users': users,
            'amount_users': len(selection)
        })

    @app.route('/users', methods=['POST'])
    def create_user():
        body = request.get_json()

        username = body.get('username', None)
        description = body.get('description', '')
        email = body.get('email',None)
        password = body.get('password',None)
        image = body.get('image', default_image)

        if username is None or email is None or password is None:
            abort(422)

        user = User(username=username, description = description, email=email, password=encriptar(password), image_file = image)

        user.insert()
        new_user_id = user.id
        group_user = GroupUser(group_id = 0, user_id = new_user_id)
        group_user.insert()

        selection = User.query.order_by('id').all()
        current_users = pagination(request, selection, True)

        return jsonify({
            'success':True,
            'created':new_user_id,
            'users': current_users,
            'total_users': len(selection)
        })

    @app.route('/users/<user_id>', methods=['PATCH'])
    def update_user(user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id==user_id).one_or_none()

            if user is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'username' in body:
                user.username = body.get('username')
            if 'email' in body:
                user.email = body.get('email')
            if 'password' in body:
                user.password = body.get('password')
            if 'description' in body:
                user.description = body.get('description')
            if 'image' in body:
                user.image_file = body.get('image')

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
                "success":True,
                "deleted":user_id,
                "todos":users,
                "total_todos":len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* GROUPS

    @app.route('/groups', methods=['POST'])
    def create_group():
        body = request.get_json()

        groupname = body.get('groupname', None)

        if groupname is None:
            abort(422)

        group = Group(group_name=groupname)

        group.insert()
        new_user_id = group.id

        selection = Group.query.order_by('id').all()
        current_groups = pagination(request, selection)

        return jsonify({
            'success':True,
            'created':new_user_id,
            'groups': current_groups,
            'total_groups': len(selection)
        })

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
            print(group.id)
            if group is None:
                error_404 = True
                abort(404)

            group.delete()

            selection = Group.query.order_by('id').all()
            groups = pagination(request, selection)

            return jsonify({
                "success":True,
                "deleted":group_id,
                "groups":groups,
                "total_groups":len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/groups/<group_id>', methods=['PATCH'])
    def update_group(group_id):
        error_404 = False
        try:
            group = Group.query.filter(Group.id==group_id).one_or_none()

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
        error_404 = False
        try:
            body = request.get_json()
            user_id = body.get('user_id')
            group_id = body.get('group_id')

            user = User.query.filter(User.id==user_id).one_or_none()
            group = Group.query.filter(Group.id==group_id).one_or_none()
            
            if user is None or group is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            title = body.get('title', None)
            content = body.get('content', None)

            if title is None or content is None:
                error_404 = True
                abort(404)

            post = Post(title=title, content=content, user_id=user_id, group_id=group_id)

            post_id = post.insert()

            selection = Post.query.filter(Post.group_id == group_id and Post.user_id == user_id).order_by('id').all()
            current_posts = pagination(request=request, selection=selection, decreasing=True)
            return jsonify({
                'success': True,
                'id': post_id,
                'posts': current_posts
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/posts', methods=['GET'])
    def get_posts():
        error_404 = False
        try:
            user_id = request.args.get('user_id', None, type=int)
            user = User.query.filter(User.id==user_id).one_or_none()

            group_id = request.args.get('group_id', None, type=int)
            group = Group.query.filter(Group.id==group_id).one_or_none()

            if (user_id is not None and user is None) or (group_id is not None and group is None): 
                error_404 = True
                abort(404)
            
            #* Obtener posts en un grupo
            if user_id is None and group_id is not None:
                selection = Post.query.filter(Post.group_id==group_id).order_by('id').all()
            #* Obtener posts de una persona
            elif group_id is None and user_id is not None:
                selection = Post.query.filter(Post.user_id==user_id).order_by('id').all()
            #* Obtener posts de un usuario en un grupo
            elif group_id is not None and user_id is not None:
                selection = Post.query.filter(Post.user_id==user_id and Post.group_id==group_id).order_by('id').all()
            #* Obtener todos los posts
            elif group_id is None and user_id is None:
                selection = Post.query.order_by('id').all()
            
            if len(selection) == 0:
                error_404 = True
                abort(404)

            posts = pagination(request=request, selection=selection)

            return jsonify({
            'success': True,
            'posts': posts,
            'amount_posts': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/posts/<int:post_id>', methods=['PATCH'])
    def update_post(post_id):
        error_404 = False
        try:
            post = Post.query.filter(Post.id==post_id).one_or_none()

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
            post = Post.query.filter(Post.id==post_id).one_or_none()

            if post is None:
                error_404 = True
                abort(404)

            post.delete()

            selection = Post.query.order_by('id').all()
            current_posts = pagination(request=request, selection=selection, decreasing=True)

            return jsonify({
                'success': True,
                'id': post_id,
                'posts': current_posts,
                'amonunt_posts': len(selection)
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

            groupuser = GroupUser(user_id = user_id, group_id = group_id)
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

            groupuser = GroupUser.query.filter(GroupUser.user_id == user_id and GroupUser.group_id == group_id).one_or_none()
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


    @app.route('/')
    def index():
        return "Insider's blog API"

    return app