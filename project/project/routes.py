

from flask import abort, render_template, request, url_for, redirect, flash
from project import app, db, bcrypt
from project.forms import RegisterationForm, LoginForm
from project.models import User, Order
from flask_login import current_user, login_user, logout_user, login_required
import subprocess
import json
from datetime import datetime
from is_safe_url import is_safe_url

orders = []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('حساب کاربری شما ساخته شد', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect (next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('ورود ناموفق! لطفا ایمیل و نام کاربری خود را دوباره بررسی کنید')
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/profile', methods=["POST"])
def profile_post():
    Brokerage = request.form.get('brokerage')
    Username = request.form.get('uname')
    Password = request.form.get('password')
    Namad = request.form.get('namad')
    Quantity = request.form.get('quantity')
    Minqueue = request.form.get('minqueue')
    Minratio = request.form.get('minratio')
    Robot = request.form.get('robot')
    Starttime = request.form.get('starttime')
    Stoptime = request.form.get('stoptime')
    data = json.dumps({"Brokerage":Brokerage, "Username": Username, "Password": Password, "Namad": Namad,
    "Quantity":Quantity, "Minqueue":Minqueue, "Minratio": Minratio, "Robot": Robot, "Starttime": Starttime, "Stoptime": Stoptime,
    })
    order = Order(namad=Namad, quantity=Quantity, status='running', user_id=current_user.id, time_submited=datetime.now())
    db.session.add(order)
    db.session.commit()
    # os.system("python3 sell.py '{}'".format(data))
    with open('output.txt', 'a') as f:
        with open('error.txt', 'a') as g:
            p1 = subprocess.run(["python3 sell.py {}".format(data)], stdout=f, stderr=g, text=True, shell=True)
    data = {
            "time" : datetime.now().time(),
            "username":Username,
            "namad":Namad,
            "quantity":Quantity,
            "robot":Robot,

    }
    
    orders.append(data)    

    return render_template('history.html',orders=orders)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/history')
def history():
    logout_user()
    return render_template('history.html')