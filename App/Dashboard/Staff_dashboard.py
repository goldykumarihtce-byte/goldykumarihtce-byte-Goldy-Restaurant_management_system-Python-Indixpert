from App.Menu.start_menu import Menu
from App.Database.db import Data
from App.Utils.exception_handling import ExceptionHandler
from App.Logs.logger import log_error



class Staff_dashboard:

    def __init__(self):
        self.db = Data()
        self.orders_file = "App/Database/order.json"  
        self.handler = ExceptionHandler()

    def update_order_status(self):
        try:
            orders = self.db.read_data(self.orders_file)

            if not orders:
                print("No orders available")
                return

            order_id = input("Enter Order ID to update: ")

            found = None
            for order in orders:
                if str(order["Order_ID"]) == order_id:   
                    found = order
                    break

            if not found:
                print("Order not found")
                return

            print("1. Pending")
            print("2. Preparing")
            print("3. Delivered")
            print("4. Cancelled")

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
                print("Order status updated successfully")
            else:
                self.handler.invalid_choice()

        except Exception as e:
            print("Error:", e)
            log_error(e)

    def staffdashboard_menu(self):

        while True:

            print("\n----- Staff Dashboard ------")
            print("1. Order Place")
            print("2. Update Order Status")
            print("3. Back")

            choice = input("Enter a choice: ")

            if not choice.isdigit():
                self.handler.invalid_choice()
                continue

            choice = int(choice)

            if choice == 1:
                try:
                    ob = Menu()
                    ob.menu()


                except Exception as e:
                    log_error(e)

            elif choice == 2:
                self.update_order_status()

            elif choice == 3:
                print("Going back to main menu")
                break

            else:
                self.handler.invalid_choice()
