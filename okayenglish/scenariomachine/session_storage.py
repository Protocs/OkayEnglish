class SessionStorage(dict):
    """Хранилище данных сессии.

    Представляет из себя словарь, к которому можно обращаться и через "[]", и через ".".
    """

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, item):
        if hasattr(self, item):
            super().__delattr__(item)
        else:
            del self[item]
