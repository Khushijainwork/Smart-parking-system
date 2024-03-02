from flask import Flask, render_template, url_for, redirect, flash, session, request, g, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from website import app, db
from website.models import *
from website.forms import *

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from backend.arduino_parking import *

executor = ThreadPoolExecutor(2)
q = Queue()

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ParkingForm()

    # while not q.empty():
    #     result = q.get()
    #     flash(f'Parking duration: {result/360} hours', 'info')

    # when form is submitted, if not logged in, redirect to login page
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please login to reserve a parking bay', 'info')
            return redirect(url_for('login'))

        # create new thread to run arduino, then redirect to home page
        executor.submit(run_arduino, q)
        flash('Parking successful!', 'info')

    return render_template('home.html', title='Car Parking Auto', form=form)

@app.route('/get_result')
def get_result():
    if not q.empty():
        result = q.get()
        result = round(result/60, 2)
        return jsonify(result=result)
    else:
        return '', 404


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if not form.email.data:
            user = User(username=form.username_new.data, password=form.password_new.data)
        else:
            user = User(username=form.username_new.data, password=form.password_new.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash('Signup successful!', 'info')
        return redirect(url_for('registered'))

    return render_template('signup.html', title='Signup', form=form)

@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thanks for joining')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # Logout user if already logged in
            if current_user.is_authenticated:
                logout()

            login_user(user)
            flash("Login successful!", 'info')
            return redirect(request.args.get('next') or url_for('home'))

        flash('Invalid username or password', 'login_error')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    flash("You have logged out successfully", 'info')
    return redirect(url_for('home'))
