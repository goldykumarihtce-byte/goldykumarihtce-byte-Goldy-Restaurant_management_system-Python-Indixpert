

import uuid
from datetime import datetime
from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error

from rich.console import Console
from rich.panel import Panel


class Booking:

    def __init__(self):
        self.db = Data()
        self.handler = ExceptionHandler()
        self.file = "App/Database/booking.json"
        self.console = Console()

        self.tables = {
            "T1": 4, "T2": 6, "T3": 8, "T4": 2, "T5": 4,
            "T6": 2, "T7": 8, "T8": 2, "T9": 4, "T10": 6
        }

        self.table_price = {
            "T1": 100, "T2": 150, "T3": 200, "T4": 120, "T5": 250,
            "T6": 180, "T7": 220, "T8": 130, "T9": 170, "T10": 210
        }

        self.time_slots = {
            "Morning": ["9-11", "11-1"],
            "Afternoon": ["1-3"],
            "Evening": ["3-5"]
        }

    def is_future_slot(self, date, slot):
        now = datetime.now()

        
        if date == now.strftime("%Y-%m-%d"):
            start_hour = int(slot.split("-")[0])
            slot_time = datetime.strptime(f"{start_hour}:00", "%H:%M").time()

            return slot_time > now.time()

        return True    

    def booking_menu(self):
        while True:
            self.console.print(Panel.fit(
                """1. Create Booking 🆕
2. View Booking 📋
3. Cancel Booking ❌
4. Reschedule Booking 🔄
5. Back 🔙""",
                title="TABLE BOOKING DASHBOARD",
                border_style="cyan"
            ))

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.create_booking()
            elif choice == "2":
                
                self.view_booking()
            elif choice == "3":
                self.cancel_booking()
            elif choice == "4":
                self.reschedule_booking()
            elif choice == "5":
                break
            else:
                self.console.print(Panel("[bold red]Invalid choice[/bold red]", title="❌ ERROR"))    



    # ================= CREATE =================
    def create_booking(self):
        try:
            data = self.handler.handle_read(self.db.read_data, self.file)
            if not isinstance(data, list):
                data = []

            while True:

                self.console.print(Panel.fit("🍽 BOOK YOUR TABLE", border_style="cyan"))

                
                while True:
                    name = input("Name: ")
                    if name.isalpha():
                        break
                    print("Invalid name")

                
                while True:
                    phone = input("Phone: ")
                    if phone.isdigit() and len(phone) == 10:
                        break
                    print("Invalid phone")

                
                while True:
                    try:
                        persons = int(input("Persons: "))
                        if persons > 0:
                            break
                    except:
                        pass
                    print("Invalid persons")

                
                while True:
                    date = input("Date (YYYY-MM-DD): ")
                    try:
                        entered = datetime.strptime(date, "%Y-%m-%d")
                        if entered.date() < datetime.now().date():
                            print("Past date not allowed")
                            continue
                        break
                    except:
                        print("Invalid date")

                #  AVAILABLE SLOTS WITH FIX
                available_categories = {}

                for category, slots in self.time_slots.items():
                    free_slots = []

                    for s in slots:

                        if not self.is_future_slot(date, s):
                            continue

                        booked = any(
                            b.get("date") == date and
                            b.get("time") == s and
                            b.get("status") == "Confirmed"
                            for b in data
                        )

                        if not booked:
                            free_slots.append(s)

                    if free_slots:
                        available_categories[category] = free_slots

                if not available_categories:
                    print("No slots available")
                    return

                # CATEGORY
                while True:
                    for i, cat in enumerate(available_categories, 1):
                        print(f"{i}. {cat}")
                    try:
                        choice = int(input("Choose category: "))
                        category = list(available_categories.keys())[choice - 1]
                        slots = available_categories[category]
                        break
                    except:
                        print("Invalid choice")

                # SLOT
                while True:
                    for i, s in enumerate(slots, 1):
                        print(f"{i}. {s}")
                    try:
                        choice = int(input("Choose slot: "))
                        if 1 <= choice <= len(slots):
                            time = slots[choice - 1]
                            break
                    except:
                        pass
                    print("Invalid slot")

                # SEATS
                table_map = {}
                for table, capacity in self.tables.items():
                    free = []
                    for i in range(1, capacity + 1):
                        seat = f"S{i}"
                        booked = any(
                            (table in b.get("table", []) and seat in b.get("sheet", []))
                            and b.get("date") == date
                            and b.get("time") == time
                            for b in data
                        )
                        if not booked:
                            free.append(seat)
                    if free:
                        table_map[table] = free

                if not table_map:
                    print("No seats available")
                    return

                for t, s in table_map.items():
                    print(f"{t} → {', '.join(s)}")

                # SELECT
                selected = []
                selected_set = set()

                while True:
                    table = input("Table: ").upper()

                    if table not in table_map:
                        print("Invalid table")
                        continue

                    seats = input("Seats (S1,S2): ").upper().split(",")

                    valid = all(seat.strip() in table_map[table] for seat in seats)
                    if not valid:
                        print("Invalid seats")
                        continue

                    for s in seats:
                        tup = (table, s.strip())
                        if tup in selected_set:
                            print("Duplicate seat")
                            continue

                        selected.append(tup)
                        selected_set.add(tup)

                    more = input("More? (yes/no): ")
                    if more == "no":
                        break

                if len(selected) != persons:
                    print("Seat mismatch")
                    return

                # PRICE
                total = sum(self.table_price.get(t[0], 0) for t in selected)

                # PAYMENT
                while True:
                    payment = input("Payment (paid/pending): ").lower()
                    if payment in ["paid", "pending"]:
                        break
                    print("Invalid payment")

                
                booking_id = str(uuid.uuid4())[:3]

                booking = {
                    "booking_id": booking_id,
                    "name": name,
                    "phone": phone,
                    "persons": persons,
                    "table": [t[0] for t in selected],
                    "sheet": [t[1] for t in selected],
                    "date": date,
                    "time": time,
                    "amount": total,
                    "payment_status": payment.upper(),
                    "status": "Confirmed"
                }

                data.append(booking)
                self.handler.handle_write(self.db.write_data, self.file, data)

                print(f"Booked! ID: {booking_id}")

                again = input("Again? ")
                if again != "yes":
                    break

        except Exception as e:
            log_error(str(e))

    def view_booking(self):
        try:
            data = self.handler.handle_read(self.db.read_data, self.file)

            if not isinstance(data, list) or not data:
                self.console.print(Panel("[bold red]No bookings found[/bold red]", title="INFO"))
                return

            for b in data:
                details = f"""
    🆔 ID        : {b.get('booking_id')}
    👤 Name      : {b.get('name')}
    📞 Phone     : {b.get('phone')}
    👥 Persons   : {b.get('persons')}
    📅 Date      : {b.get('date')}
    🕒 Time      : {b.get('time')}
    💰 Amount    : ₹{b.get('amount')}
    💳 Payment   : {b.get('payment_status')}
    📌 Status    : {b.get('status')}
    """
                self.console.print(Panel(details, title="📋 BOOKING DETAILS", border_style="blue"))

        except Exception as e:
            log_error(str(e))
            self.console.print(Panel("[red]Error loading bookings[/red]", title="❌ ERROR"))
                
                

    
    def cancel_booking(self):
        data = self.handler.handle_read(self.db.read_data, self.file)

        bid = input("Enter Booking ID: ").strip()

        found = next(
            (b for b in data if str(b.get("booking_id")) == bid),
            None
        )

        if not found:
            print("Not found")
            return

        if found.get("status") == "Cancelled":
            print("Already cancelled")
            return

        found["status"] = "Cancelled"
        self.handler.handle_write(self.db.write_data, self.file, data)

        print("Cancelled successfully")


    def reschedule_booking(self):
        data = self.handler.handle_read(self.db.read_data, self.file)

        bid = input("Enter Booking ID: ")

        found = next((b for b in data if str(b.get("booking_id")) == bid), None)

        if not found:
            print("Not found")
            return

        for i, cat in enumerate(self.time_slots, 1):
            print(f"{i}. {cat}")

        choice = int(input("Choose: "))
        category = list(self.time_slots.keys())[choice - 1]

        slots = self.time_slots[category]

        for i, s in enumerate(slots, 1):
            print(f"{i}. {s}")

        choice = int(input("Slot: "))
        found["time"] = slots[choice - 1]

        self.handler.handle_write(self.db.write_data, self.file, data)

        print("Rescheduled")



