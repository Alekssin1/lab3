import json
import uuid
import datetime
from sales import SALES_ADVANCED, SALES_LATE, SALES_STUDENT


class Customer:
    def __init__(self, name, surname, student_or_not):
        self.name = name
        self.surname = surname
        self.student_or_not = student_or_not

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
    def student_or_not(self):
        return self.__student_or_not

    @student_or_not.setter
    def student_or_not(self, value):
        if not isinstance(value, bool):
            raise TypeError("Student_or_not must be a boolean")
        self.__student_or_not = value


class Regular:
    def __init__(self):
        self.id = uuid.uuid1()
        with open("event.json", 'r') as f:
            event = json.load(f)
        self.price = event['event']['type_of_ticket']['regular']

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not value or not isinstance(value, (float, int)):
            raise TypeError("Price must be a number")
        self.__price = round(value, 2)


class Advanced(Regular):

    def __init__(self):

        super().__init__()
        with open("event.json", 'r') as f:
            event = json.load(f)
            self.price = event['event']['type_of_ticket']['regular'] * SALES_ADVANCED
            event['event']['type_of_ticket']['advanced'] = self.price
        with open('event.json', 'w') as f:
            json.dump(event, f, indent=4)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not value or not isinstance(value, (float, int)):
            raise TypeError("Price must be a number")
        self.__price = round(value, 2)


class Late(Regular):
    def __init__(self):
        super().__init__()
        with open("event.json", 'r') as f:
            event = json.load(f)
            self.price = event['event']['type_of_ticket']['regular'] * SALES_LATE
            event['event']['type_of_ticket']['late'] = self.price
        with open('event.json', 'w') as f:
            json.dump(event, f, indent=4)


class Student(Regular):
    def __init__(self):
        super().__init__()
        with open("event.json", 'r') as f:
            event = json.load(f)
            self.price = event['event']['type_of_ticket']['regular'] * SALES_STUDENT
            event['event']['type_of_ticket']['student'] = self.price
        with open('event.json', 'w') as f:
            json.dump(event, f, indent=4)


class UserInfo:
    def __init__(self, customer, ticket):
        self.customer = customer
        self.ticket = ticket
        self.datetime = str(datetime.datetime.now())
        with open("database.json", 'r') as f:
            database = json.load(f)
        if 'event' not in database:
            database['event'] = {}
        if not str(self.ticket.id) in database['event']:
            database['event'][str(self.ticket.id)] = {}
            database['event'][str(self.ticket.id)]['name'] = self.customer.name
            database['event'][str(self.ticket.id)]['surname'] = self.customer.surname
            database['event'][str(self.ticket.id)]['price'] = self.ticket.price
            database['event'][str(self.ticket.id)]['purchase_date'] = self.datetime
        with open("database.json", 'w') as f:
            json.dump(database, f, indent=4)

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value):
        if not value or not isinstance(value, Customer):
            raise TypeError("Customer must be a Customer object")
        self.__customer = value

    @property
    def ticket(self):
        return self.__ticket

    @ticket.setter
    def ticket(self, value):
        if not value or not isinstance(value, (Regular, Advanced, Late, Student)):
            raise TypeError("Ticket must be a one type of ticket.")
        self.__ticket = value

    def __str__(self):
        return f"Ticket id: {str(self.ticket.id)}\nName: {self.customer.name}\nSurname: {self.customer.surname}\n" \
               f"Price: {self.ticket.price}\nPurchase date: {self.datetime}\nSAVE THIS TICKET! " \
               f"U NEED ID TO FIND IT IN THIS SITE!"


class Event:
    def __init__(self):
        with open("event.json", 'r') as f:
            event = json.load(f)
        self.date = datetime.datetime(*list(event["event"]["date"]))
        self.ticket_regular = Regular()
        self.ticket_student = Student()
        self.ticket_advanced = Advanced()
        self.ticket_late = Late()

    def show_tickets_price(self):
        date_delta = (self.date - datetime.datetime.now()).days
        if date_delta < 0:
            return f"Time to buy tickets is up. Event ended."
        with open("event.json", 'r') as f:
            event = json.load(f)
        if date_delta > 60:
            return f"You can buy ticket now for {event['event']['type_of_ticket']['advanced']}$\nPrice for students " \
                   f"{event['event']['type_of_ticket']['student']}$\n{event['event']['number_of_tickets']}" \
                   f" tickets left\n\n"
        elif 0 <= date_delta < 10:
            return f"You can buy ticket now for {event['event']['type_of_ticket']['late']}$\nPrice for students " \
                   f"{event['event']['type_of_ticket']['student']}$\n{event['event']['number_of_tickets']}" \
                   f" tickets left\n\n"
        else:
            return f"You can buy ticket now for {event['event']['type_of_ticket']['regular']}$\nPrice for students " \
                   f"{event['event']['type_of_ticket']['student']}$\n{event['event']['number_of_tickets']}" \
                   f" tickets left\n\n"

    def buy_ticket(self, customer: Customer):
        with open("event.json", 'r') as f:
            event = json.load(f)
        if event["event"]["number_of_tickets"] <= 0:
            raise ValueError("Tickets sold out!")
        date_delta = (self.date - datetime.datetime.now()).days
        if date_delta < 0:
            raise TimeoutError("Time to buy tickets is up. Event ended.")
        event["event"]["number_of_tickets"] -= 1
        with open("event.json", 'w') as f:
            json.dump(event, f, indent=4)
        if customer.student_or_not:
            return self.ticket_student
        elif date_delta > 60:
            return self.ticket_advanced
        elif 0 <= date_delta < 10:
            return self.ticket_late
        else:
            return self.ticket_regular

    @staticmethod
    def search_ticket(ticket_id):
        with open("database.json", 'r') as f:
            database = json.load(f)
        if not ticket_id or not isinstance(ticket_id, str):
            raise TypeError("Ticket id must be a string")
        if "event" not in database:
            raise KeyError("There is no events in database")
        if ticket_id not in database["event"]:
            raise KeyError("There is no tickets in database")
        name = database["event"][ticket_id]["name"]
        surname = database["event"][ticket_id]["surname"]
        price = database["event"][ticket_id]["price"]
        date = database["event"][ticket_id]["purchase_date"]
        return f"YOUR TICKET:\nTicket id: {ticket_id}\nName: {name}\nSurname: {surname}\n" \
               f"Price: {price}\nPurchase date: {date}"


# name_of_customer = input("Enter your name:")
# surname_of_customer = input("Enter your surname:")
event = Event()
(print(event.show_tickets_price()))

name_of_customer1 = "Phoenix"
surname_of_customer1 = "Hoking"
client1 = Customer(name=name_of_customer1, surname=surname_of_customer1, student_or_not=False)
ticket1 = event.buy_ticket(client1)
client_ticket1 = UserInfo(client1, ticket1)
print(client_ticket1, "\n\n")

name_of_customer2 = "Stephen"
surname_of_customer2 = "King"
client2 = Customer(name=name_of_customer2, surname=surname_of_customer2, student_or_not=True)
ticket2 = event.buy_ticket(client2)
client_ticket2 = UserInfo(client2, ticket2)
print(client_ticket2, "\n\n")

print(event.search_ticket("7146289d-41f8-11ec-99b2-80304949e310"))
