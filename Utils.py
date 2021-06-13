from sys import platform
import os

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


def clear_screen():
    global operating_system
    if operating_system == "windows":
        os.system('cls')
    else:
        os.system('clear')


def pList_to_dict(products_list):
    result = dict()
    for i in range(len(products_list)):
        if products_list[i].id in result.keys():
            result[products_list[i].id] += 1
        else:
            result[products_list[i].id] = 1
    return result


operating_system = get_operating_system()