



from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error
from App.Billing.bill import Ganeratebill
from App.Dashboard.Admin_dashboard import Admin_dashboard
from App.Order.order import Order
from rich.console import Console
from rich.panel import Panel


class Menu:

    def __init__(self):
        self.handler = ExceptionHandler()
        self.db = Data()
        self.menu_file = "App/Database/menu.json"
        self.order_file = "App/Database/order.json"
        self.review_file = "App/Database/review.json"
        self.console = Console()  # ✅ Use this instead of global console

    # ================= BOX UI =================
    def show_box(self, title, messages, status=None):
        self.console.print(f"\n[bold cyan]{title}[/bold cyan]")
        for msg in messages:
            if status == "success":
                self.console.print(f"[green]✔ {msg}[/green]")
            elif status == "error":
                self.console.print(f"[red]✖ {msg}[/red]")
            else:
                self.console.print(msg)

    # ================= CANCEL ORDER =================
    def cancel_replace_order(self):
        try:
            orders = self.db.read_data(self.order_file)
            if not orders:
                self.console.print("[red]No orders available[/red]")
                return

            order_id = input("Enter Order ID: ")
            found = next((o for o in orders if str(o.get("order_id")) == order_id), None)

            if not found:
                self.console.print("[red]Order not found[/red]")
                return

            found["Status"] = "Cancelled"
            self.db.write_data(self.order_file, orders)
            self.console.print("[yellow]Order Cancelled ✅[/yellow]")

        except Exception as e:
            log_error(e)

    # ================= ADD REVIEW =================
    def add_review(self):
        try:
            reviews = self.db.read_data(self.review_file)
            if not isinstance(reviews, list):
                reviews = []

            name = input("Enter name: ")
            review = input("Enter review: ")

            from datetime import datetime
            reviews.append({
                "id": len(reviews) + 1,
                "name": name,
                "review": review,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.db.write_data(self.review_file, reviews)
            self.console.print("[green]✔ Review Added[/green]")

        except Exception as e:
            log_error(e)

    # ================= START MENU =================
    def start_menu(self):
        while True:
            panel = Panel(
                "[bold cyan]1.[/bold cyan] Show Menu 🍔\n"
                "[bold cyan]2.[/bold cyan] Order Items 🛒\n"
                "[bold cyan]3.[/bold cyan] Cancel Order ❌\n"
                "[bold cyan]4.[/bold cyan] Generate Bill 🧾\n"
                "[bold cyan]5.[/bold cyan] Add Review ✨\n"
                "[bold cyan]6.[/bold cyan] Exit 🔚",
                title="🍽️ MAIN MENU",
                border_style="cyan"
            )

            self.console.print(panel)

            option = input("Enter choice: ").strip()

            if not option.isdigit():
                self.console.print(Panel("[bold red]Invalid choice[/bold red]", title="ERROR"))
                continue

            option = int(option)

            if option == 1:
                menu = Admin_dashboard()
                menu.show_menu()

            elif option == 2:
                order = Order()
                order.order_item()

            elif option == 3:
                self.cancel_replace_order()

            elif option == 4:
                try:
                    orders = self.db.read_data(self.order_file)
                    if not isinstance(orders, list):
                        orders = []

                    if not orders:
                        self.console.print(Panel("[bold yellow]No orders available[/bold yellow]", title="INFO"))
                        continue

                    order_id = input("Enter Order ID: ").strip()
                    found = next((o for o in orders if str(o.get("order_id")) == order_id), None)

                    if not found:
                        self.console.print(Panel("[bold red]Order not found[/bold red]", title="ERROR"))
                        continue

                    if found.get("Status", "").lower() == "cancelled":
                        self.console.print(Panel("[bold red]Order is cancelled[/bold red]", title="ERROR"))
                        continue

                    Ganeratebill().generate_bill(found)

                except Exception as e:
                    log_error(e)
                    self.console.print(Panel("[bold red]Bill generation failed[/bold red]", title="ERROR"))

            elif option == 5:
                self.add_review()

            elif option == 6:
                self.console.print(Panel("[bold yellow]Exiting Menu...[/bold yellow]", title="EXIT"))
                return

            else:
                self.console.print(Panel("[bold red]Invalid option[/bold red]", title="ERROR"))