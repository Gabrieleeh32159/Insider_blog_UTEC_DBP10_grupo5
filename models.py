from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db_name = "proyecto"
password = os.environ.get('pg_pass')
port = 9173
db_path='postgresql://postgres:{}@localhost:{}/{}'.format(password,port,db_name)

db = SQLAlchemy()

def setup_db(app, database_path=db_path):
    app.config['SQLALCHEMY_DATABASE_URI']=db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()
    print('db setted up! :)')

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

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def format(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

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
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'group_id':self.group_id
        }


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key = True)
    group_name = db.Column(db.String(30), unique = True, nullable = False)
    members = db.relationship('User', secondary = 'group_user', lazy = True)
    posts = db.relationship('Post', backref = 'posts', lazy = True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Id('{self.id}', Group_name'{self.group_name}')"

    def format(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
        }


class GroupUser(db.Model):
    __tablename__ = 'group_user'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key = True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True) 

