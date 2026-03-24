import json
class Booking_table:
    def __init__(self):
        self.tables={
            "T1": 2,
            "T2": 2,
            "T3": 4,
            "T4": 4,
            "T5": 5,
            "T6": 6
        }

        try:
            with open("bookings.json","r") as file:
                self.bookings=json.load(file)

        except:
            self.bookings=[]


    def show_available_tables(self,date,time):

        booked_tables=[]

        for booking in self.bookings:
            if booking["date"] == date and booking["time"] == time:
                booked_tables.append(booking["table"])

        print("\nAvailable Tables")

        for table,seats in self.tables.items():
            if table not in booked_tables:
                print(f"{table} ({seats} seats)")


    def book_table(self):

        print("\n-------TABLE BOOKING-----------")  

        name=input("Customer Name:") 
        date=input("Booking date:")
        time=input("Booking Time:")

        self.show_available_tables(date,time)

        table_no=input("Select table Number:")

        booking_data={
            "name": name,
            "table": table_no,
            "date": date,
            "time": time 
        } 

        self.bookings.append(booking_data)       

        with open("bookings.json","w") as file:
            json.dump(self.bookings, file, indent=4)

        print("Table Booked Successfully")


    def view_booking(self):

        print("\n-----All Bookings--------")

        for booking in self.bookings:
            print(f"Name: {booking['name']}")
            print(f"Table: {booking['table']}")
            print(f"Date: {booking['date']}")
            print(f"Time: {booking['time']}")
            print("--------------------------")
                         
booking=Booking_table()

booking.book_table()
booking.view_booking()

