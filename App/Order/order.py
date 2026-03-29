



from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler


class Order:
    def __init__(self):
        self.db = Data()
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

    # ================= ORDER ITEM =================
    def order_item(self):
        handler = ExceptionHandler()
        menu = self.db.read_data(self.menu_file)
        orders = self.db.read_data(self.order_file)

        if not isinstance(menu, list):
            menu = []
        if not isinstance(orders, list):
            orders = []

    
        username = input("Enter your username: ").strip()

        order_id = len(orders) + 1
        order_list = []

        while True:
            item = input("Enter item name: ").strip().lower()
            found = next((f for f in menu if f["name"].lower() == item), None)

            if not found:
                self.show_box("ERROR", ["Item not available"], "error")
                continue

            if found["type"] == "dessert":
                price = found["price"]
                size = "single"
            else:
                size = input("Choose size (half/full): ").lower()
                if size == "half":
                    price = found["half_price"]
                elif size == "full":
                    price = found["full_price"]
                else:
                    self.show_box("ERROR", ["Invalid size"], "error")
                    continue

            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    self.show_box("ERROR", ["Quantity must be > 0"], "error")
                    continue
            except ValueError:
                handler.value_error()
                continue

            order_list.append({
                "name": item,
                "type": found["type"],
                "size": size,
                "price": price,
                "quantity": quantity
            })

            more = input("Add more items? (yes/no): ").strip().lower()
            if more == "no":
                break

        order_data = {
            "order_id": order_id,
            "username": username,  
            "items": order_list,
            "Status": "Pending"
        }

        orders.append(order_data)
        self.db.write_data(self.order_file, orders)
        self.show_box("SUCCESS", ["Order placed successfully", f"Order ID: {order_id}"])