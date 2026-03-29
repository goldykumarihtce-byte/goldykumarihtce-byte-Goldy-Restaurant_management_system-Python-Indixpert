from App.Menu.start_menu import Menu
from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error
from App.Booking.booking import Booking
from rich.panel import Panel
from rich.table import Table
from rich.console import Console

class Staff_dashboard:

    def __init__(self):
        self.db = Data()
        self.orders_file = "App/Database/order.json"  # ✅ Correct file
        self.handler = ExceptionHandler()
        self.console = Console()

    

    def update_order_status(self):
        try:
            orders = self.db.read_data(self.orders_file)

            if not isinstance(orders, list):
                orders = []

            if not orders:
                self.console.print(Panel("[bold yellow]No orders available[/bold yellow]", title="INFO"))
                return

            order_id = input("Enter Order ID to update: ")

            found = next((order for order in orders if str(order.get("order_id")) == order_id), None)

            if not found:
                self.console.print(Panel("[bold red]Order not found[/bold red]", title="ERROR"))
                return

            # 🔥 Status selection table
            table = Table(title="📌 Select New Status", show_lines=True)
            table.add_column("Option", justify="center", style="cyan")
            table.add_column("Status", style="green")

            table.add_row("1", "Pending")
            table.add_row("2", "Preparing")
            table.add_row("3", "Delivered")
            table.add_row("4", "Cancelled")

            self.console.print(table)

            status_choice = input("Select new status: ")

            status_map = {
                "1": "Pending",
                "2": "Preparing",
                "3": "Delivered",
                "4": "Cancelled"
            }

            if status_choice in status_map:
                found["Status"] = status_map[status_choice]
                self.db.write_data(self.orders_file, orders)

                # 🔥 Success panel
                panel = Panel(
                    f"[bold green]Order ID {order_id} updated to {status_map[status_choice]} ✅[/bold green]",
                    title="SUCCESS",
                    border_style="green"
                )

                self.console.print(panel)

            else:
                self.console.print(Panel("[bold red]Invalid choice[/bold red]", title="ERROR"))

        except Exception as e:
            log_error(e)
            self.console.print(Panel("[bold red]Failed to update order[/bold red]", title="ERROR"))

    

    def staffdashboard_menu(self):
        while True:
            panel = Panel(
                "[bold cyan]1.[/bold cyan] Place Order 🛒\n"
                "[bold cyan]2.[/bold cyan] Update Order Status ⚡\n"
                "[bold cyan]3.[/bold cyan] Booking 📅\n"
                "[bold cyan]4.[/bold cyan] Back 🔙",
                title="👨‍🍳 STAFF DASHBOARD",
                border_style="blue"
            )

            self.console.print(panel)

            choice = input("Enter your choice (1-4): ").strip()

            if not choice.isdigit():
                self.console.print(Panel("[bold red]Invalid choice[/bold red]", title="ERROR"))
                continue

            choice = int(choice)

            if choice == 1:
                try:
                    menu_obj = Menu()
                    menu_obj.start_menu()
                except Exception as e:
                    log_error(e)
                    print("Failed to start menu")

            elif choice == 2:
                self.update_order_status()


            elif choice == 3:
                book=Booking()
                book.booking_menu() 
                
            elif choice == 4:
                print("Going back to main menu")
                self.console.print(Panel("[bold yellow]Going back...[/bold yellow]", title="EXIT"))
                break

            else:
                self.console.print(Panel("[bold red]Invalid option[/bold red]", title="ERROR"))
                if not choice.isdigit():
                    self.handler.invalid_choice()
                    continue

         











