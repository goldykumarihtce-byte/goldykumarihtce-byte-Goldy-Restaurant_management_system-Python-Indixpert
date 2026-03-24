from App.Database.db import Data
from App.Menu.show_menu import showMenu

from App.Utils.exception_handling import ExceptionHandler


class Order:
    def __init__(self):
        self.db=Data()
        self.order_file= "App/Database/order.json"
        self.menu_file = "App/Database/menu.json"

        self.current_order = []


    def showmenu(self):

        menu = self.db.read_data(self.menu_file)

        if not isinstance(menu, list) or not menu:
            print("Menu is empty")
            return

        print("\n------FOOD MENU------")

        for item in menu:
            print(f"{item['name']:25} Rs{item['price']}")    

    def menu(self):
        while True:
            print("1. Show Menu")
            print("2. Order Items")
            print("3. Update Order")
            print("4. Add Review")
            print("5. Exit")
            print("-"*30)

            try:
                option=int(input("Please select any option:"))

            except ValueError:
                print("Enter a valid number")    
                continue

            if option==1:
                self.showmenu()

            elif option==2:
                
                self.order_item()


            elif option==3:
              
                self.update_order()    

            elif option==4:
                print("Exiting menu....")    

            else:
                print("Invalid option") 


    def update_order(self):

        orders = self.db.read_data(self.order_file)

        if not orders:
            print("No orders available")
            return

        order_id = input("Enter Order ID: ")

        found = None
        for o in orders:
            if str(o["Order_ID"]) == order_id:
                found = o
                break

        if not found:
            print("Order not found")
            return

        print("\nCurrent Order:")
        print(found["item"], "-", found["Quantity"])

        confirm = input("Do you want to cancel and replace order? (yes/no): ")

        if confirm.lower() == "yes":

            found["Status"] = "Cancelled"   
            print("Old order cancelled ")

            print("\nPlace new order")
            self.order_item()   

            self.db.write_data(self.order_file, orders)  

        else:
            print("Order not updated")


    def order_item(self):

        handler = ExceptionHandler()

        menu = self.db.read_data(self.menu_file)
        orders = self.db.read_data(self.order_file)

        if not isinstance(menu, list):
            menu = []

        if not isinstance(orders, list):
            orders = []

        order_id = len(orders) + 1
        order_list = []

        while True:
            print("\n***** ORDER PLEASE ******")

            item = input("Enter item name: ").strip().lower()

            found = None
            for food in menu:
                if food["name"].lower() == item:
                    found = food
                    break

            if not found:
                print("Item not available")
                continue

            size = input("Choose size (half/full): ").lower()

            if size == "half":
                price = found["half_price"]
            elif size == "full":
                price = found["full_price"]
            else:
                print("Invalid size")
                continue

            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    continue
            except ValueError:
                handler.value_error()
                continue

            order_list.append({
                "name": item,
                "size": size,
                "price": price,
                "quantity": quantity
            })

            more = input("Do you want to order more? (yes/no): ").lower()
            if more == "no":
                break

        order_data = {
            "order_id": order_id,
            "items": order_list,
            "Status": "Pending"
        }

        orders.append(order_data)
        self.db.write_data(self.order_file, orders)

        print("\nOrder Successful ✅")
        print(f"🆔 Order ID: {order_id}")        

    # def order_item(self):

    #     handler = ExceptionHandler()

    #     menu = self.db.read_data(self.menu_file)
    #     orders = self.db.read_data(self.order_file)

    #     if not isinstance(menu, list):
    #         menu = []

    #     if not isinstance(orders, list):
    #         orders = []

    #     order_id = len(orders) + 1

    #     order_list = []   

    #     while True:
    #         print("\n***** ORDER PLEASE ******")

    #         item = input("Enter item name: ").strip().lower()

    #         found = None

    #         for food in menu:
    #             if food["name"].lower() == item:
    #                 found = food
    #                 break

    #         if not found:
    #             print("Item not available")
    #             continue

    #         print("Price:", found["price"])

    #         try:
    #             quantity = int(input("Enter quantity: "))

    #             if quantity <= 0:
    #                 print("Quantity must be greater than 0")
    #                 continue   

    #         except ValueError:
    #             handler.value_error()
    #             continue

            
    #         order_list.append({
    #             "name": item,
    #             "price": found["price"],
    #             "quantity": quantity
    #         })

    #         more = input("Do you want to order more? (yes/no): ").lower().strip()

    #         if more == "no":
    #             break

        
    #     order_data = {
    #         "order_id": order_id,   
    #         "items": order_list,
    #         "Status": "Pending"
    #     }

    #     orders.append(order_data)

    #     self.db.write_data(self.order_file, orders)

    #     print("\nOrder Successful ✅")
    #     print(f"🆔 Order ID: {order_id}")