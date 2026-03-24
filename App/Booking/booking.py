import json

class Booking:

    def __init__(self):
        try:
            with open("bookings.json", "r") as file:
                self.bookings = json.load(file)
        except:
            self.bookings = []

    def book_table(self):

        print("\n----- Table Booking -----")

        name = input("Customer Name: ")
        table_no = input("Table Number: ")
        date = input("Booking Date: ")
        time = input("Booking Time: ")
        booking_data = {
            "name": name,
            "table": table_no,
            "date": date,
            "time": time
        }

        self.bookings.append(booking_data)

        with open("bookings.json", "w") as file:
            json.dump(self.bookings, file, indent=4)

        print("Table booked successfully")

    def view_bookings(self):

        print("\n----- All Bookings -----")

        for booking in self.bookings:
            print(f"Name: {booking['name']}")
            print(f"Table: {booking['table']}")
            print(f"Date: {booking['date']}")
            print(f"Time: {booking['time']}")
            print("--------------------")
            