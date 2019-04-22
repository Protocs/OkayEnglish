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
    training_type = db.Column(db.String(22), nullable=False)

db.create_all()

def get_user_stats(user_id, training_type):
    stats = TrainingStats.query.filter_by(user_id=user_id, training_type=training_type).all()
    return stats
