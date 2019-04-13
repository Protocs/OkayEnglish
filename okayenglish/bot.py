from flask import Flask
import json

from .res_req_parser import RequestParser, ResponseParser


class Bot:
    """Ядро навыка для приложения ``app``"""

    def __init__(self, app: Flask):
        self.app = app

    def handle_request(self, req_json):
        req = RequestParser(req_json)
        response = ResponseParser(req)

        # Простой эхо-бот.
        response.reply_text = req.text
        return json.dumps(response)
