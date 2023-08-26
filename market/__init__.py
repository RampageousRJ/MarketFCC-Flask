from flask import Flask,render_template,current_app
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='12157649e3719b0c0238a865'
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LcyAbAnAAAAAGj1ZLz7ZqWVCqBuZAlvzLWS9pRK"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LcyAbAnAAAAAPXGV_OzjOXHWvxu6ocLeO3XR7VV"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager=LoginManager(app)

from market import routes