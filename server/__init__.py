from flask import (
    Flask,
    abort,
    jsonify,
    request
)
from flask_cors import CORS
from models import setup_db, User, Post, GroupUser, Group

items_per_page = 5

def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*items_per_page
    end = start + items_per_page
    users = [user.format() for user in selection]
    current_users = users[start:end]

    return current_users

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app,origin=['https://utec.edu.pe'], max_age=10)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,OPTIONS')
        return response
    
    @app.route('/users', methods=['GET'])
    def get_users():
        selection = User.query.order_by('id').all()
        users = pagination(request, selection)

        if len(users) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'users': users,
            'amount_users': len(users)
        })

    @app.route('/users', methods=['POST'])
    def create_user():
        body = request.get_json()

        username = body.get('username', None)
        email = body.get('email',None)
        password = body.get('password',None)

        user = User(username=username, email=email, password=password)
        new_user_id = user.id

        selection = User.query.order_by('id').all()
        current_users = pagination(request, selection)

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

    @app.route('/groups', methods=['GET'])
    def get_groups():
        error_404 = False
        try:
            groups = {group.id: {'id': group.id, 'name': group.group_name} for group in Group.query.order_by("id").all()}

            if len(groups) == 0:
                error_404 = True
                abort(404)

            return jsonify({
                'success': True,
                'lists': groups,
                'total_lists': len(groups)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)

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