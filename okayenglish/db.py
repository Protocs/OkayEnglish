from datetime import datetime

from okayenglish.app import db


class User(db.Model):
    user_id = db.Column(db.String(64), nullable=False, unique=True, primary_key=True)


class TrainingStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey("user.user_id"))
    date = db.Column(db.DateTime, default=lambda: datetime.now())
    right_answers = db.Column(db.Integer, nullable=False)
    wrong_answers = db.Column(db.Integer, nullable=False)


db.create_all()
