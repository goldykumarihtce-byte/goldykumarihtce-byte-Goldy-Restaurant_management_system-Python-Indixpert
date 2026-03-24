from datetime import datetime

class Ganerate_bill:

    def generate_bill(self, order):

        print("\n============== BILL ==============")
        print(f"Order ID : {order.get('order_id')}")
        print(f"Status   : {order.get('Status')}")

        print("\nItems:")
        print("-" * 40)

        total = 0

        for item in order.get("items", []):
            name = item.get("name")
            size = item.get("size")
            price = item.get("price")
            qty = item.get("quantity")

            item_total = price * qty
            total += item_total

            print(f"{name:15} ({size}) {qty} x ₹{price} = ₹{item_total}")

        print("-" * 40)
        print(f"Total Amount : ₹{total}")
        print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=================================\n")
# from datetime import datetime
# import json
# class Ganerate_bill:

#     def __init__(self):
#         self.file_json = "App/Database/bills.json"
#         self.file_txt = "App/Database/bill.txt"

#     def generate_bill(self, order):
#         print("\n============== BILL ==============")

#         print(f"Order ID : {order.get('order_id')}")
#         print(f"Customer : {order.get('username')}")
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         print(f"Date            : {date}")
#         print("-------------------------------------------")

#         total = 0

#         for item in order.get("items",[]):
#             name = item.get("name")
#             price = item.get("price")
#             qty = item.get("quantity")

#             item_total = price * qty
#             total += item_total


#             print(f"{name} * {qty} = Rs{item_total}")

#         print("----------------------------------------------")

#         gst = total * 0.18 

#         discount = 0
#         if total > 500:
#             discount = total + gst - discount

#         final_total = total + gst - discount

#         print(f"Subtotal        =Rs{total}")
#         print(f"GST (18%)       ={gst:.2f}")
#         print(f"Discount        =Rs{discount:.2f}") 
#         print("------------------------------------------")

#         print(f"final Amount    ={final_total:.2f}")

#         print("\nSelect Payment Method:")
#         print("1. Cash")
#         print("2. UPI")

#         choice = int(input("Enter choice:"))

#         if choice == 1:
#             payment = "Cash"

#         elif choice == 2:
#             payment = "UPI"

#         else:
#             print("Invalid choice")

#         print("============THANK YOU=================\n")

#         bill_data = {
#             "order_id": order.get("order_id"),
#             "username": order.get("username"),
#             "date": date,
#             "items": order.get("items"),
#             "subtotal": total,
#             "gst": gst,
#             "discount": discount,
#             "final_total": final_total,
#             "payment": payment
#         }

#         self.save_json(bill_data)
#         self.save_txt(bill_data)

#         return final_total

#     # 🔹 Save JSON
#     def save_json(self, bill):
#         try:
#             try:
#                 with open(self.file_json, "r") as f:
#                     data = json.load(f)
#             except:
#                 data = []

#             data.append(bill)

#             with open(self.file_json, "w") as f:
#                 json.dump(data, f, indent=4)

#         except Exception as e:
#             print("Error saving JSON:", e)

#     # 🔹 Save TXT
#     def save_txt(self, bill):
#         try:
#             with open(self.file_txt, "a") as f:
#                 f.write("\n=========== BILL ===========\n")
#                 f.write(f"Order ID: {bill['order_id']}\n")
#                 f.write(f"Customer: {bill['username']}\n")
#                 f.write(f"Date: {bill['date']}\n")

#                 for item in bill["items"]:
#                     f.write(f"{item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}\n")

#                 f.write(f"Subtotal: ₹{bill['subtotal']}\n")
#                 f.write(f"GST: ₹{bill['gst']:.2f}\n")
#                 f.write(f"Discount: ₹{bill['discount']:.2f}\n")
#                 f.write(f"Final: ₹{bill['final_total']:.2f}\n")
#                 f.write(f"Payment: {bill['payment']}\n")
#                 f.write("============================\n")

#         except Exception as e:
#             print("Error saving TXT:", e)



