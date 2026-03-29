

from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error
from App.Booking.booking import Booking
from App.Reports.report_file import Report
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class Admin_dashboard:

    def __init__(self):
        self.db = Data()
        self.console = Console()  # fixed: instance variable
        self.menu_file = "App/Database/menu.json"
        self.orders_file = "App/Database/order.json"
        self.bill_file = "App/Database/bill.json"
        self.handler = ExceptionHandler()

        # Ensure menu file is valid
        self.menu = self.db.read_data(self.menu_file)
        if not isinstance(self.menu, list):
            self.menu = []
            self.db.write_data(self.menu_file, self.menu)

  
    def show_box(self, title, messages, status=None):
        print("\n╔" + "═"*45 + "╗")
        print(f"   {title}")
        print("╠" + "═"*45 + "╣")
        for msg in messages:
            if status == "success":
                print(f" [✔] {msg}")
            elif status == "error":
                print(f" [✖] {msg}")
            else:
                print(f"  {msg}")
        print("╚" + "═"*45 + "╝")

   
    def show_menu(self):
        menu = self.db.read_data(self.menu_file)
        if not isinstance(menu, list) or not menu:
            self.console.print("[red]Menu is empty[/red]")
            return

        def normalize_type(type_str):
            return type_str.lower().replace(" ", "-")

        types = ["veg", "non-veg", "dessert"]
        for t in types:
            filtered = [item for item in menu if normalize_type(item.get("type","")) == t]
            if not filtered:
                continue

            table = Table(title=f"{t.upper()} MENU")
            table.add_column("ID", justify="center", style="cyan", no_wrap=True)
            table.add_column("Name", style="magenta")
            if t == "dessert":
                table.add_column("Price", justify="right", style="green")
            else:
                table.add_column("Half Price", justify="right", style="green")
                table.add_column("Full Price", justify="right", style="green")

            for item in filtered:
                if t == "dessert":
                    table.add_row(str(item.get("id")), item.get("name"), f"₹{item.get('price')}")
                else:
                    table.add_row(
                        str(item.get("id")),
                        item.get("name"),
                        f"₹{item.get('half_price')}",
                        f"₹{item.get('full_price')}"
                    )

            self.console.print(table)
            self.console.print("\n")

    def add_item(self):
        try:
            menu = self.db.read_data(self.menu_file)
            if not isinstance(menu, list):
                menu = []

            name = input("Enter item name: ").strip()
            type_ = input("Enter type (veg/non-veg/dessert): ").strip().lower()

            if type_ not in ["veg", "non-veg", "dessert"]:
                self.show_box("ERROR", ["Invalid type"], "error")
                return

            if type_ == "dessert":
                price = int(input("Enter price: "))
                new_item = {
                    "id": len(menu)+1,
                    "name": name,
                    "type": type_,
                    "price": price
                }
            else:
                half_price = int(input("Enter half price: "))
                full_price = int(input("Enter full price: "))
                new_item = {
                    "id": len(menu)+1,
                    "name": name,
                    "type": type_,
                    "half_price": half_price,
                    "full_price": full_price
                }

            menu.append(new_item)
            self.db.write_data(self.menu_file, menu)
            self.show_box("SUCCESS", ["Item added successfully"], "success")

        except Exception as e:
            log_error(e)
            self.show_box("ERROR", ["Failed to add item"], "error")

  
    def update_item(self):
        try:
            menu = self.db.read_data(self.menu_file)
            if not menu:
                self.show_box("INFO", ["Menu is empty"], "error")
                return

            self.show_menu()
            item_id = int(input("Enter item ID to update: "))
            item = next((i for i in menu if i.get("id") == item_id), None)
            if not item:
                self.show_box("ERROR", ["Item not found"], "error")
                return

            new_name = input(f"Enter new name [{item.get('name')}]: ").strip()
            if new_name:
                item["name"] = new_name

            if item["type"] == "dessert":
                price = input(f"Enter new price [{item.get('price')}]: ").strip()
                if price:
                    item["price"] = int(price)
            else:
                half_price = input(f"Enter new half price [{item.get('half_price')}]: ").strip()
                full_price = input(f"Enter new full price [{item.get('full_price')}]: ").strip()
                if half_price:
                    item["half_price"] = int(half_price)
                if full_price:
                    item["full_price"] = int(full_price)

            self.db.write_data(self.menu_file, menu)
            self.show_box("SUCCESS", ["Item updated successfully"], "success")

        except Exception as e:
            log_error(e)
            self.show_box("ERROR", ["Failed to update item"], "error")

   
    def delete_item(self):
        try:
            menu = self.db.read_data(self.menu_file)
            if not menu:
                self.show_box("INFO", ["Menu is empty"], "error")
                return

            self.show_menu()
            item_id = int(input("Enter item ID to delete: "))
            item = next((i for i in menu if i.get("id") == item_id), None)
            if not item:
                self.show_box("ERROR", ["Item not found"], "error")
                return

            menu.remove(item)
            # Reassign IDs
            for idx, i in enumerate(menu, start=1):
                i["id"] = idx

            self.db.write_data(self.menu_file, menu)
            self.show_box("SUCCESS", ["Item deleted successfully"], "success")

        except Exception as e:
            log_error(e)
            self.show_box("ERROR", ["Failed to delete item"], "error")

    def view_orders(self):
        try:
            orders = self.db.read_data(self.orders_file)

            if not orders:
                self.console.print(Panel("[bold yellow]No orders found[/bold yellow]", title="INFO"))
                return

            for o in orders:
                table = Table(title=f"🧾 Order ID: {o.get('order_id')}", show_lines=True)

                table.add_column("Item", style="cyan")
                table.add_column("Type", style="magenta")
                table.add_column("Size", style="green")
                table.add_column("Qty", justify="center")
                table.add_column("Price", justify="right")

                for itm in o.get("items", []):
                    table.add_row(
                        itm.get("name", "-"),
                        itm.get("type", "-"),
                        itm.get("size", "-"),
                        str(itm.get("quantity", 0)),
                        f"₹{itm.get('price', 0)}"
                    )

                panel = Panel(
                    table,
                    title=f"👤 User: {o.get('username', 'Unknown')}",
                    subtitle=f"📌 Status: {o.get('Status')}",
                    border_style="blue"
                )

                self.console.print(panel)

        except Exception as e:
            log_error(e)
            self.console.print(Panel("[bold red]Failed to load orders[/bold red]", title="ERROR"))
    


    def check_payment(self):
        try:
            bills = self.db.read_data(self.bill_file)

            if not bills:
                self.console.print(Panel("[bold yellow]No bills found[/bold yellow]", title="INFO"))
                return

            oid = input("Enter Order ID: ").strip()

            found = next((b for b in bills if str(b.get("order_id")) == oid), None)

            if not found:
                self.console.print(Panel("[bold red]Payment not found[/bold red]", title="ERROR"))
                return

            # 🔥 Table banaya
            table = Table(title=f"💳 Payment Details (Order ID: {found.get('order_id')})", show_lines=True)

            table.add_column("Field", style="cyan", no_wrap=True)
            table.add_column("Details", style="green")

            table.add_row("Customer", found.get("username", "Unknown"))
            table.add_row("Total Paid", f"₹{found.get('total_payment', 0)}")
            table.add_row("Payment Status", "Paid ✅")

            # 🔥 Panel wrap
            panel = Panel(
                table,
                title="🧾 PAYMENT INFO",
                border_style="blue"
            )

            self.console.print(panel)

        except Exception as e:
            log_error(e)
            self.console.print(Panel("[bold red]Failed to fetch payment[/bold red]", title="ERROR"))

    # =============== TOTAL REVENUE =================
    def total_revenue(self):
        try:
            bills = self.db.read_data(self.bill_file)

            if not isinstance(bills, list):
                bills = []

            total = sum(b.get("total_payment", 0) for b in bills)

            # 🔥 Table banaya
            table = Table(title="💰 Revenue Summary", show_lines=True)

            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")

            table.add_row("Total Orders", str(len(bills)))
            table.add_row("Total Revenue", f"₹{total}")

            # 🔥 Panel wrap
            panel = Panel(
                table,
                title="📊 TOTAL REVENUE",
                border_style="blue"
            )

            self.console.print(panel)

        except Exception as e:
            log_error(e)
            self.console.print(Panel("[bold red]Failed to calculate revenue[/bold red]", title="ERROR"))


    # =============== ADMIN DASHBOARD MENU =================
    

    def admin_dashboard_menu(self):
        while True:
            panel = Panel(
                "[bold cyan]1.[/bold cyan] Show Menu 🍔\n"
                "[bold cyan]2.[/bold cyan] Add Item ➕\n"
                "[bold cyan]3.[/bold cyan] Update Item ✏️\n"
                "[bold cyan]4.[/bold cyan] Delete Item ❌\n"
                "[bold cyan]5.[/bold cyan] View Orders 📋\n"
                "[bold cyan]6.[/bold cyan] Check Payment 💳\n"
                "[bold cyan]7.[/bold cyan] View Booking 📅\n"
                "[bold cyan]8.[/bold cyan] Total Revenue 💰\n"
                "[bold cyan]9.[/bold cyan] Report ✅\n"
                "[bold cyan]10.[/bold cyan] Back 🔙",
                title="🛠️ ADMIN DASHBOARD",
                border_style="blue"
            )

            self.console.print(panel)

            choice = input("Enter your choice (1-9): ").strip()

            if not choice.isdigit():
                self.console.print(Panel("[bold red]Invalid choice[/bold red]", title="ERROR"))
                continue

            choice = int(choice)

            if choice == 1:
                self.show_menu()

            elif choice == 2:
                self.add_item()

            elif choice == 3:
                self.update_item()

            elif choice == 4:
                self.delete_item()

            elif choice == 5:
                self.view_orders()

            elif choice == 6:
                self.check_payment()

            elif choice == 7:
                book = Booking()
                book.view_booking()

            elif choice == 8:
                self.total_revenue()

            elif choice == 9:
                report=Report()
                report.generate_report()    

            elif choice == 10:
                self.console.print(Panel("[bold yellow]Going back...[/bold yellow]", title="EXIT"))
                break

            else:
                self.console.print(Panel("[bold red]Invalid option[/bold red]", title="ERROR"))