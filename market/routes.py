from market import app
from flask import render_template,redirect,url_for,flash
from market.models import Item,User
from market.forms import RegisterForm,LoginForm
from market import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.order_by(Item.id.asc()).all()
    return render_template('market.html',items=items)

@app.route('/register',methods=['GET','POST'])
def register():
    regform = RegisterForm()
    if regform.validate_on_submit():
        new_user = User(username=regform.username.data,
                        email=regform.email.data,
                        password=regform.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if regform.errors != {}:
        for error_msg in regform.errors.values():
            flash(error_msg[0], category='danger')
    return render_template('register.html',form=regform)    

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        potential_user = User.query.filter_by(username=form.username.data).first()
        if potential_user and potential_user.check_password_correction(attempted_password=form.password.data):
            login_user(potential_user)
            flash(f"Logged in as {potential_user}",category='success')
            return redirect(url_for('market_page'))
        flash("Invalid Credentials",category='danger')
    return render_template('login.html',form=form)

@app.errorhandler(404)
def not_found(e):
    flash('Page not found: Redirected to home page',category='danger')
    return redirect(url_for('home'))