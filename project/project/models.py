from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    orders = db.relationship('Order', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namad = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    status = db.Column(db.String(15))
    time_submited = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Order('{self.user_id}','{self.namad}', '{self.date_submited}', '{self.status}')"