


from datetime import datetime, timedelta
from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


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

    # ================= MENU =================
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

                self.console.print(Panel.fit(
                    "[bold yellow]🍽 BOOK YOUR TABLE[/bold yellow]",
                    border_style="cyan"
                ))

                name = input("👤 Enter Name: ")
                phone = input("📞 Enter Mobile No: ")
                persons = int(input("👥 Enter Persons: "))
                date = input("📅 Enter Date (YYYY-MM-DD): ")

                # 🔥 AVAILABLE CATEGORIES
                available_categories = {}
                for category, slots in self.time_slots.items():
                    free_slots = [
                        s for s in slots
                        if not any(
                            b.get("date") == date and
                            b.get("time") == s and
                            b.get("status") == "Confirmed"
                            for b in data
                        )
                    ]
                    if free_slots:
                        available_categories[category] = free_slots

                if not available_categories:
                    self.console.print(Panel("[bold red]No slots available[/bold red]", title="❌ ERROR"))
                    return

                cat_text = "\n".join([f"{i}. {cat}" for i, cat in enumerate(available_categories, 1)])
                self.console.print(Panel(cat_text, title="⏰ Time Categories", border_style="blue"))

                while True:
                    try:
                        choice = int(input("👉 Enter choice: "))
                        category = list(available_categories.keys())[choice - 1]
                        available_slots = available_categories[category]
                        break
                    except:
                        self.console.print(Panel("[red]Invalid choice[/red]", title="❌ ERROR"))

                slot_text = "\n".join([f"{i}. {s}" for i, s in enumerate(available_slots, 1)])
                self.console.print(Panel(slot_text, title=f"{category} Slots", border_style="magenta"))

                while True:
                    try:
                        choice = int(input("👉 Select Slot: "))
                        if 1 <= choice <= len(available_slots):
                            time = available_slots[choice - 1]
                            break
                    except:
                        pass
                    self.console.print(Panel("[red]Invalid choice[/red]", title="❌ ERROR"))

                # 🔥 AVAILABLE SEATS
                table_map = {}

                for table, capacity in self.tables.items():
                    free_seats = []

                    for i in range(1, capacity + 1):
                        seat = f"S{i}"

                        booked = any(
                            (table in b.get("table", []) and seat in b.get("sheet", []))
                            and b.get("date") == date
                            and b.get("time") == time
                            and b.get("status") == "Confirmed"
                            for b in data
                        )

                        if not booked:
                            free_seats.append(seat)

                    if free_seats:
                        table_map[table] = free_seats

                if not table_map:
                    self.console.print(Panel("[red]No seats available[/red]", title="❌ ERROR"))
                    return

                table_text = "\n".join(
                    [f"{t} → {', '.join(s)}" for t, s in table_map.items()]
                )

                self.console.print(Panel(table_text, title="💺 Available Tables & Seats", border_style="magenta"))

                # 🔥 USER SELECT
                selected = []

                while True:
                    table = input("👉 Enter Table (e.g., T1): ").upper()

                    if table not in table_map:
                        self.console.print(Panel("[red]Invalid Table[/red]", title="❌ ERROR"))
                        continue

                    seats_input = input("👉 Enter Seats (S1,S2): ").upper().split(",")

                    valid = all(seat.strip() in table_map[table] for seat in seats_input)

                    if not valid:
                        self.console.print(Panel("[red]Invalid seats[/red]", title="❌ ERROR"))
                        continue

                    for s in seats_input:
                        selected.append((table, s.strip()))

                    more = input("Add more seats? (yes/no): ").lower()
                    if more != "yes":
                        break

                if len(selected) != persons:
                    self.console.print(Panel("[bold red]Seats must match persons[/bold red]", title="❌ ERROR"))
                    return

                # 💰 PRICE
                total = sum(self.table_price.get(t[0], 0) for t in selected)
                booking_id = len(data) + 1

                # 🔥 GROUP VIEW
                table_group = {}
                for t, s in selected:
                    table_group.setdefault(t, []).append(s)

                selected_text = "\n".join(
                    [f"{t} → {', '.join(s)}" for t, s in table_group.items()]
                )

                self.console.print(Panel(selected_text, title="✅ Selected Seats", border_style="green"))

                summary = f"""
👤 Name     : {name}
📞 Phone    : {phone}
👥 Persons  : {persons}
📅 Date     : {date}
🕒 Time     : {time}
💰 Amount   : ₹{total}
"""
                self.console.print(Panel(summary, title="📋 BOOKING SUMMARY", border_style="cyan"))

                confirm = input("👉 Confirm Booking? (yes/no): ").lower()
                if confirm != "yes":
                    self.console.print(Panel("[yellow]Cancelled[/yellow]", title="INFO"))
                    return

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
                    "status": "Confirmed"
                }

                data.append(booking)
                self.handler.handle_write(self.db.write_data, self.file, data)

                self.console.print(Panel(f"""
🎉 Booking Confirmed!

🆔 Booking ID : {booking_id}
👤 Name       : {name}
📅 Date       : {date}
🕒 Time       : {time}
💰 Amount     : ₹{total}
""", title="✅ SUCCESS", border_style="green"))

                again = input("\n👉 Do you want to book another table? (yes/no): ").lower()
                if again != "yes":
                    break

        except Exception as e:
            log_error(str(e))
            self.console.print(Panel("[bold red]Booking Error[/bold red]", title="❌ ERROR"))

    # ================= VIEW =================
    def view_booking(self):
        try:
            data = self.handler.handle_read(self.db.read_data, self.file)

            if not data:
                self.console.print(Panel("[bold red]No bookings found[/bold red]", title="INFO"))
                return

            for b in data:
                table = Table(title=f"📋 Booking ID: {b.get('booking_id')}", show_lines=True)

                table.add_column("Field", style="cyan")
                table.add_column("Details", style="green")

                tables = b.get("table", [])
                seats = b.get("sheet", [])

                if tables and seats:
                    table_map = {}
                    for t, s in zip(tables, seats):
                        table_map.setdefault(t, []).append(s)
                    table_text = "\n".join([f"{t} → {', '.join(s)}" for t, s in table_map.items()])
                else:
                    table_text = "Not Assigned"

                table.add_row("👤 Name", str(b.get("name")))
                table.add_row("📞 Phone", str(b.get("phone")))
                table.add_row("📅 Date", str(b.get("date")))
                table.add_row("🕒 Time", str(b.get("time")))
                table.add_row("🍽 Tables", table_text)
                table.add_row("💰 Amount", f"₹{b.get('amount')}")
                table.add_row("📌 Status", str(b.get("status")))

                self.console.print(Panel(table, border_style="blue"))

        except Exception as e:
            log_error(str(e))
            self.console.print(Panel("[bold red]Error loading bookings[/bold red]", title="❌ ERROR"))   

    def cancel_booking(self):
        try:
            data = self.handler.handle_read(self.db.read_data, self.file)

            if not isinstance(data, list) or not data:
                self.console.print(Panel("[bold yellow]No bookings available[/bold yellow]", title="INFO"))
                return

            bid = input("Enter Booking ID to cancel: ").strip()

            if not bid.isdigit():
                self.console.print(Panel("[bold red]Invalid Booking ID[/bold red]", title="ERROR"))
                return

            bid = int(bid)

            found = next((b for b in data if b.get("booking_id") == bid), None)

            if not found:
                self.console.print(Panel("[bold red]Booking not found[/bold red]", title="ERROR"))
                return

            # 🔥 Already cancelled check
            if found.get("status", "").lower() == "cancelled":
                self.console.print(Panel("[yellow]Booking already cancelled[/yellow]", title="INFO"))
                return

            # 🔥 Confirm cancel
            confirm = input("Are you sure you want to cancel? (yes/no): ").lower()

            if confirm != "yes":
                self.console.print(Panel("[yellow]Cancellation aborted[/yellow]", title="INFO"))
                return

            # 🔥 Update status
            found["status"] = "Cancelled"

            # ✅ Proper save using handler
            self.handler.handle_write(self.db.write_data, self.file, data)

            # 🔥 Success panel
            self.console.print(
                Panel(
                    f"[bold red]Booking ID {bid} cancelled successfully ❌[/bold red]",
                    title="CANCELLED",
                    border_style="red"
                )
            )

        except Exception as e:
            log_error(f"Cancel Booking Error: {e}")
            self.console.print(Panel("[bold red]Error cancelling booking[/bold red]", title="ERROR"))




    def reschedule_booking(self):
        try:
            data = self.handler.handle_read(self.db.read_data, self.file)

            if not isinstance(data, list) or not data:
                self.console.print(Panel("[bold yellow]No bookings available[/bold yellow]", title="INFO"))
                return

            bid = input("Enter Booking ID to reschedule: ").strip()

            if not bid.isdigit():
                self.console.print(Panel("[bold red]Invalid Booking ID[/bold red]", title="ERROR"))
                return

            bid = int(bid)

            found = next(
                (b for b in data if b.get("booking_id") == bid and b.get("status") == "Confirmed"),
                None
            )

            if not found:
                self.console.print(Panel("[bold red]Booking not found or already cancelled[/bold red]", title="ERROR"))
                return

            # 🔥 Time Slot Table
            table = Table(title="⏰ Available Time Slots", show_lines=True)
            table.add_column("Option", justify="center", style="cyan")
            table.add_column("Time Slot", style="green")

            for i, slot in enumerate(self.time_slots, 1):
                table.add_row(str(i), slot)

            self.console.print(table)

            # 🔹 Select new slot
            while True:
                choice = input("Select new slot: ").strip()

                if not choice.isdigit():
                    self.console.print(Panel("[red]Invalid choice[/red]", title="ERROR"))
                    continue

                choice = int(choice)

                if 1 <= choice <= len(self.time_slots):
                    new_time = self.time_slots[choice - 1]
                    break

                self.console.print(Panel("[red]Choice out of range[/red]", title="ERROR"))

            # 🔥 Confirm
            confirm = input(f"Confirm reschedule to {new_time}? (yes/no): ").lower()

            if confirm != "yes":
                self.console.print(Panel("[yellow]Reschedule cancelled[/yellow]", title="INFO"))
                return

            # 🔥 Update
            found["time"] = new_time

            # ✅ Save using handler
            self.handler.handle_write(self.db.write_data, self.file, data)

            # 🔥 Success Panel
            self.console.print(
                Panel(
                    f"[bold green]Booking ID {bid} rescheduled to {new_time} 🔄[/bold green]",
                    title="SUCCESS",
                    border_style="green"
                )
            )

        except Exception as e:
            log_error(f"Reschedule Error: {e}")
            self.console.print(Panel("[bold red]Error rescheduling booking[/bold red]", title="ERROR"))         