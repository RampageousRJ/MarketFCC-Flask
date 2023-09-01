from market import app
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import *
from market import db
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    form=Purchase()
    if request.method=='POST':
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(name=purchased_item).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.owner = current_user.id
                current_user.budget -= p_item.price
                db.session.commit()
                flash(f'Bravo! You bought {p_item.name}',category='success')
            else:
                flash(f"Unable to buy {p_item.name} due to insufficient budget",category='danger')
            
    if request.method=='GET':
        items = Item.query.order_by(Item.id.asc()).filter_by(owner=None)
        return render_template('market.html',items=items,form=form)
    return render_template('market.html',items=items,form=form)
    

@app.route('/register',methods=['GET','POST'])
def register():
    regform = RegisterForm()
    if regform.validate_on_submit():
        new_user = User(username=regform.username.data,
                        email=regform.email.data,
                        password=regform.password1.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered Successfully! Login to continue',category='success')
        return redirect(url_for('login'))
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

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out successfully!',category='info')
    return redirect(url_for('home'))