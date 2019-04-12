from okayenglish.bot import Bot
from flask import Flask, request

app = Flask(__name__)
bot = Bot(app)


@app.route("/post", methods=["POST"])
def get_request():
    return bot.handle_request(request.json)


if __name__ == "__main__":
    app.run()
