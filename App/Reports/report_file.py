










from datetime import datetime
from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Report:

    def __init__(self):
        self.db = Data()
        self.handler = ExceptionHandler()
        self.console = Console()

        self.order_file = "App/Database/order.json"
        self.booking_file = "App/Database/booking.json"



    def generate_report(self):
        try:
            orders = self.handler.handle_read(self.db.read_data, self.order_file)
            bookings = self.handler.handle_read(self.db.read_data, self.booking_file)

            if not isinstance(orders, list) or not orders:
                self.console.print(Panel("[bold red]No orders found[/bold red]", title="❌ ERROR"))
                return

            if not isinstance(bookings, list):
                bookings = []

            # 🔥 DATE TIME
            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%I:%M %p")

            total_items_all = 0
            total_amount_all = 0

            # ================= LOOP ALL ORDERS =================
            for order in orders:

                # ✅ CUSTOMER FIX
                customer = (
                    order.get("customer_name")
                    or order.get("name")
                    or order.get("username")
                    or "N/A"
                )

                items = order.get("items") or order.get("order_items") or []

                payment = (
                    order.get("payment_method")
                    or order.get("payment")
                    or "N/A"
                )

                phone = order.get("phone")

                # ✅ BOOKING MATCH (NAME BASED)
                booking = next(
                    (
                        b for b in bookings
                        if b.get("name", "").lower() == customer.lower()
                        and b.get("status") == "Confirmed"
                    ),
                    None
                )

                if booking:
                    tables = booking.get("tables") or booking.get("table") or []
                    seats = booking.get("seats") or booking.get("sheet") or []

                    table_map = {}
                    for t, s in zip(tables, seats):
                        table_map.setdefault(t, []).append(s)

                    table_text = "\n".join(
                        [f"{t} → {', '.join(s)}" for t, s in table_map.items()]
                    )

                    booking_status = "[bold green]YES[/bold green]"
                else:
                    table_text = "[red]N/A[/red]"
                    booking_status = "[red]NO[/red]"

                # ================= HEADER =================
                header = f"""
    [bold cyan]📅 Date       :[/bold cyan] {date}
    [bold cyan]⏰ Time       :[/bold cyan] {time}

    [bold yellow]👤 Customer   :[/bold yellow] {customer}
    [bold magenta]🪑 Table No   :[/bold magenta]
    {table_text}

    [bold green]📌 Booking    :[/bold green] {booking_status}
    [bold blue]💳 Payment    :[/bold blue] {payment}
    """

                self.console.print(Panel(
                    header,
                    title="[bold green]🍽️ RESTAURANT REPORT[/bold green]",
                    border_style="cyan"
                ))

                # ================= ORDER TABLE =================
                table = Table(title="🧾 ORDER DETAILS", show_lines=True)

                table.add_column("ID", style="cyan", justify="center")
                table.add_column("Item Name", style="yellow")
                table.add_column("Qty", style="green", justify="center")
                table.add_column("Price", style="magenta", justify="center")

                total_items = 0
                total_amount = 0

                for i, item in enumerate(items, 1):
                    name = item.get("name") or item.get("item_name") or "Item"
                    qty = item.get("qty") or item.get("quantity") or 1
                    price = item.get("price") or 0

                    total_items += qty
                    total_amount += price * qty   # ✅ FIXED

                    table.add_row(str(i), name, str(qty), f"₹{price}")

                self.console.print(table)

                # ================= SUMMARY =================
                summary = f"""
    [bold yellow]💰 Total Items  :[/bold yellow] {total_items}
    [bold green]🛒 Total Sales  :[/bold green] ₹{total_amount}
    [bold cyan]💵 Total Earning:[/bold cyan] ₹{total_amount}
    """

                self.console.print(Panel(
                    summary,
                    title="[bold blue]📊 SUMMARY[/bold blue]",
                    border_style="green"
                ))

                total_items_all += total_items
                total_amount_all += total_amount

            # ================= FINAL SUMMARY =================
            final_summary = f"""
    [bold yellow]📦 Total Items (All Orders):[/bold yellow] {total_items_all}
    [bold green]💰 Total Revenue:[/bold green] ₹{total_amount_all}
    """

            self.console.print(Panel(
                final_summary,
                title="[bold magenta]📊 FINAL REPORT[/bold magenta]",
                border_style="yellow"
            ))

            # ================= FOOTER =================
            self.console.print(Panel(
                "[bold magenta]🙏 Thank You! Visit Again 🙏[/bold magenta]",
                border_style="cyan"
            ))

        except Exception as e:
            log_error(f"Report Error: {e}")
            self.console.print(Panel(
                f"[bold red]Error generating report: {e}[/bold red]",
                title="❌ ERROR"
            ))