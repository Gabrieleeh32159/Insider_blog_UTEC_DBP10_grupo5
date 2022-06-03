from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

database_name = "proyecto"
username = 'postgres'
password = 'gabrieleeh32159'
database_path = f"postgresql://{username}:{password}@{'localhost:5432'}/{database_name}"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    description = db.Column(db.Text, default='')
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    groups = db.relationship('Group', secondary='group_user', lazy = True)

    '''
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=300):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'email': self.email,
            'image_file': self.image_file,
            'password':self.password,
            'posts':[post.format() for post in self.posts]
        }

# __ex__ <- are called dunder methods (shows how the object is printed )
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

    #El post puede debe haber sido publicado en algún grupo. Por defecto este será el grupo 1. General. 
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False, default=0) 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_posted': self.date_posted,
            'content': self.content,
            'user_id': self.user_id,
            'group_id': self.group_id
        }
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key = True)
    group_name = db.Column(db.String(30), unique = True, nullable = False)
    members = db.relationship('User', secondary = 'group_user', lazy = True)
    posts = db.relationship('Post', backref = 'posts', lazy = True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'group_name': self.group_name
        }

class GroupUser(db.Model):
    __tablename__ = 'group_user'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key = True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True) 