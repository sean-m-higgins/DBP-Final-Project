from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
     __table_args__ = {'extend_existing': True}
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     content = db.Column(db.Text, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     def __repr__(self):
         return f"Post('{self.title}', '{self.date_posted}')"


class Experiment(db.Model):
    __table__ = db.Model.metadata.tables['Experiment']
    
class Project(db.Model):
    __table__ = db.Model.metadata.tables['Project']

class Uses_Reagent(db.Model):
    __table__ = db.Model.metadata.tables['Uses_Reagent']
    
class Employee(db.Model):
    __table__ = db.Model.metadata.tables['Employee']

class Project(db.Model):
    __table__ = db.Model.metadata.tables['Project']

class Reagent(db.Model):
    __table__ = db.Model.metadata.tables['Reagent']

class Product(db.Model):
    __table__ = db.Model.metadata.tables['Product']

class Equipment(db.Model):
    __table__ = db.Model.metadata.tables['Equipment']

class Uses_Equipment(db.Model):
    __table__ = db.Model.metadata.tables['Uses_Equipment']

    

  
