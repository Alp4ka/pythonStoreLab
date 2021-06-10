class Product:
    def __init__(self, id, name, price, amount=0):
        self.id = id
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

    def __str__(self):
        return f"###Product### Id: {self.id}. Name: '{self.name}'. Price: '{self.price}'. Amount: '{self.amount}'"

    def __repr__(self):
        return self.__str__()

    def db_representation(self):
        return f"{self.id};{self.name};{self.price};{self.amount}"
