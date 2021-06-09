class Product:
    def __init__(self, name, price, amount=0):
        self.name = name
        self.price = price
        self.amount = amount

    @staticmethod
    def is_equal(product1, product2):
        if product1.name == product2.name and \
                product1.price == product2.price and \
                product1.amount == product2.amount:
            return True
        return False

