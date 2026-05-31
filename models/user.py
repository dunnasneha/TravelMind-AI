from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    preferred_language = db.Column(db.String(20), default='English')
    travel_style = db.Column(db.String(50), default='Balanced')
    
    trips = db.relationship('Trip', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}')"
