from Manager import *
from Models.Order import OrderStatus
import os
import Models
from Utils import *

manager = None


def product_view(product):
    global manager
    while True:
        clear_screen()
        print(f"-------Product #{product.id} {product.name} (Admin)")
        print(product)
        values = ['1', '2', '3']
        print("1. Edit quantity")
        print("2. Edit price")
        print("3. Exit")
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
        pressed = int(pressed)
        if pressed == 1:
            quantity_view(product)
            return
        elif pressed == 2:
            price_view(product)
            return
        else:
            storage_view()
            return


def quantity_view(product):
    global manager
    while True:
        clear_screen()
        print(f"-------Product #{product.id} {product.name} Quantity (Admin)")
        print(product.__repr__())
        print("HINT: Type an integer>=0 to change the quantity of selected product.")
        value = input()
        try:
            numeric = int(value)
            if numeric < 0:
                raise Exception("Numeric should be more than zero.")
            product.amount = numeric
            Manager.save_record(product)
            product_view(product)
            return
        except:
            print("Strange number:c")
            input("<'Enter' to continue>")
            continue


def price_view(product):
    global manager
    while True:
        clear_screen()
        print(f"-------Product #{product.id} {product.name} Price (Admin)")
        print(product)
        print("HINT: Type a float number >=0.0 to change the price of selected product.")
        value = input()
        try:
            numeric = float(value)
            if numeric < 0:
                raise Exception("Numeric should be more than zero.")
            product.price = numeric
            Manager.save_record(product)
            product_view(product)
            return
        except:
            print("Strange number:c")
            input("<'Enter' to continue>")
            continue


def storage_view():
    global manager
    while True:
        clear_screen()
        print(f"-------Storage (Admin)")
        products = manager.read_products()
        values = [str(x) for x in range(len(products) + 1)]
        for i in range(len(products)):
            print(f"{values[i]}. {products[i].__repr__()}")
        print(f"{values[-1]}. Exit")
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
        pressed = int(pressed)
        if pressed == len(values) - 1:
            menu_view()
            return
        else:
            product = products[pressed]
            product_view(product)
            return


def orders_view():
    global manager
    while True:
        clear_screen()
        print(f"-------Orders (Admin)")
        orders = sorted(manager.read_orders(), key=lambda x: x.status)
        orders = sorted(orders, key=lambda x: x.creation_date)
        values = [str(x) for x in range(len(orders)+1)]
        for i in range(len(orders)):
            print(f"{values[i]}. {orders[i]}")
        print(f"{values[-1]}. Exit")
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
                continue
        pressed = int(pressed)
        if pressed == len(values) - 1:
            menu_view()
            return
        else:
            order = orders[pressed]
            order_view(order)
            return


def order_view(order):
    global manager
    while True:
        clear_screen()
        print(f"-------Order #{order.id} (Admin)")
        values = ['1', '2']
        print(f"1. Switch to status {OrderStatus.to_string(order.next_status())}")
        print("2. Exit")
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
                continue
        pressed = int(pressed)
        if pressed == 1:
            if order.change_status_to(order.next_status()):
                print("Success!")
                input("<'Enter' to continue>")
                manager.save_record(order)
                orders_view()
                return
            else:
                print("You are not able to change status:c")
                input("<'Enter' to continue>")
                order_view(order)
                return
        elif pressed == 2:
            orders_view()
            return


def menu_view():
    while True:
        clear_screen()
        print("-------Main Menu (Admin)\n1. Storage\n2. Orders\n3. Exit")
        values = ['1', '2', '3']
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
        if pressed == '1':
            storage_view()
            return
        elif pressed == '2':
            orders_view()
            return
        else:
            return

def main():
    global manager
    manager = Manager()
    menu_view()
    return

main()