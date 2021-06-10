from Models import *
from Models.Order import OrderStatus
from Utils import *
import datetime


class Manager:
    def __init__(self):
        self.current_user = None

    @staticmethod
    def read_users():
        users = list()
        with open(USERS_PATH) as file:
            lines = file.readlines()
            for line in lines:
                user = Manager.parse_user(line)
                if user is not None:
                    users.append(user)
        return users

    @staticmethod
    def read_products():
        products = list()
        with open(PRODUCTS_PATH) as file:
            lines = file.readlines()
            for line in lines:
                product = Manager.parse_product(line)
                if product is not None:
                    products.append(product)
        return products

    @staticmethod
    def read_orders():
        orders = list()
        with open(ORDERS_PATH) as file:
            lines = file.readlines()
            for line in lines:
                order = Manager.parse_order(line)
                if order is not None:
                    orders.append(order)
        return orders

    @staticmethod
    def parse_product(line):
        line = line.replace("\n", "")
        splitted = line.split(";")
        if len(splitted) < 4:
            return None
        else:
            id = int(splitted[0])
            name = splitted[1]
            price = int(splitted[2])
            amount = int(splitted[3])
            return Product(id, name, price, amount)

    @staticmethod
    def parse_user(line):
        line = line.replace("\n", "")
        splitted = line.split(";")
        if len(splitted) < 3:
            return None
        else:
            name = splitted[0]
            login = splitted[1]
            password = splitted[2]
            return User(name, login, password)

    @staticmethod
    def parse_order(line):
        line = line.replace("\n", "")
        splitted = line.split(";")
        if len(splitted) < 5:
            return None
        else:
            id = int(splitted[0])
            owner = splitted[1]
            creation_date = datetime.datetime.strptime(splitted[2], "%d.%m.%Y").date()
            status = OrderStatus(int(splitted[3]))
            products = [Manager.product_from_id(int(product)) for product in splitted[4].split()]
            return Order(id, owner, creation_date, status, products)

    @staticmethod
    def product_from_id(id):
        products = Manager.read_products()
        similar = [x for x in products if x.id == id]
        if len(similar) > 0:
            return similar[0]
        else:
            return None

    def login(self, login, password):
        users = Manager.read_users()
        needed = [user for user in users if user.login == login]
        if len(needed) > 0:
            if needed[0].sign_in(password):
                self.current_user = needed[0]
                return True
            else:
                raise Exception("Wrong password!")
        else:
            raise Exception("No such a user!")

    @staticmethod
    def create_record(object):
        path = ""
        record = ""
        if isinstance(object, User):
            path = USERS_PATH
            record = object.db_representation()
        elif isinstance(object, Product):
            path = PRODUCTS_PATH
            record = object.db_representation()
        elif isinstance(object, Product):
            path = ORDERS_PATH
            record = object.db_representation()
        else:
            return
        with open(path, "a") as file:
            file.write(record+"\n")

    def register(self, login, name, password):
        users = self.read_users()
        similar = [user for user in users if user.login == login]
        if len(similar) > 0:
            raise Exception("Already a user with such a login!")
        else:
            if User.check_password(password):
                real_password = User.encode(password)
                user = User(name, login, real_password)
                self.create_record(user)
                return True
            else:
                raise Exception("Strange password!")

    # TODO
    def save(self, object):
        pass


