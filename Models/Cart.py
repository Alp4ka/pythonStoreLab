import Manager


class Cart:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.products = dict()

    def add_product(self, product):
        #id -> amount
        if self.products.get(product.id, None):
            self.products[product.id] += 1
        else:
            self.products[product.id] = 1

    def remove_product(self, product):
        if self.products.get(product.id, None):
            if self.products[product.id] <= 1:
                del self.products[product.id]
            else:
                self.products[product.id] -= 1

    def convert(self):
        all_products = Manager.Manager.read_products()
        result = list()
        for id, amount in self.products.items():
            for p in all_products:
                if p.id == id:
                    result.extend([p for x in range(amount)])
                    break

        return result


