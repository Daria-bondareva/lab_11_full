from . import db
from flask_login import UserMixin

# UserMixin додає Flask-Login поля (is_authenticated, etc.)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # У реальному житті це треба хешувати!

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))