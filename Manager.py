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
            price = float(splitted[2])
            amount = int(splitted[3])
            return Product(id, name, price, amount)

    @staticmethod
    def parse_user(line):
        line = line.replace("\n", "")
        splitted = line.split(";")
        if len(splitted) < 3:
            return None
        else:
            id = splitted[0]
            name = splitted[1]
            login = splitted[2]
            password = splitted[3]
            return User(id, name, login, password)

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
            products = [Manager.product_from_id(int(product))
                        for product in splitted[4].split()]
            return Order(id, owner, creation_date, status, products)

    @staticmethod
    def product_from_id(id):
        products = Manager.read_products()
        similar = [x for x in products if x.id == id]
        if len(similar) > 0:
            return similar[0]
        else:
            return None

    def pay_order(self, order):
        order_products = order.products
        if self.check_decrease_ability(order_products):
            self.decrease_products(order_products)
            order.status = OrderStatus.PAID
            self.save_record(order)
            return True
        else:
            return False

    def decrease_products(self, order_products):
        storage_products = Manager.read_products()
        d = pList_to_dict(order_products)
        for sproduct in storage_products:
            if sproduct.id in d.keys():
                if d[sproduct.id] <= sproduct.amount:
                    sproduct.amount -= d[sproduct.id]
                    self.save_record(sproduct)

    def check_decrease_ability(self, order_products):
        storage_products = Manager.read_products()
        d = pList_to_dict(order_products)
        for sproduct in storage_products:
            if sproduct.id in d.keys():
                if d[sproduct.id] > sproduct.amount:
                    return False

        return True





    def make_order(self):
        # Убедиться что товара на складе долстаочно
        all_products = Manager.read_products()
        if self.current_user is not None:
            cart = self.current_user.cart
            if len(cart.products.keys()) == 0 :
                return False
            for product_id, amount in cart.products.items():
                for it in all_products:
                    if it.id == product_id:
                        if it.amount < amount:
                            return False
                        break
            converted = cart.convert()
            orders = Manager.read_orders()
            today = datetime.datetime.today()
            new_order= Order(id=len(orders)+1,
                             owner_login=self.current_user.login,
                             creation_date=today,
                             status=OrderStatus.NEW,
                             products=converted)
            Manager.create_record(new_order)
            self.current_user.cart = Cart(self.current_user.id)
            return True

    def add_to_cart(self, product):
        if self.current_user is not None:
            self.current_user.cart.add_product(product)

    def remove_from_cart(self, product):
        if self.current_user is not None:
            self.current_user.cart.remove_product(product)

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
        elif isinstance(object, Product):
            path = PRODUCTS_PATH
        elif isinstance(object, Order):
            path = ORDERS_PATH
        else:
            return
        record = object.db_representation()
        with open(path, "a") as file:
            file.write(record + "\n")

    def register(self, login, name, password):
        users = self.read_users()
        similar = [user for user in users if user.login == login]
        new_id = len(users)+1
        if len(similar) > 0:
            raise Exception("Already a user with such a login!")
        else:
            if User.check_password(password):
                real_password = User.encode(password)
                user = User(new_id, name, login, real_password)
                self.create_record(user)
                return True
            else:
                raise Exception("Strange password!")

    @staticmethod
    def save_record(object):
        path = ""
        records = ""
        if isinstance(object, User):
            path = USERS_PATH
            records = Manager.read_users()
        elif isinstance(object, Product):
            path = PRODUCTS_PATH
            records = Manager.read_products()
        elif isinstance(object, Order):
            path = ORDERS_PATH
            records = Manager.read_orders()
        else:
            return
        for i in range(len(records)):
            if object.is_equal(records[i], object):
                records[i] = object
                with open(path, 'w') as f:
                    f.write('')
                break
        for record in records:
            Manager.create_record(record)
