import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from App.Logs.logger import log_error
from App.Database.db import Data

console = Console(force_terminal=True, color_system="truecolor")


class InventoryManager:

    def __init__(self):
        self.db = Data()
        self.file = "App/Database/inventory.json"

    def load(self):
        return self.db.read_data(self.file)

    def save(self, data):
        self.db.write_data(self.file, data)


    
    def view(self):
        try:
            data = self.load()

            if not data:
                console.print("[bold red]❌ Inventory Empty[/bold red]")
                return

            categories = {}

            for item in data:
                cat = item.get("category", "Other")
                categories.setdefault(cat, []).append(item)

            for cat, items in categories.items():

                color_map = {
                    "Veg": "green",
                    "Non-Veg": "red",
                    "Grocery": "blue",
                    "Sweets": "magenta"
                }

                table = Table(
                    title=f"📦 {cat.upper()} ITEMS",
                    box=box.ROUNDED,
                    show_lines=True
                )

                table.add_column("ID", justify="center", style="cyan")
                table.add_column("Name", style="white")
                table.add_column("Stock", justify="center", style="green")
                table.add_column("Status", justify="center", style="yellow")

                for item in items:
                    stock = item.get("stock", 0)

                    if stock == 0:
                        status = "[red]OUT[/red]"
                    elif stock < 5:
                        status = "[yellow]LOW[/yellow]"
                    else:
                        status = "[green]OK[/green]"

                    table.add_row(
                        str(item.get("id")),
                        item.get("name"),
                        str(stock),
                        status
                    )

                console.print(Panel(table, border_style=color_map.get(cat, "cyan")))

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "view", e)

    # ================= ADD =================
    def add(self):
        try:
            name = input("Item Name: ").strip()

            qty_input = input("Quantity: ")
            if not qty_input.isdigit():
                console.print("[red]❌ Invalid quantity[/red]")
                return

            qty = int(qty_input)

            console.print("1. Veg\n2. Non-Veg\n3. Sweets")
            ch = input("Choose: ")

            category_map = {
                "1": "Veg",
                "2": "Non-Veg",
                "3": "Sweets"
            }

            category = category_map.get(ch, "Other")

            data = self.load()

            for item in data:
                if item["name"].lower() == name.lower():
                    item["stock"] += qty
                    self.save(data)
                    console.print("[green]🔄 Updated existing item[/green]")
                    return

            new_id = max([i.get("id", 0) for i in data], default=0) + 1

            data.append({
                "id": new_id,
                "name": name,
                "stock": qty,
                "category": category
            })

            self.save(data)
            console.print("[green]✅ Item Added[/green]")

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "add", e)

    # ================= REMOVE =================
    def remove(self):
        try:
            name = input("Enter item name to remove: ").lower()
            data = self.load()

            new = [i for i in data if i["name"].lower() != name]

            if len(new) == len(data):
                console.print("[red]❌ Item not found[/red]")
                return

            self.save(new)
            console.print("[red]🗑️ Item Removed[/red]")

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "remove", e)

    # ================= UPDATE =================
    def update(self):
        try:
            item_id = input("Enter Item ID: ")

            if not item_id.isdigit():
                console.print("[red]❌ Invalid ID[/red]")
                return

            item_id = int(item_id)

            qty = input("New Stock: ")
            if not qty.isdigit():
                console.print("[red]❌ Invalid quantity[/red]")
                return

            qty = int(qty)

            data = self.load()

            for item in data:
                if item.get("id") == item_id:
                    item["stock"] = qty
                    self.save(data)
                    console.print("[green]🔄 Stock Updated[/green]")
                    return

            console.print("[red]❌ Item not found[/red]")

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "update", e)

    # ================= SEARCH =================
    def search(self):
        try:
            name = input("Search item: ").lower()
            data = self.load()

            found = [i for i in data if name in i["name"].lower()]

            if not found:
                console.print("[red]❌ Item not found[/red]")
                return

            for i in found:
                console.print(Panel(
                    f"Item: {i['name']}\nStock: {i['stock']}\nCategory: {i.get('category')}"
                ))

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "search", e)

    # ================= LOW STOCK =================
    def low_stock(self):
        try:
            data = self.load()

            low = [i for i in data if i.get("stock", 0) < 5]

            if not low:
                console.print("[green]✅ No Low Stock[/green]")
                return

            table = Table(title="LOW STOCK ALERT", box=box.ROUNDED)
            table.add_column("Item")
            table.add_column("Stock")
            table.add_column("Category")

            for i in low:
                table.add_row(i["name"], str(i["stock"]), i.get("category"))

            console.print(Panel(table, border_style="red"))

        except Exception as e:
            log_error.log_exception(self.__class__.__name__, "low_stock", e)

    # ================= GET ITEM =================
    def get_inventory_by_id(self, item_id):
        data = self.load()
        for item in data:
            if str(item["id"]) == str(item_id):
                return item
        return None

    # ================= GET STOCK =================
    def get_stock_by_id(self, item_id):
        data = self.load()
        for item in data:
            if item.get("id") == item_id:
                return item.get("stock", 0)
        return None

    # ================= REDUCE STOCK =================
    def reduce_stock(self, item_id, qty):
        data = self.load()
        for item in data:
            if item.get("id") == item_id:
                item["stock"] -= qty
                break
        self.save(data)


# ================= MENU =================
def inventory_staff_menu():
    im = InventoryManager()

    while True:
        console.print(Panel(
            "[bold cyan]1. View[/bold cyan]\n"
            "[bold green]2. Add[/bold green]\n"
            "[bold yellow]3. Update[/bold yellow]\n"
            "[bold red]4. Remove[/bold red]\n"
            "[bold magenta]5. Search[/bold magenta]\n"
            "[bold white]6. Low Stock[/bold white]\n"
            "[bold blue]7. Back[/bold blue]"
        ))

        choice = input("Enter choice: ")

        if choice == "1":
            im.view()
        elif choice == "2":
            im.add()
        elif choice == "3":
            im.update()
        elif choice == "4":
            im.remove()
        elif choice == "5":
            im.search()
        elif choice == "6":
            im.low_stock()
        elif choice == "7":
            break
        else:
            console.print("[red]❌ Invalid choice[/red]")    

    # ================= VIEW =================
#     def view(self):
#         try:
#             data = self.load()

#             if not data:
#                 console.print("[bold red]❌ Inventory Empty[/bold red]")
#                 return

#             categories = {}

#             # ===== GROUP BY CATEGORY =====
#             for item in data:
#                 cat = item.get("category", "Other")
#                 categories.setdefault(cat, []).append(item)

#             # ===== SHOW CATEGORY WISE =====
#             for cat, items in categories.items():

#                 color_map = {
#                     "Veg": "green",
#                     "Non-Veg": "red",
#                     "Grocery": "blue",
#                     "Sweets": "magenta"
#                 }

#                 border_color = color_map.get(cat, "cyan")

#                 table = Table(
#                     title=f"📦 {cat.upper()} ITEMS",
#                     box=box.ROUNDED,
#                     show_lines=True
#                 )

#                 table.add_column("ID", style="bold cyan", justify="center")
#                 table.add_column("Name", style="bold white")
#                 table.add_column("Stock", style="bold green", justify="center")
#                 table.add_column("Status", style="bold yellow", justify="center")

#                 # ===== LOOP ITEMS =====
#                 for item in items:
#                     stock = item.get("stock", 0)

#                     # ===== STATUS FIX =====
#                     if stock == 0:
#                         status = "[red]❌ OUT[/red]"
#                     elif stock < 5:
#                         status = "[yellow]⚠️ LOW[/yellow]"
#                     else:
#                         status = "[green]✅ OK[/green]"

#                     table.add_row(
#                         str(item.get("id", "-")),   # ✅ ID FIX
#                         item.get("name", "-"),
#                         str(stock),
#                         status
#                     )

#                 console.print(Panel(table, border_style=border_color))

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "view", e)
#     # ================= ADD =================

#     def add(self):
#         try:
#             name = input("Item Name: ").strip()

#             qty_input = input("Quantity: ")
#             if not qty_input.isdigit():
#                 console.print("[red]❌ Invalid quantity[/red]")
#                 return

#             qty = int(qty_input)

#             console.print("1. Veg\n2. Non-Veg\n3. Grocery\n4. Sweets")
#             ch = input("Choose: ")

#             category_map = {
#                 "1": "Veg",
#                 "2": "Non-Veg",
#                 "3": "Grocery",
#                 "4": "Sweets"
#             }

#             category = category_map.get(ch, "Other")

#             data = self.load()

#             # ===== UPDATE EXISTING =====
#             for item in data:
#                 if item["name"].lower() == name.lower():
#                     item["stock"] += qty
#                     self.save(data)
#                     console.print("[green]🔄 Updated[/green]")
#                     return

#             # ===== NEW ITEM =====
#             new_id = max([i.get("id", 0) for i in data], default=0) + 1

#             data.append({
#                 "id": new_id,
#                 "name": name,
#                 "stock": qty,
#                 "category": category
#             })

#             self.save(data)

#             console.print("[green]✅ Item Added[/green]")

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "add", e)
#     # ================= REMOVE =================
#     def remove(self):
#         try:
#             console.print("[yellow]Item Name to remove:[/yellow]", end=" ")
#             name = input().lower()

#             data = self.load()

#             new = [i for i in data if i["name"].lower() != name]

#             if len(new) == len(data):
#                 console.print("[red]❌ Item not found[/red]")
#                 return

#             self.save(new)

#             console.print("[bold red]🗑️ Item Removed[/bold red]")

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "remove", e)

#     # ================= UPDATE =================
#     def update(self):
#         try:
#             # ===== INPUT ID =====
#             console.print("[yellow]Enter Item ID:[/yellow]", end=" ")
#             item_id_input = input().strip()

#             if not item_id_input.isdigit():
#                 console.print("[red]❌ Invalid ID[/red]")
#                 return

#             item_id = int(item_id_input)

#             # ===== INPUT NEW STOCK =====
#             console.print("[yellow]New Stock Quantity:[/yellow]", end=" ")
#             qty_input = input().strip()

#             if not qty_input.isdigit():
#                 console.print("[red]❌ Quantity must be a number[/red]")
#                 return

#             qty = int(qty_input)

#             if qty < 0:
#                 console.print("[red]❌ Quantity cannot be negative[/red]")
#                 return

#             # ===== LOAD DATA =====
#             data = self.load()

#             # ===== FIND ITEM =====
#             for item in data:
#                 if item.get("id") == item_id:

#                     item["stock"] = qty   # ✅ ONLY stock update

#                     self.save(data)

#                     console.print(
#                         f"[bold green]🔄 Updated: {item['name']} → Stock = {qty}[/bold green]"
#                     )
#                     return

#             # ===== NOT FOUND =====
#             console.print("[red]❌ Item not found[/red]")

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "update", e)
#     # ================= SEARCH =================
#     def search(self):
#         try:
#             console.print("[yellow]Search Item:[/yellow]", end=" ")
#             name = input().lower()

#             data = self.load()

#             found = [i for i in data if name in i["name"].lower()]

#             if not found:
#                 console.print("[red] Item not found[/red]")
#                 return

#             for i in found:
#                 console.print(Panel(
#                     f"[cyan]Item:[/cyan] {i['name']}\n"
#                     f"[green]Quantity:[/green] {i['qty']}\n"
#                     f"[magenta]Category:[/magenta] {i.get('category','-')}",
#                     border_style="cyan"
#                 ))

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "search", e)

#     # ================= LOW STOCK =================
#     def low_stock(self):
#         try:
#             data = self.load()

#             low = [i for i in data if i.get("qty", 0) < 5]

#             if not low:
#                 console.print("[green]✅ No Low Stock Items[/green]")
#                 return

#             table = Table(title="⚠️ LOW STOCK ALERT", box=box.ROUNDED)

#             table.add_column("Item", style="red")
#             table.add_column("Qty", style="yellow")
#             table.add_column("Category", style="cyan")

#             for i in low:
#                 table.add_row(i["name"], str(i["qty"]), i.get("category", "-"))

#             console.print(Panel(table, border_style="red"))

#         except Exception as e:
#             log_error.log_exception(self.__class__.__name__, "low_stock", e)

#     def get_inventory_by_id(self, item_id):
#         data = self.load()

#         for item in data:
#             if str(item["id"]) == str(item_id):
#                 return item

#             return None
#     def get_stock_by_id(self, item_id):
#         data = self.load()
#         for item in data:
#             if item.get("id") == item_id:
#                 return item.get("stock", 0)
#         return None


#     def reduce_stock(self, item_id, qty):
#         data = self.load()
#         for item in data:
#             if item.get("id") == item_id:
#                 item["stock"] -= qty
#                 break
#         self.save(data)


# # ================= MENU =================
# def inventory_staff_menu():
#     im = InventoryManager()

#     while True:
#         try:
#             console.print(Panel(
#                 "[bold blue]📦 INVENTORY STAFF MENU[/bold blue]\n\n"
#                 "[bold cyan]1. View Inventory[/bold cyan]\n"
#                 "[bold green]2. Add Item[/bold green]\n"
#                 "[bold yellow]3. Update Item[/bold yellow]\n"
#                 "[bold red]4. Remove Item[/bold red]\n"
#                 "[bold magenta]5. Search Item[/bold magenta]\n"
#                 "[bold white]6. Low Stock Alert[/bold white]\n"
#                 "[bold blue]7. Back[/bold blue]",
#                 border_style="blue"
#             ))

#             console.print("[yellow]Enter choice:[/yellow]", end=" ")
#             ch = input()

#             if ch == "1":
#                 im.view()
#             elif ch == "2":
#                 im.add()
#             elif ch == "3":
#                 im.update()
#             elif ch == "4":
#                 im.remove()
#             elif ch == "5":
#                 im.search()
#             elif ch == "6":
#                 im.low_stock()
#             elif ch == "7":
#                 break
#             else:
#                 console.print("[red]❌ Invalid choice[/red]")

#         except Exception as e:
#             log_error.log_exception("InventoryMenu", "loop", e)
#             console.print("[red]Menu Error![/red]")