from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import join, abspath, dirname

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F3HUIF23H8923F9H8389FHXKLN'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)