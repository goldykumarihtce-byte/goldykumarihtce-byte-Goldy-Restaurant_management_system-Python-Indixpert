# from App.Utils.exception_handling import ExceptionHandler
# from App.Database.db import Data
# from App.Logs.logger import Logger
# import uuid
# import getpass


# class Signup:

#     def __init__(self):
#         self.db = Data()
#         self.file = "App/Database/users.json"
#         self.logger = Logger()

#     def signup_user(self):

#         print("\n-----SIGN UP------\n")

#         handler = ExceptionHandler()

#         try:

#             users = handler.handle_read(self.db.read_data, self.file)

#             if not isinstance(users, list):
#                 users = []

#             userid = str(uuid.uuid4().hex[:6])
#             print("Id:", userid)

            
#             while True:
#                 name = input("Enter name: ").strip()

#                 if name.isalpha():
#                     break
#                 else:
#                     print("name should contain only alphabets")
#                     self.logger.log_error("Invalid name entered during signup")


#             while True:
#                 address = input("Enter Address: ").strip()

#                 if address.isalpha():
#                     break
#                 else:
#                     print(" Address cannot be empty")
#                     self.logger.log_error("Invalid address entered during signup") 


#             while True:
#                     phone = input("Phone: ")
#                     if phone.isdigit() and len(phone) == 10:
#                         break
#                     else:
#                         print("Invalid phone number")
#                         self.logger.log_error("Invalid phone entered during signup")

#             while True:
#                 email = input("Enter Email: ")

#                 if "@" not in email or "." not in email:
#                     print("Invalid email format")
#                     self.logger.log_error(f"Invalid email format during signup: {email}")
#                     continue

#                 duplicate = False

#                 for user in users:
#                     if user["email"] == email:
#                         print("Email already registered")
#                         self.logger.log_error(f"Duplicate signup attempt: {email}")
#                         duplicate = True
#                         break

#                 if duplicate:
#                     continue

#                 break

            
#             while True:
#                 password = getpass.getpass("Enter password: ")

#                 if password.isalnum():
#                     break
#                 else:
#                     print("Password should contain letters and numbers only")
#                     self.logger.log_error("Invalid password format during signup")

#             user_data = {
#                 "userid": userid,
#                 "name": name,
#                 "address": address,
#                 "phone No": phone,
#                 "email": email,
#                 "password": password,
#                 "role": "staff"
#             }

#             users.append(user_data)

#             self.db.write_data(self.file, users)

#             print("-------Signup successful----------")

#             return user_data

#         except Exception as e:

#             print("Signup failed")
#             self.logger.log_error(e)

#             return None




from App.Utils.exception_handling import ExceptionHandler
from App.Database.db import Data
from App.Logs.logger import Logger
import uuid
import getpass

from rich.console import Console
from rich.panel import Panel


class Signup:

    def __init__(self):
        self.db = Data()
        self.file = "App/Database/users.json"
        self.logger = Logger()
        self.console = Console()

    # ================= BOX UI =================
    def show_box(self, title, message, status="success"):
        color = "green" if status == "success" else "red"
        self.console.print(Panel(f"[bold]{message}[/bold]", title=title, border_style=color))

    
    def signup_user(self):

        self.console.print(Panel("📝 SIGN UP FORM", style="cyan"))

        handler = ExceptionHandler()

        try:

            users = handler.handle_read(self.db.read_data, self.file)

            if not isinstance(users, list):
                users = []

            userid = str(uuid.uuid4().hex[:6])
            self.console.print(f"[bold yellow]User ID:[/bold yellow] {userid}")


            while True:
                name = input("Enter Name: ").strip()

                if name.replace(" ", "").isalpha():
                    break
                else:
                    self.show_box("ERROR", "Name should contain only alphabets", "error")
                    self.logger.log_error("Invalid name entered during signup")

           
            while True:
                address = input("Enter Address: ").strip()

                if len(address) >= 5:
                    break
                else:
                    self.show_box("ERROR", "Address must be at least 5 characters", "error")
                    self.logger.log_error("Invalid address entered")

           
            while True:
                phone = input("Phone: ").strip()

                if phone.isdigit() and len(phone) == 10:
                    break
                else:
                    self.show_box("ERROR", "Invalid phone number", "error")
                    self.logger.log_error("Invalid phone entered")

           
            while True:
                email = input("Enter Email: ").strip()

                if "@" not in email or "." not in email:
                    self.show_box("ERROR", "Invalid email format", "error")
                    continue

                duplicate = any(user["email"] == email for user in users)

                if duplicate:
                    self.show_box("ERROR", "Email already registered", "error")
                    continue

                break

           
            while True:
                password = getpass.getpass("Enter Password: ")

                if len(password) >= 6:
                    break
                else:
                    self.show_box("ERROR", "Password must be at least 6 characters", "error")

            
            user_data = {
                "userid": userid,
                "name": name,
                "address": address,
                "phone No": phone,
                "email": email,
                "password": password,
                "role": "staff"
            }

            users.append(user_data)
            self.db.write_data(self.file, users)

            self.show_box("SUCCESS", "Signup successful 🎉")

            return user_data

        except Exception as e:

            self.show_box("ERROR", "Signup failed", "error")
            self.logger.log_error(e)

            return None



          