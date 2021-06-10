import copy
from enum import Enum


class OrderStatus(Enum):
    NEW = 1
    PAID = 2
    SENT = 3
    DELIVERED = 4


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

    def __str__(self):
        return f"###Order### Id: '{self.id}'. Owner: {self.owner}. Creation Date: '{self.creation_date}'. Status: '{self.status}'. Products: '{'|'.join(map(str, self.products))}'"

    def __repr__(self):
        return self.__str__()

    def db_representation(self):
        return f"{self.id};{self.owner}{self.creation_date};{int(self.status)};{' '.join([x.id for x in self.products])}"
