from flask import (
    Flask,
    abort,
    jsonify,
    request
)
from flask_cors import CORS, cross_origin
from models import setup_db, User, Post, Group, GroupUser

POSTS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*POSTS_PER_PAGE
    end = start + POSTS_PER_PAGE
    elements = [element.format() for element in selection]
    current_elements = elements[start:end]
    return current_elements

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app, origins=['http://127.0.0.1:50001'], max_age=10)

    @app.after_request
    def after_resquest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    #Obtener todos los posts
    @app.route('/posts', methods=['GET'])
    def get_posts():
        selection = Post.query.order_by('date_posted').all()
        posts = paginate(request, selection)

        if (len(posts) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'posts': posts,
            'total_posts': len(selection)
        })

    @app.route('/users', methods=['GET'])
    def get_users():
        selection = User.query.order_by('id').all()
        users = paginate(request, selection)

        if (len(users) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'users':users,
            'total_users':len(selection)
        })

    #manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    return app