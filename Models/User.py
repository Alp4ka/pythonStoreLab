import hashlib
from Utils import *
from Models.Order import OrderStatus
from Models.Cart import Cart
import Manager


class User:
    def __init__(self, id, name, login, password):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.cart = Cart(id)

    def get_orders(self):
        orders = Manager.Manager.read_orders()
        my_orders = [order for order in orders if order.owner == self.login]
        return my_orders

    def get_active(self):
        result = [order for order in self.get_orders() if order.status == OrderStatus.NEW]
        return result

    def __str__(self):
        return f"###User### Id: '{self.id}'. Login: '{self.login}' Name: '{self.name}'"

    def __repr__(self):
        return self.__str__ + " Password: '{self.password}'"

    def db_representation(self):
        return f"{self.id};{self.name};{self.login};{self.password}"

    @staticmethod
    def is_equal(user1, user2):
        if user1.id == user2.id:
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
