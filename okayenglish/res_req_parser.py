TYPICAL_RESPONSE = {
    "session": None,
    "version": None,
    "response": {"end_session": False},
}


class RequestParser(dict):
    def __init__(self, request_json):
        super().__init__(request_json)

    @property
    def session(self):
        return self.get("session")

    @property
    def version(self):
        return self.get("version")

    @property
    def text(self):
        return self["request"].get("original_utterance")


class ResponseParser(dict):
    def __init__(self, request: RequestParser):
        super().__init__()
        for k, v in TYPICAL_RESPONSE.items():
            if k in ("session", "version"):
                self[k] = request.get(k)
            else:
                self[k] = v

    @property
    def reply_text(self):
        return self["response"]["text"]

    @reply_text.setter
    def reply_text(self, new_text):
        self["response"]["text"] = new_text
