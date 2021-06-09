import hashlib


class User:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    @staticmethod
    def is_equal(user1, user2):
        if user1.name == user2.name and \
                user1.login == user2.login and \
                user1.password == user2.password:
            return True
        return False

    @staticmethod
    def check_password(data):
        if 7 < len(data) < 40:
            return True
        return False

    def login(self, password):
        if self.encode(password) == self.password:
            return True
        return False

    # Encode string via md5 algorithm.
    def encode(self, data):
        hash_object = hashlib.md5(data.encode())
        return hash_object.hexdigest()
