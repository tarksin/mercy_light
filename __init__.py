# __init__.py
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import pymysql
from wtforms import (StringField, SubmitField, IntegerField, BooleanField,
                    DateTimeField, RadioField,SelectField, TextField, TextAreaField)
from wtforms.validators import DataRequired
from  mercy_light.forms import AddNutrientForm, OrganismForm, DelNutrientForm, SignupForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

login_manager = LoginManager()

# bcrypt = Bcrypt()
# password_hash = bcrypt.generate_password_hash(pw_in)
# check_isOK = bcrypt.check_password_hash(pw_hash, pw_in)

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maxx:xnynzn987@localhost:3306/nutrition'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '84db222b-431f-4461-bef9-914b7671fb4c'

db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = 'login'
