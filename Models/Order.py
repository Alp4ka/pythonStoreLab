import copy
from enum import Enum


class OrderStatus(Enum):
    NEW = 1
    PAID = 2
    SENT = 3
    DELIVERED = 4


class Order:
    def __init__(self, id, creation_date, status, products):
        self.id = id
        self.creation_date = creation_date
        self.status = status
        self.products = copy.deepcopy(products)

    @staticmethod
    def is_equal(order1, order2):
        if order1.id == order2.id and \
                order1.creation_date == order2.creation_date and \
                order1.status == order2.status:
            return True
        return False

