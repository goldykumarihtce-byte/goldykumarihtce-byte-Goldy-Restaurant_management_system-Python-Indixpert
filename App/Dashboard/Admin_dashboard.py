from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error
from App.Order.order import Order
from App.Billing.bill import Ganerate_bill


class Admin_dashboard:

    def __init__(self):

        self.db = Data()
        self.file = "App/Database/menu.json"
        self.orders_file = "App/Database/order.json"

        self.handler = ExceptionHandler()

        self.menu = self.db.read_data(self.file)

        if not isinstance(self.menu, list):
            self.menu = []
            self.db.write_data(self.file, self.menu)

    
    def show_menu(self):

        menu = self.db.read_data(self.file)

        print("\n========== 🍽️ FOOD MENU 🍽️ ==========")

        print("\n🥦 VEG ITEMS")
        print("-"*50)

        for item in menu:
            if item["type"] == "veg":
                print(f"{item['name']:20} Half: ₹{item['half_price']} | Full: ₹{item['full_price']}")

        print("\n🍗 NON-VEG ITEMS")
        print("-"*50)

        for item in menu:
            if item["type"] == "non-veg":
                print(f"{item['name']:20} Half: ₹{item['half_price']} | Full: ₹{item['full_price']}")

    
    def admin_dashboard_menu(self):

        while True:

            print("\n-------ADMIN DASHBOARD--------")
            print("1. Add Item")
            print("2. Update Item")
            print("3. Delete Item")
            print("4. View Menu")
            print("5. Order")
            print("6. Update Order")
            print("7. Generate Bill")
            print("8. Back")

            choice = input("\nEnter choice: ")

            if not choice.isdigit():
                self.handler.invalid_choice()
                continue

            choice = int(choice)

            
            if choice == 1:

                try:
                    name = input("Enter item name: ").strip().lower()

                
                    for item in self.menu:
                        if item["name"].lower() == name:
                            print("Item already exists")
                            break
                    else:
                        item_type = input("Enter type (veg/non-veg): ").lower()
                        half_price = int(input("Enter half price: "))
                        full_price = int(input("Enter full price: "))

                        item = {
                            "name": name,
                            "type": item_type,
                            "half_price": half_price,
                            "full_price": full_price
                        }

                        self.menu.append(item)
                        self.db.write_data(self.file, self.menu)

                        print("✅ Item Added Successfully")

                except ValueError as e:
                    self.handler.value_error()
                    log_error(e)

            
            elif choice == 2:

                name = input("Enter item name to update: ").lower()

                found = False

                for item in self.menu:
                    if item["name"].lower() == name:

                        try:
                            item["type"] = input("Enter new type (veg/non-veg): ").lower()
                            item["half_price"] = int(input("Enter new half price: "))
                            item["full_price"] = int(input("Enter new full price: "))
                        except ValueError as e:
                            self.handler.value_error()
                            log_error(e)
                            continue

                        found = True
                        break

                if found:
                    self.db.write_data(self.file, self.menu)
                    print("✅ Item Updated Successfully")
                else:
                    print("Item not found")

            
            elif choice == 3:

                name = input("Enter item name to delete: ").lower()

                new_menu = [item for item in self.menu if item["name"].lower() != name]

                if len(new_menu) == len(self.menu):
                    print("Item not found")
                else:
                    self.menu = new_menu
                    self.db.write_data(self.file, self.menu)
                    print("✅ Item Deleted")

            elif choice == 4:
                self.show_menu()

            
            elif choice == 5:
                order = Order()
                order.order_item()

            
            elif choice == 6:
                order = Order()
                order.update_order()

            
            elif choice == 7:

                try:
                    orders = self.db.read_data(self.orders_file)

                    if not orders:
                        print("No orders available")
                        continue

                    order_id = input("Enter Order ID: ")

                    found = None
                    for order in orders:
                        if str(order.get("order_id")) == order_id:
                            found = order
                            break

                    if not found:
                        print("Order not found")
                        continue

                    bill = Ganerate_bill()
                    bill.generate_bill(found)

                except Exception as e:
                    print("Error generating bill:", e)
                    log_error(e)

            elif choice == 8:
                return

            else:
                self.handler.invalid_choice()