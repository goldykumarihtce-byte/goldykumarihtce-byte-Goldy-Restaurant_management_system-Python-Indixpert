



# from App.Database.db import Data
# from App.Utils.exception_handling import ExceptionHandler
# from App.Inventory.inventory_manager import InventoryManager


# class Order:
#     def __init__(self):
#         self.db = Data()
#         self.order_file = "App/Database/order.json"
#         self.menu_file = "App/Database/menu.json"

#     # ================= BOX UI =================
#     def show_box(self, title, messages, status="success"):
#         symbol = "✔" if status == "success" else "✖"
#         print("\n╔" + "═"*35 + "╗")
#         print(f"   {title}")
#         print("╠" + "═"*35 + "╣")
#         for msg in messages:
#             print(f" [{symbol}] {msg}")
#         print("╚" + "═"*35 + "╝")

#     # ================= ORDER ITEM =================
#     def order_item(self):
#         handler = ExceptionHandler()
#         menu = self.db.read_data(self.menu_file)
#         orders = self.db.read_data(self.order_file)

#         if not isinstance(menu, list):
#             menu = []
#         if not isinstance(orders, list):
#             orders = []

    
#         name = input("Enter your name: ").strip()

#         order_id = len(orders) + 1
#         order_list = []

#         while True:
#             item = input("Enter item name: ").strip().lower()
#             found = next((f for f in menu if f["name"].lower() == item), None)

#             if not found:
#                 self.show_box("ERROR", ["Item not available"], "error")
#                 continue

#             if found["type"] == "dessert":
#                 price = found["price"]
#                 size = "single"
#             else:
#                 size = input("Choose size (half/full): ").lower()
#                 if size == "half":
#                     price = found["half_price"]
#                 elif size == "full":
#                     price = found["full_price"]
#                 else:
#                     self.show_box("ERROR", ["Invalid size"], "error")
#                     continue

#             try:
#                 quantity = int(input("Enter quantity: "))
#                 if quantity <= 0:
#                     self.show_box("ERROR", ["Quantity must be > 0"], "error")
#                     continue
#             except ValueError:
#                 handler.value_error()
#                 continue

#             order_list.append({
#                 "name": item,
#                 "type": found["type"],
#                 "size": size,
#                 "price": price,
#                 "quantity": quantity
#             })

#             more = input("Add more items? (yes/no): ").strip().lower()
#             if more == "no":
#                 break

#         order_data = {
#             "order_id": order_id,
#             "name": name,  
#             "items": order_list,
#             "Status": "Pending"
#         }

#         orders.append(order_data)
#         self.db.write_data(self.order_file, orders)
#         self.show_box("SUCCESS", ["Order placed successfully", f"Order ID: {order_id}"])









# from App.Database.db import Data
# from App.Utils.exception_handling import ExceptionHandler
# from App.Inventory.inventory_manager import InventoryManager


# class Order:
#     def __init__(self):
#         self.db = Data()
#         self.inventory = InventoryManager()
#         self.order_file = "App/Database/order.json"
#         self.menu_file = "App/Database/menu.json"

#     def show_box(self, title, messages, status="success"):
#         symbol = "✔" if status == "success" else "✖"
#         print("\n╔" + "═"*35 + "╗")
#         print(f"   {title}")
#         print("╠" + "═"*35 + "╣")
#         for msg in messages:
#             print(f" [{symbol}] {msg}")
#         print("╚" + "═"*35 + "╝")

#     def order_item(self):
#         handler = ExceptionHandler()
#         menu = self.db.read_data(self.menu_file)
#         orders = self.db.read_data(self.order_file)
    

#         if not isinstance(menu, list):
#             menu = []
#         if not isinstance(orders, list):
#             orders = []

#         username = input("Enter your name: ").strip()
#         order_id = len(orders) + 1
#         order_list = []

#         while True:
#             # 🔍 SEARCH
#             keyword = input("\nSearch item (e.g. chicken, paneer): ").strip().lower()

#             filtered = [f for f in menu if keyword in f["name"].lower()]

#             if not filtered:
#                 self.show_box("ERROR", ["No items found"], "error")
#                 continue

#             # 📋 SHOW FILTERED MENU
#             print("\n====== SEARCH RESULT ======")
#             for item in filtered:
#                 if item["type"].lower() == "dessert":
#                     print(f"{item['id']}. {item['name']} - ₹{item['price']}")
#                 else:
#                     print(f"{item['id']}. {item['name']} (Half ₹{item['half_price']} / Full ₹{item['full_price']})")

#             # 🔢 SELECT ID
#             item_id_input = input("\nEnter item ID: ").strip()

#             if not item_id_input.isdigit():
#                 self.show_box("ERROR", ["Invalid ID"], "error")
#                 continue

#             item_id = int(item_id_input)

#             found = next((f for f in filtered if f["id"] == item_id), None)

#             if not found:
#                 self.show_box("ERROR", ["Invalid selection"], "error")
#                 continue

#             # 📦 INVENTORY CHECK
#             stock = self.inventory.get_stock_by_id(item_id)

#             if stock is None:
#                 self.show_box("ERROR", ["Item not in inventory"], "error")
#                 continue

#             # 💰 PRICE
#             if found["type"].strip().lower() == "dessert":
#                 price = found["price"]
#                 size = "single"
#             else:
#                 size = input("Choose size (half/full): ").strip().lower()

#                 if size == "half":
#                     price = found["half_price"]
#                 elif size == "full":
#                     price = found["full_price"]
#                 else:
#                     self.show_box("ERROR", ["Invalid size"], "error")
#                     continue

#             # 🔢 QUANTITY
#             qty_input = input("Enter quantity: ").strip()

#             if not qty_input.isdigit():
#                 handler.value_error()
#                 continue

#             quantity = int(qty_input)

#             if quantity <= 0:
#                 self.show_box("ERROR", ["Quantity must be > 0"], "error")
#                 continue

#             if quantity > stock:
#                 self.show_box("ERROR", [f"Only {stock} available"], "error")
#                 continue

#             # ✅ ADD ORDER
#             order_list.append({
#                 "id": item_id,
#                 "name": found["name"],
#                 "type": found["type"],
#                 "size": size,
#                 "price": price,
#                 "quantity": quantity
#             })

#             more = input("Add more? (yes/no): ").strip().lower()

#             if more == "no":
#                 break

#         # 💾 SAVE ORDER
#         order_data = {
#             "order_id": order_id,
#             "username": username,
#             "items": order_list,
#             "Status": "Pending"
#         }

#         orders.append(order_data)
#         self.db.write_data(self.order_file, orders)

#         # 📉 REDUCE STOCK
#         for item in order_list:
#             self.inventory.reduce_stock(item["id"], item["quantity"])

#         self.show_box("SUCCESS", ["Order placed", f"Order ID: {order_id}"])    

        # name = input("Enter your name: ").strip()
        # order_id = len(orders) + 1
        # order_list = []

        # while True:
        #     item = input("Enter item name: ").strip().lower()
        #     found = next((f for f in menu if f["name"].lower() == item), None)

        #     if not found:
        #         self.show_box("ERROR", ["Item not available"], "error")
        #         continue

        #     item_id = found["id"]
        #     stock = self.inventory.get_stock_by_id(item_id)

        #     if stock is None:
        #         self.show_box("ERROR", ["Item not in inventory"], "error")
        #         continue

        #     # Price logic
        #     if found["type"] == "dessert":
        #         price = found["price"]
        #         size = "single"
        #     else:
        #         size = input("Choose size (half/full): ").lower()
        #         if size == "half":
        #             price = found["half_price"]
        #         elif size == "full":
        #             price = found["full_price"]
        #         else:
        #             self.show_box("ERROR", ["Invalid size"], "error")
        #             continue

        #     try:
        #         quantity = int(input("Enter quantity: "))
        #         if quantity <= 0:
        #             raise ValueError
        #     except:
        #         handler.value_error()
        #         continue

        #     # 🔥 STOCK CHECK
        #     if quantity > stock:
        #         self.show_box("ERROR", [f"Only {stock} available"], "error")
        #         continue

        #     order_list.append({
        #         "id": item_id,
        #         "name": item,
        #         "type": found["type"],
        #         "size": size,
        #         "price": price,
        #         "quantity": quantity
        #     })

        #     more = input("Add more? (yes/no): ").lower()
        #     if more == "no":
        #         break

        # # 🔥 SAVE ORDER
        # order_data = {
        #     "order_id": order_id,
        #     "name": name,
        #     "items": order_list,
        #     "Status": "Pending"
        # }

        # orders.append(order_data)
        # self.db.write_data(self.order_file, orders)

        # # 🔥 REDUCE STOCK
        # for i in order_list:
        #     self.inventory.reduce_stock(i["id"], i["quantity"])

        # self.show_box("SUCCESS", ["Order placed", f"Order ID: {order_id}"])





from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Inventory.inventory_manager import InventoryManager
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()


class Order:
    def __init__(self):
        self.db = Data()
        self.inventory = InventoryManager()
        self.order_file = "App/Database/order.json"
        self.menu_file = "App/Database/menu.json"

    # ================= BOX UI =================
    def show_box(self, title, messages, status="success"):
        symbol = "✔" if status == "success" else "✖"
        print("\n╔" + "═"*35 + "╗")
        print(f"   {title}")
        print("╠" + "═"*35 + "╣")
        for msg in messages:
            print(f" [{symbol}] {msg}")
        print("╚" + "═"*35 + "╝")

    # ================= ORDER =================
    def order_item(self):
        handler = ExceptionHandler()
        menu = self.db.read_data(self.menu_file)
        orders = self.db.read_data(self.order_file)

        if not isinstance(menu, list):
            menu = []
        if not isinstance(orders, list):
            orders = []

        while True:
                name = input("Enter name: ").strip()

                if name.isalpha():
                    break
                else:
                    print("name should contain only alphabets")

        order_id = len(orders) + 1
        order_list = []

        while True:
            # 🔍 SEARCH
            keyword = input("\nSearch item (e.g. chicken, paneer): ").strip().lower()

            filtered = [f for f in menu if keyword in f["name"].lower()]

            if not filtered:
                self.show_box("ERROR", ["No items found"], "error")
                continue

            # ================= TABLE VIEW =================
            table = Table(title="🔍 SEARCH RESULTS", show_lines=True)

            table.add_column("ID", justify="center", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Type", style="green")
            table.add_column("Price", style="yellow")
            table.add_column("Stock", style="red")

            for item in filtered:
                stock = self.inventory.get_stock_by_id(item["id"])

                if item["type"].lower() == "dessert":
                    price = f"₹{item['price']}"
                else:
                    price = f"Half ₹{item['half_price']} / Full ₹{item['full_price']}"

                stock_text = str(stock) if stock is not None else "N/A"

                table.add_row(
                    str(item["id"]),
                    item["name"],
                    item["type"],
                    price,
                    stock_text
                )

            console.print(table)
            print("\n👉 Select ID only from above table")

            # ================= SELECT ITEM =================
            item_id_input = input("\nEnter item ID: ").strip()

            if not item_id_input.isdigit():
                self.show_box("ERROR", ["Invalid ID"], "error")
                continue

            item_id = int(item_id_input)

            found = next((f for f in filtered if f["id"] == item_id), None)

            if not found:
                self.show_box("ERROR", ["Invalid selection"], "error")
                continue

            # ================= STOCK CHECK =================
            stock = self.inventory.get_stock_by_id(item_id)

            if stock is None:
                self.show_box("ERROR", ["Item not in inventory"], "error")
                continue

            if stock == 0:
                self.show_box("ERROR", ["Item Out of Stock"], "error")
                continue

            # ================= PRICE =================
            if found["type"].lower() == "dessert":
                price = found["price"]
                size = "single"
            else:
                size = input("Choose size (half/full): ").strip().lower()

                if size == "half":
                    price = found["half_price"]
                elif size == "full":
                    price = found["full_price"]
                else:
                    self.show_box("ERROR", ["Invalid size"], "error")
                    continue

            # ================= QUANTITY =================
            qty_input = input("Enter quantity: ").strip()

            if not qty_input.isdigit():
                handler.value_error()
                continue

            quantity = int(qty_input)

            if quantity <= 0:
                self.show_box("ERROR", ["Quantity must be > 0"], "error")
                continue

            if quantity > stock:
                self.show_box("ERROR", [f"Only {stock} available"], "error")
                continue

            # ================= ADD ORDER =================
            order_list.append({
                "id": item_id,
                "name": found["name"],
                "type": found["type"],
                "size": size,
                "price": price,
                "quantity": quantity
            })

            more = input("Add more? (yes/no): ").strip().lower()

            if more == "no":
                break

        # ================= SAVE ORDER =================
        order_data = {
            "order_id": order_id,
            "name": name,
            "items": order_list,
            "Status": "Pending"
        }

        orders.append(order_data)
        self.db.write_data(self.order_file, orders)

        # ================= REDUCE STOCK =================
        for item in order_list:
            self.inventory.reduce_stock(item["id"], item["quantity"])

        # ================= SUCCESS =================
        console.print(Panel(
            f"[bold green]✅ Order placed successfully!\nOrder ID: {order_id}[/bold green]",
            title="SUCCESS",
            border_style="green"
        ))