TYPICAL_RESPONSE = {
    "session": None,
    "version": None,
    "response": {"end_session": False},
}


class RequestParser(dict):
    def __init__(self, request_json):
        super().__init__(request_json)

    def get_session(self):
        return self.get("session")

    def get_version(self):
        return self.get("version")

    def get_text(self):
        return self.get("request").get("original_utterance")


class ResponseParser(dict):
    def __init__(self, request: RequestParser):
        super().__init__()
        for k, v in TYPICAL_RESPONSE.items():
            if k in ("session", "version"):
                self[k] = request.get(k)
            else:
                self[k] = v

    def set_reply_text(self, text):
        self["response"]["text"] = text
