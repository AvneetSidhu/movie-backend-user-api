from enum import unique
from flask import Flask, request
from secret import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

user_movie = db.Table('movie_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    pw = db.Column(db.String(80), unique=False)
    movies = db.relationship('Movie', secondary=user_movie, backref='users')

    def __init__(self, username, password):
        self.username = username  
        self.pw = password
    
    def __repr__(self):
        return '<User %r>' % self.username

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(30),unique=True)

    def __init__(self, movie_id):
        self.movie_id = movie_id
    
    def __repr__(self):
        return '<Movie %r>' % self.movie_id

@app.route("/")
def health():
    print(DB_URI)
    return 'healthy'

@app.route("/add-to-watchlist")
def addToWatchlist():
    return 'healthy'

@app.route("/remove-from-watchlist")
def removeFromWatchlist():
    return 'healthy'

@app.route("/sign-up", methods = ['POST'])
def signUp():
    userdata = request.get_json()
    username = userdata['username']
    password = userdata['password']
    hashedPass = bcrypt.generate_password_hash(password,10).decode('utf-8')
    user = User(username, hashedPass)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return 'error while posting to database', 500

    return 'True', 200
