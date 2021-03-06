import copy
from enum import IntEnum
from Models.Product import Product
import datetime


class OrderStatus(IntEnum):
    NEW = 1
    PAID = 2
    SENT = 3
    DELIVERED = 4

    @staticmethod
    def to_string(status):
        if status == OrderStatus.NEW:
            return "NEW"
        elif status == OrderStatus.PAID:
            return "PAID"
        elif status == OrderStatus.SENT:
            return "SENT"
        elif status == OrderStatus.DELIVERED:
            return "DELIVERED"
        else:
            return None


class Order:
    def __init__(self, id, owner_login, creation_date, status, products):
        self.id = id
        self.owner = owner_login
        self.creation_date = creation_date
        self.status = status
        self.products = products

    @staticmethod
    def is_equal(order1, order2):
        if order1.id == order2.id:
            return True
        return False

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        for i in range(len(self.products)):
            if Product.is_equal(self.products[i], product):
                del self.products[i]
                return

    def change_status_to(self, new_status):
        if int(new_status) - int(self.status) == 1 and self.status != OrderStatus.NEW:
            self.status = new_status
            return True
        else:
            return False

    def next_status(self):
        return OrderStatus(int(self.status) + 1) if self.status != OrderStatus.DELIVERED else OrderStatus.DELIVERED

    def __str__(self):
        return f"###Order### Id: '{self.id}'. Owner: {self.owner}. Creation Date: '{self.creation_date}'. Status: '{OrderStatus.to_string(self.status)}'. Products: '{'|'.join(map(str, self.products))}'"

    def __repr__(self):
        return self.__str__()

    def db_representation(self):
        return f"{str(self.id)};{str(self.owner)};{self.creation_date.strftime('%d.%m.%Y')};{str(int(self.status))};{' '.join([str(x.id) for x in self.products])}"
