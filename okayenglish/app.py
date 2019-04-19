from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from okayenglish.config import DATABASE_URI, TRACK_MODIFICATIONS

from okayenglish.bot import Bot

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TRACK_MODIFICATIONS
db = SQLAlchemy(app)
bot = Bot(app)


@app.route("/post", methods=["POST"])
def get_request():
    return bot.handle_request(request.json)
