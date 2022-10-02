from enum import unique
from flask import Flask, request
from secret import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
users = {ADMIN_USER: generate_password_hash(ADMIN_PASS)}

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

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route("/")
@auth.login_required
def health():           
    return 'healthy'

@app.route("/get-watchlist")
@auth.login_required
def getWatchList():
    userdata = request.get_json()
    if "username" in userdata:
        usernameGiven = userdata['username']
    else:
        return "error: missing required fields", 422

    try:
        user = User.query.filter_by(username=usernameGiven).first()
        movieslist= []
        if user.movies:
            for movie in user.movies:
                movieslist.append(movie.movie_id)
            return json.dumps(movieslist), 200

        return 'user has no movies', 200
    except:
        return 'something went wrong', 500



@app.route("/add-to-watchlist")
@auth.login_required
def addToWatchlist():
    userdata = request.get_json()
    if "username" in userdata and "movie_id" in userdata:
        usernameGiven = userdata['username']
        movieid = userdata['movie_id']
    else:
        return "error: missing required fields", 422
    try:
        user = User.query.filter_by(username=usernameGiven).first()
        existingmovie = Movie.query.filter_by(movie_id=movieid).first()
        if existingmovie:
            print('here')
            user.movies.append(existingmovie)
            db.session.commit()
        else:
            newmovie = Movie(movie_id=movieid)
            db.session.add(newmovie)
            db.session.commit()
            user.movies.append(newmovie)
            db.session.commit()

        return 'movie added successfully', 200
    except:
        return 'something went wrong', 500

@app.route("/remove-from-watchlist")
@auth.login_required
def removeFromWatchlist():
    userdata = request.get_json()
    if "username" in userdata and "movie_id" in userdata:
        usernameGiven = userdata['username']
        movieid = userdata['movie_id']
    else:
        return "error: missing required fields", 422
    try:
        user = User.query.filter_by(username=usernameGiven).first()
        movie = Movie.query.filter_by(movie_id=movieid).first()
        user.movies.remove(movie)
        db.session.commit()
        return 'movie removed successfully', 200
    except:
        return 'something went wrong', 500


@app.route("/sign-up", methods = ['POST'])
@auth.login_required
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

if __name__ == '__main__':
    app.run()