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
    menu_view()


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
    if pressed == '1':
        register_view()
    elif pressed == '2':
        login_view()
    else:
        exit()


def main():
    global manager
    manager = Manager()
    menu_view()

main()