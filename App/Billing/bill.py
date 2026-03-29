



from datetime import datetime
from App.Database.db import Data
from App.Logs.logger import log_error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class Ganeratebill:

    def __init__(self):
        self.console = Console()

    def generate_bill(self, order):
        try:
            db = Data()
            bills_file = "App/Database/bill.json"
            menu_file = "App/Database/menu.json"

            # ================= LOAD =================
            try:
                bills = db.read_data(bills_file)
                if not isinstance(bills, list):
                    bills = []
            except:
                bills = []

            try:
                menu = db.read_data(menu_file)
                if not isinstance(menu, list):
                    menu = []
            except:
                menu = []

            # ================= DUPLICATE CHECK =================
            for b in bills:
                if b.get("order_id") == order.get("order_id"):
                    self.console.print(Panel(
                        "[bold yellow]⚠ Bill already exists![/bold yellow]",
                        title="WARNING"
                    ))
                    return

            # ================= HEADER =================
            self.console.print(Panel.fit(
                f"[bold cyan]🧾 BILL - ORDER ID: {order.get('order_id')}[/bold cyan]\n"
                f"[white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/white]",
                border_style="cyan"
            ))

            # ================= ITEMS TABLE =================
            table = Table(title="🍽 Ordered Items", show_lines=True)
            table.add_column("Item", style="cyan")
            table.add_column("Size", style="magenta")
            table.add_column("Qty", justify="center")
            table.add_column("Price", justify="right")
            table.add_column("Total", justify="right", style="green")

            subtotal = 0

            for item in order.get("items", []):
                name = item.get("name", "Unknown")
                qty = item.get("quantity", 1)
                size = str(item.get("size", "full")).lower()

                menu_item = next(
                    (m for m in menu if m.get("name", "").lower() == name.lower()),
                    None
                )

                if menu_item:
                    item_type = menu_item.get("type", "").lower()

                    if item_type == "dessert":
                        price = menu_item.get("price", 0)
                    elif item_type in ["veg", "nonveg", "non-veg"]:
                        price = menu_item.get("half_price", 0) if size == "half" else menu_item.get("full_price", 0)
                    else:
                        price = 0
                else:
                    price = 0

                if not isinstance(price, (int, float)):
                    price = 0
                if not isinstance(qty, int):
                    qty = 1

                total = price * qty
                subtotal += total

                table.add_row(name, size, str(qty), f"₹{price}", f"₹{total}")

            self.console.print(table)

            # ================= TOTAL BOX =================
            gst = round(subtotal * 0.05, 2)
            total_payment = subtotal + gst

            total_text = f"""
💰 Subtotal : ₹{subtotal}
📊 GST (5%) : ₹{gst}
💳 Total    : ₹{total_payment}
"""
            self.console.print(Panel(total_text, title="💵 PAYMENT SUMMARY", border_style="green"))

            # ================= PAYMENT =================
            pay_text = "1. UPI\n2. Cash\n3. Card"
            self.console.print(Panel(pay_text, title="💳 Payment Method", border_style="blue"))

            while True:
                choice = input("👉 Enter choice (1-3): ").strip()
                if choice in ["1", "2", "3"]:
                    break
                self.console.print(Panel("[red]Invalid choice[/red]", title="ERROR"))

            payment_method = {"1": "UPI", "2": "Cash", "3": "Card"}[choice]
            upi_details = {}
            card_details = {}

            # ================= UPI =================
            if payment_method == "UPI":
                upi_text = "1. UPI ID\n2. QR Code\n3. Mobile Number"
                self.console.print(Panel(upi_text, title="📱 UPI Options"))

                while True:
                    upi_choice = input("👉 Enter choice: ").strip()
                    if upi_choice in ["1", "2", "3"]:
                        break
                    self.console.print(Panel("[red]Invalid choice[/red]", title="ERROR"))

                if upi_choice == "1":
                    while True:
                        upi_id = input("Enter UPI ID: ")
                        if "@" in upi_id:
                            upi_details["upi_id"] = upi_id
                            break
                        self.console.print(Panel("[red]Invalid UPI ID[/red]", title="ERROR"))
                else:
                    while True:
                        pin = input("Enter 4-digit PIN: ")
                        if pin.isdigit() and len(pin) == 4:
                            upi_details["pin"] = "****"
                            break
                        self.console.print(Panel("[red]Invalid PIN[/red]", title="ERROR"))

            # ================= CARD =================
            elif payment_method == "Card":
                while True:
                    card = input("Enter Card Number: ")
                    if card.isdigit() and len(card) == 16:
                        break
                    self.console.print(Panel("[red]Invalid Card[/red]", title="ERROR"))

                while True:
                    cvv = input("Enter CVV: ")
                    if cvv.isdigit() and len(cvv) == 3:
                        break
                    self.console.print(Panel("[red]Invalid CVV[/red]", title="ERROR"))

                card_details = {
                    "card_number": card[-4:],
                    "cvv": "***"
                }

            # ================= SUCCESS =================
            self.console.print(Panel(
                f"[bold green]Payment Successful via {payment_method} ✅[/bold green]",
                title="SUCCESS",
                border_style="green"
            ))

            # ================= SAVE =================
            bill_record = {
                "order_id": order.get("order_id"),
                "username": order.get("username"),
                "items": order.get("items"),
                "subtotal": subtotal,
                "gst": gst,
                "total_payment": total_payment,
                "payment_method": payment_method,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            bills.append(bill_record)
            db.write_data(bills_file, bills)

            self.console.print(Panel(
                "[bold cyan]🧾 Bill Saved Successfully![/bold cyan]",
                border_style="cyan"
            ))

        except Exception as e:
            log_error(e)
            self.console.print(Panel(
                f"[bold red]Error: {e}[/bold red]",
                title="ERROR"
            ))