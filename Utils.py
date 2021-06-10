from sys import platform

ORDERS_PATH = "./Bin/orders_db.txt"
PRODUCTS_PATH = "./Bin/products_db.txt"
USERS_PATH = "./Bin/users_db.txt"


def get_operating_system():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "osx"
    elif platform == "win32":
        return "windows"
    else:
        return "windows"