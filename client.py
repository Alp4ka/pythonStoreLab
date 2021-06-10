from Manager import Manager
import os
import Models
from Utils import *


operating_system = get_operating_system()
manager = None


def register_view():
    global manager
    response = False
    while not response:
        clear_screen()
        print("-------Registration")
        login = ""
        while True:
            login = input("Enter your login: ")
            login = login.strip()
            if len(login) < 3:
                print("I need more than 3 symbols!")
            else:
                break
        name = ""
        while True:
            name = input("Enter your name: ")
            name = name.strip()
            if len(name) < 3:
                print("I need more than 3 symbols!")
            else:
                break
        password = ""
        while True:
            password = input("Enter your password: ")
            password = password.strip()
            if not Models.User.check_password(password):
                print("I need more than 7 symbols!")
            else:
                break
        try:
            response = manager.register(login, name, password)
        except Exception as ex:
            print(ex)
            response = False
    menu_view()


def login_view():
    global manager
    response = False
    while not response:
        clear_screen()
        print("-------Log In")
        login = input("Enter your login: ")
        login = login.strip()

        password = input("Enter your password: ")
        password = password.strip()
        try:
            response = manager.login(login, password)
        except Exception as ex:
            print(ex)
            response = False
    print(f"Logged in as {manager.current_user}")
    input("<Any key to continue>")
    logged_menu()


def clear_screen():
    global operating_system
    if operating_system == "windows":
        os.system('cls')
    else:
        os.system('clear')


def menu_view():
    clear_screen()
    print("-------Main Menu\n1. Sign Up\n2. Sign In\n3. Exit")
    values = ['1', '2', '3']
    pressed = None
    while pressed is None:
        pressed = input()
        if pressed not in values:
            pressed = None
            print("No such an item:c")
    if pressed == '1':
        register_view()
    elif pressed == '2':
        login_view()
    else:
        exit()

#TODO
def shop_view():
    global manager
    clear_screen()
    print(f"-------Shop ({manager.current_user.login})")
    products = [product for product in manager.read_products() if product.amount > 0]
    values = [str(x) for x in range(len(products)+2)]
    for i in range(len(products)):
        print(f"{values[i]}. {products[i]}")
    print(f"{values[-2]}. Confirm")
    print(f"{values[-1]}. Exit")
    pressed = None
    while pressed is None:
        pressed = input()
        if pressed not in values:
            pressed = None
            print("No such an item:c")

def orders_view():
    pass

def cart_view():
    pass


def logged_menu():
    global manager
    clear_screen()
    print(f"-------Menu ({manager.current_user.login})\n1. Shop\n2. My Orders\n3.  Cart")
    values = ['1', '2', '3']
    pressed = None
    while pressed is None:
        pressed = input()
        if pressed not in values:
            pressed = None
            print("No such an item:c")
    if pressed == '1':
        shop_view()
    elif pressed == '2':
        orders_view()
    else:
        cart_view()


def main():
    global manager
    manager = Manager()
    menu_view()

main()