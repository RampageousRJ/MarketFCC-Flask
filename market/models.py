from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer,nullable=False,default=20000)
    items = db.relationship('Item',backref='owner')
    
    def __repr__(self):
        return f"{self.username}"        
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text):
        self.password_hash=bcrypt.generate_password_hash(plain_text).decode('utf-8')
        
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
    

class Item(db.Model):
    __tablename__='item'
    id=db.Column(db.String(length=7),nullable=False,primary_key=True)
    name=db.Column(db.String(length=30),nullable=False)
    price=db.Column(db.Float(),nullable=False)
    description=db.Column(db.String(length=1024))
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
    
# http://flask-login.readthedocs.io/#how-it-works