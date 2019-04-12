from flask import Flask
import json


class Bot:
    """Ядро навыка для приложения ``app``"""

    def __init__(self, app: Flask):
        self.app = app

    def handle_request(self, req):
        return json.dumps({
            "response": {
                "text": "Здравствуйте! Это мы, хороводоведы.",
                "tts": "Здравствуйте! Это мы, хоров+одо в+еды.",
                "buttons": [
                    {
                        "title": "Надпись на кнопке",
                        "payload": {},
                        "url": "https://example.com/",
                        "hide": True
                    }
                ],
                "end_session": False
            },
            "session": {
                "session_id": "2eac4854-fce721f3-b845abba-20d60",
                "message_id": 4,
                "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
            },
            "version": "1.0"
        })
