from App.Database.db import Data
from App.Order.order import Order
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error
from App.Billing.bill import Ganerate_bill


class Menu:

    def __init__(self):
        self.handler = ExceptionHandler()
        self.db = Data()

        self.menu_file = "App/Database/menu.json"       
        self.order_file = "App/Database/order.json"    
        self.review_file = "App/Database/review.json"  

    def show_menu(self):

        menu = self.db.read_data(self.menu_file)

        if not menu:
            print("Menu is empty")
            return

        print("\n------ FOOD MENU🍞🍔🍗 ------")

        for i, item in enumerate(menu, start=1):
            print(f"{i}. {item['name']} - ₹{item['price']}")  

    
    def cancel_replace_order(self):
        try:
            orders = self.db.read_data(self.order_file)

            if not orders:
                print("No orders available")
                return

            order_id = input("Enter Order ID to cancel: ")

            found = None
            for order in orders:
                if str(order["Order_ID"]) == order_id:
                    found = order
                    break

            if not found:
                print("Order not found ")
                return

            
            found["Status"] = "Cancelled"
            print("Old order cancelled ")

            print("\nPlace new order ✅")

            menu = self.db.read_data(self.menu_file)

            item = input("Enter new item name: ").strip().lower()

            food_found = None
            for food in menu:
                if food["name"].lower() == item:
                    food_found = food
                    break

            if not food_found:
                print("Item not available ")
                return

            try:
                qty = int(input("Enter quantity: "))
            except ValueError:
                print("Invalid quantity")
                return

            
            if orders:
                new_id = max(o["Order_ID"] for o in orders) + 1
            else:
                new_id = 1

            new_order = {
                "Order_ID": new_id,
                "item": item,
                "Quantity": qty,
                "Status": "Pending"
            }

            orders.append(new_order)
            self.db.write_data(self.order_file, orders)

            print("\n✅ New Order Placed Successfully")
            print(f"🆔 New Order ID: {new_id}")

        except Exception as e:
            log_error(e)

    def add_review(self):
        try:
            reviews = self.db.read_data(self.review_file)

            if not isinstance(reviews, list):
                reviews = []

            name = input("Enter your name: ").strip()
            review_text = input("Enter your review: ").strip()

            if not name or not review_text:
                print("Name and Review cannot be empty")
                return
            
            review_id = len(reviews) + 1

            from datetime import datetime

            reviews.append({
                "Review_ID": review_id,
                "name": name,
                "review": review_text,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.db.write_data(self.review_file, reviews)

            print("✅Review added successfully")

        except Exception as e:
            log_error(e)

    def menu(self):

        while True:

            print("\n1. Show Menu🍔🍕🥤🍟")
            print("2. Order Items🛒")
            print("3. Cancel_Replace_Order❌-🍿")
            print("4. Add Review❇️")
            print("5. Back")
            print("-" * 30)

            option = input("Please select any option: ")

            if not option.isdigit():
                self.handler.invalid_choice()
                continue

            option = int(option)

            if option == 1:
                self.show_menu()

            elif option == 2:
                order = Order()              
                order.order_item()

            elif option == 3:
                self.cancel_replace_order()

            elif option == 4:
                orders = self.db.read_data(self.order_file)

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
                bill.generate_bill(found)   # ✅ correct
                                

            elif option == 5:
                self.add_review()

            elif option == 6:
                print("Exiting menu")
                break

            else:
                self.handler.invalid_choice()