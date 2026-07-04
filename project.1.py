'''
Project: Vehicle Rental System

Problem Statement
You are building a small program for a vehicle rental company.

 Requirements
Create a base  class Vehicle with attributes:brand model And a method show_details() that prints them.

Create a child class Car that inherits from Vehicle.
Extra attribute: seating_capacity
Method rental_price(days) → calculates rental price as days * 1000.
Override show_details() to display seating capacity too.

Create another child class Bike that inherits from Vehicle.
Extra attribute: engine_cc
Method rental_price(days) → calculates rental price as days * 500.
Override show_details() to display engine CC.

Create objects for both Car and Bike, display their details, and calculate rental price for a given number of days.
'''
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def show_details(self):
        print("Brand :", self.brand)
        print("Model :", self.model)

class Car(Vehicle):
    def __init__(self, brand, model, seating):
        super().__init__(brand, model)
        self.seating = seating

    def show_details(self):
        super().show_details()
        print("Seating :", self.seating)

    def rental_price(self, days):
        print("Rental Price :", days * 1000)
class Bike(Vehicle):
    def __init__(self, brand, model, cc):
        super().__init__(brand, model)
        self.cc = cc

    def show_details(self):
        super().show_details()
        print("Engine CC :", self.cc)

    def rental_price(self, days):
        print("Rental Price :", days * 500)

print("1. Car")
print("2. Bike")
choice = input("Enter your choice : ")

if choice == "1":
    brand = input("Enter Brand : ")
    model = input("Enter Model : ")
    seating = int(input("Enter Seating Capacity : "))
    days = int(input("Enter Rental Days : "))

    c = Car(brand, model, seating)
    c.show_details()
    c.rental_price(days)
elif choice == "2":
    brand = input("Enter Brand : ")
    model = input("Enter Model : ")
    cc = int(input("Enter Engine CC : "))
    days = int(input("Enter Rental Days : "))

    b = Bike(brand, model, cc)
    b.show_details()
    b.rental_price(days)

else:
    print("Invalid Choice")
       