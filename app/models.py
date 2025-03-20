from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationships (Cascade delete when user is deleted)
    journals = db.relationship('FarmJournal', backref='user', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='user', lazy=True, cascade="all, delete-orphan")

class FarmJournal(db.Model):
    __tablename__ = 'farm_journal'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50))
    farm_location = db.Column(db.Text)
    sowing_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date)
    yield_amount = db.Column(db.Float, nullable=False) 
    sold_amount = db.Column(db.Float, nullable=False, default=0)  
    unit_price = db.Column(db.Float, nullable=False)  
    total_revenue = db.Column(db.Float, nullable=False, default=0)
    expenses = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def calculate_revenue_and_profit(self):
        self.total_revenue = self.sold_amount * self.unit_price  
        self.profit = self.total_revenue - self.expenses

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.now)  # ✅ Ensure timestamp field exists


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # ✅ Add timestamp field
