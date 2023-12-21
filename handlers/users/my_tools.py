
class ShoppingCart:
    def __init__(self):
        self.products = []

    def get_total_price(self):
        total = 0
        for i in self.products:
            total += i['quantity'] * i['price']
        return total

    def plus_quantity(self, name):
        for i in self.products:
            if i['id'] == name:
                i['quantity'] += 1

    def minus_quantity(self, name):
        for i in self.products:
            if i['id'] == name:
                if i['quantity'] > 1:
                    i['quantity'] -= 1
                else:
                    self.products.remove(i)

    def add_product(self, id, name, price):
        for i in self.products:
            if i['name'] == name:
                i['quantity'] += 1
                return
        int_price = ''
        for i in str(price)[:-2]:
            if i.isdigit():
                int_price += i
        self.products.append(dict(
            name=name,
            price=int(int_price),
            quantity=1,
            id=id
        ))

    def clear(self):
        self.products.clear()

