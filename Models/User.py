import hashlib
from Utils import *
import Manager


class User:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def get_orders(self):
        orders = Manager.Manager.read_orders()
        my_orders = [order for order in orders if order.owner == self.login]
        return my_orders

    def __str__(self):
        return f"###User### Login: '{self.login}' Name: '{self.name}'"

    def __repr__(self):
        return f"###User### Login: '{self.login}' Name: '{self.name}' Password: '{self.password}'"

    def db_representation(self):
        return f"{self.name};{self.login};{self.password}"

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

    def sign_in(self, password):
        if User.encode(password) == self.password:
            return True
        return False

    # Encode string via md5 algorithm.
    @staticmethod
    def encode(data):
        hash_object = hashlib.md5(data.encode())
        return hash_object.hexdigest()
