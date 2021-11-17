import json
import datetime
import uuid

ADD_TO_PRICE = 5


class Customer:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.visit_day = datetime.datetime.now().weekday()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or value.isdigit():
            raise TypeError("Name must be a string")
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        if not value or not isinstance(value, str) or value.isdigit():
            raise TypeError("Name must be a string")
        self.__surname = value

    @property
    def visit_day(self):
        return self.__visit_day

    @visit_day.setter
    def visit_day(self, value):
        if not isinstance(value, int):
            raise TypeError("Visit day must be a integer")
        self.__visit_day = value

    def __str__(self):
        return f'Customer info: {self.name} {self.surname}'


class Monday:
    def __init__(self):
        with open('pizza.json') as f:
            pizza_data = json.load(f)
        self.day_of_week = "0"
        self.name = pizza_data["pizza-of-the-day"][self.day_of_week]["name"]
        self.price = pizza_data["pizza-of-the-day"][self.day_of_week]["price"]
        self.ingredients = pizza_data["pizza-of-the-day"][self.day_of_week]["ingredients"]

    def __str__(self):
        return f'Name of pizza: {self.name}\nPrice of pizza: {self.price}\n'

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or value.isdigit():
            raise TypeError('Name must be a string')
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Price must be a integer or float')
        if value <= 0:
            raise ValueError('Price must be > 0')
        self.__price = value

    @property
    def day_of_week(self):
        return self.__day_of_week

    @day_of_week.setter
    def day_of_week(self, value):
        if not isinstance(value, str):
            raise TypeError("Day of week must be a string")
        self.__day_of_week = value

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value):
        if not isinstance(value, dict):
            raise TypeError("Ingredients must be an dict")
        self.__ingredients = value


class Tuesday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "1"


class Wednesday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "2"


class Thursday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "3"


class Friday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "4"


class Saturday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "5"


class Sunday(Monday):
    def __init__(self):
        super().__init__()
        self.day_of_week = "6"


class Order:

    def __init__(self, customer, *extra_ingredients):
        self.id = str(uuid.uuid1())
        self.customer = customer
        self.day_of_week = str(customer.visit_day)
        self.extra_ingredients = extra_ingredients

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError('Invalid input data type')
        self.__customer = customer

    @property
    def extra_ingredients(self):
        return self.__extra_ingredients

    @extra_ingredients.setter
    def extra_ingredients(self, value):
        with open('storage.json') as f:
            storage = json.load(f)
        for ingredient in value:
            if storage[ingredient] < 50:
                raise KeyError('There is no such ingredient in storage')
        self.__extra_ingredients = value

    def buy_pizza(self):
        with open("order.json", 'r') as f:
            order = json.load(f)
        with open("storage.json", 'r') as file:
            storage = json.load(file)
        if self.id not in order:
            order[self.id] = {}
            order[self.id]['name'] = self.customer.name
            order[self.id]['surname'] = self.customer.surname
            name_of_day = {"0": Monday(), "1": Tuesday(), "2": Wednesday(), "3": Thursday(), "4": Friday(),
                           "5": Saturday(), "6": Sunday()}
            pizza_obj = name_of_day[self.day_of_week]
            order[self.id]['price'] = pizza_obj.price + len(self.extra_ingredients) * ADD_TO_PRICE
            order[self.id]['pizza_name'] = pizza_obj.name
            order[self.id]['ingredients'] = pizza_obj.ingredients
            for ingredient in self.extra_ingredients:
                if ingredient not in order[self.id]['ingredients']:
                    order[self.id]['ingredients'][ingredient] = 50
                else:
                    order[self.id]['ingredients'][ingredient] += 50
        with open("order.json", 'w') as f:
            json.dump(order, f, indent=4)
        for ingredient in order[self.id]['ingredients']:
            if storage[ingredient] < order[self.id]['ingredients'][ingredient]:
                raise ValueError("Out of ingredients in storage")
            storage[ingredient] -= order[self.id]['ingredients'][ingredient]
        with open("storage.json", 'w') as file:
            json.dump(storage, file, indent=4)
        return f"YOUR ORDER:" \
               f"\nOrder id: {self.id}" \
               f"\nName of customer: {self.customer.name}\nSurname of customer: " \
               f"{self.customer.surname}\nPrice of pizza: {pizza_obj.price}" \
               f"\nPrice of extra ingredients: {len(self.extra_ingredients) * ADD_TO_PRICE}" \
               f"\nName of pizza: {pizza_obj.name}\nIngredients of pizza: {', '.join(pizza_obj.ingredients)}" \
               f"\nExtra ingredients: {', '.join(self.extra_ingredients)}"

    @staticmethod
    def search_ticket(order_id):
        with open("order.json", 'r') as f:
            order = json.load(f)
        if not order_id or not isinstance(order_id, str):
            raise TypeError("Ticket id must be a string")
        if order_id not in order:
            raise KeyError("There is no order with this id in database")
        name = order[order_id]['name']
        surname = order[order_id]['surname']
        price = order[order_id]['price']
        pizza_name = order[order_id]['pizza_name']
        ingredients = order[order_id]['ingredients']
        return f"\n\nORDER YOU SEARCHING FOR:\nOrder id: {order_id}\nName: {name}\nSurname: {surname}\n" \
               f"Price: {price}\nPizza name: {pizza_name}\nIngredients: {', '.join(ingredients)}"


name_of_customer2 = "Stephen"
surname_of_customer2 = "King"
client2 = Customer(name=name_of_customer2, surname=surname_of_customer2)
pizza = Order(client2, "chicken", "pineapple pieces")
print(pizza.buy_pizza())
print(pizza.search_ticket("b12fc815-4792-11ec-8dce-80304949e310"))
