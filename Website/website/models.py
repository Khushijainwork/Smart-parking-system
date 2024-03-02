from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from website import db, login_manager

class User(UserMixin, db.Model):
    """ Table for user information """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # Warn if password not passed through
    @property
    def password(self):
        raise AttributeError('Password is not readable')

    # Generate and store password hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class ParkingBay(db.Model):
    """ Table for parking bay information """
    id = db.Column(db.Integer, primary_key=True)
    bay_id = db.Column(db.String(32), unique=True, nullable=False)
    bay_type = db.Column(db.String(32), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.bay_id}', '{self.bay_type}', '{self.status}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))