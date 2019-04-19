from flask import Flask
import json

from okayenglish.res_req_parser import RequestParser, ResponseParser
from okayenglish.scenariomachine.session import Session


class Bot:
    """Ядро навыка для приложения ``app``"""

    def __init__(self, app: Flask):
        self.app = app
        self._sessions = {}

    def handle_request(self, req_json):
        from okayenglish.db import User, db

        req = RequestParser(req_json)
        response = ResponseParser(req)

        # Создание сессии для нового пользователя
        user_id = req.session["user_id"]
        if user_id not in self._sessions or req.new_session:
            user = User.query.filter_by(user_id=user_id).first()
            if user is None:
                user = User(user_id=req.user_id)
                db.session.add(user)
                db.session.commit()
            self._sessions[user_id] = Session(user)

        session = self._sessions[user_id]
        session.receive(req)
        session.next_state(response)
        session.send(response)

        return json.dumps(response)
