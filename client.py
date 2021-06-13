from Manager import Manager
from Models.Order import OrderStatus
import Models
from Utils import *


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
                input("<'Enter' to continue>")
            else:
                break
        name = ""
        while True:
            name = input("Enter your name: ")
            name = name.strip()
            if len(name) < 3:
                print("I need more than 3 symbols!")
                input("<'Enter' to continue>")
            else:
                break
        password = ""
        while True:
            password = input("Enter your password: ")
            password = password.strip()
            if not Models.User.check_password(password):
                print("I need more than 7 symbols!")
                input("<'Enter' to continue>")
            else:
                break
        try:
            response = manager.register(login, name, password)
        except Exception as ex:
            print(ex)
            response = False
            input("<'Enter' to continue>")
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
            input("<'Enter' to continue>")
    print(f"Logged in as {manager.current_user}")
    input("<'Enter' to continue>")
    logged_menu()


def menu_view():
    while True:
        clear_screen()
        print("-------Main Menu\n1. Sign Up\n2. Sign In\n3. Exit")
        values = ['1', '2', '3']
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
        if pressed == '1':
            register_view()
        elif pressed == '2':
            login_view()
        else:
            exit()


def shop_view():
    global manager
    while True:
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
                input("<'Enter' to continue>")
        pressed = int(pressed)
        if pressed == len(products)+1:
            logged_menu()
        elif pressed == len(products):
            if manager.make_order():
                print("Order confirmed!")
            else:
                print("Something went wrong:c")
            input("<'Enter' to continue>")
            logged_menu()
        else:
            product_chosen = products[pressed]
            manager.add_to_cart(product_chosen)
            print(f"{product_chosen} added to cart!")
            input("<'Enter' to continue>")


def orders_view():
    global manager
    clear_screen()
    print(f"-------My Orders ({manager.current_user.login})")
    print("HINT: press a number of order you want to observe.")
    my_orders = manager.current_user.get_orders()
    values = [str(x) for x in range(len(my_orders) + 1)]
    for i in range(len(my_orders)):
        print(f"{values[i]}. {my_orders[i]}")
    print(f"{values[-1]}. Exit")
    pressed = None
    while pressed is None:
        pressed = input()
        if pressed not in values:
            pressed = None
            print("No such an item:c")
            input("<'Enter' to continue>")
    pressed = int(pressed)
    if pressed == len(my_orders):
        logged_menu()
    else:
        order_chosen = my_orders[pressed]
        order_view(order_chosen)


def order_view(order):
    while True:
        global manager
        clear_screen()
        print(f"-------Order #{order.id}")
        print("HINT: input number of product and '-'/'+' to select whether you want to remove or add a product.")
        print("EXAMPLE: 1 +")
        products = order.products
        keys = dict()

        values = [str(x) for x in range(len(products) + 2)]

        for i in range(len(products)):
            print(f"{values[i]}. {products[i]}")

        print(f"{values[-2]}. Pay")
        print(f"{values[-1]}. Exit")
        pressed = None
        action = None
        while pressed is None:
            data = input().split()
            pressed = data[0]
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
            elif pressed != values[-1] and pressed != values[-2]:
                if len(data) != 2:
                    pressed = None
                    print("I need two arguments:c")
                    input("<'Enter' to continue>")
                else:
                    if data[1]  in ['+', '-']:
                        action = data[1]
                    else:
                        pressed = None
                        print("Wrong action:c")
                        input("<'Enter' to continue>")

        pressed = int(pressed)
        if pressed == len(values) - 1:
            orders_view()
        elif pressed == len(values) - 2:
            if order.status == OrderStatus.NEW:
                if manager.pay_order(order):
                    print("Success!")
                    input("<'Enter' to continue>")
                else:
                    print("Sorry. You are not able to pay for this order:( \nThere are no some products in out storage...")
                    input("<'Enter' to continue>")
            else:
                print("Order is already paid!")
                input("<'Enter' to continue>")
        else:
            if order.status == OrderStatus.NEW:
                chosen_product = products[pressed]
                if action == '+':
                    order.add_product(chosen_product)
                    print(f"{chosen_product} added!")
                    input("<'Enter' to continue>")
                else:
                    if len(order.products) == 1:
                        print("Zakaz uzhe sdelan. Plati shekeli:c")
                        input("<'Enter' to continue>")
                        continue
                    order.remove_product(chosen_product)
                    print(f"{chosen_product} removed!")
                    input("<'Enter' to continue>")
                manager.save_record(order)

            else:
                print("You can't edit this order:c")
                input("<'Enter' to continue>")


def cart_view():
    global manager
    while True:
        clear_screen()
        print(f"-------My Cart ({manager.current_user.login})")
        print("HINT: press a number of product you want to remove from cart.")
        my_products = manager.current_user.cart.convert()
        values = [str(x) for x in range(len(my_products) + 2)]
        for i in range(len(my_products)):
            print(f"{values[i]}. {my_products[i]}")
        print(f"{values[-2]}. Confirm")
        print(f"{values[-1]}. Exit")
        pressed = None
        while pressed is None:
            pressed = input()
            if pressed not in values:
                pressed = None
                print("No such an item:c")
                input("<'Enter' to continue>")
        pressed = int(pressed)
        if pressed == len(my_products)+1:
            logged_menu()
        elif pressed == len(my_products):
            if manager.make_order():
                print("Order confirmed!")
            else:
                print("Something went wrong:c")
            input("<'Enter' to continue>")
            logged_menu()
        else:
            product_chosen = my_products[pressed]
            manager.remove_from_cart(product_chosen)
            print(f"{product_chosen} removed from cart!")


def logged_menu():
    global manager
    clear_screen()
    print(f"-------Menu ({manager.current_user.login})\n1. Shop\n2. My Orders\n3. Cart\n4. Exit")
    values = ['1', '2', '3', '4']
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
    elif pressed == '3':
        cart_view()
    else:
        exit()


def main():
    global manager
    manager = Manager()
    menu_view()

main()