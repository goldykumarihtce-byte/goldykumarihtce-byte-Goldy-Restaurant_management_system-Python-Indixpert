# from App.Utils.exception_handling import ExceptionHandler
# from App.Database.db import Data
# from App.Logs.logger import Logger
# import getpass

# class Login:

#     def __init__(self):
#         self.db = Data()
#         self.file = "App/Database/users.json"
#         self.logger = Logger()

#     def login_user(self):

#         print("\n------LOGIN-------\n")

#         handler = ExceptionHandler()
#         users = handler.handle_read(self.db.read_data, self.file)

#         if not isinstance(users, list):
#             users = []

#         try:
#             while True:   

#                 email = input("Enter a email: ")

#                 if "@" not in email or "." not in email:
#                     print("Invalid email format, try again!")
#                     self.logger.log_error("Invalid email format entered")
#                     continue   

#                 found_user = None
#                 for user in users:
#                     if user["email"] == email:
#                         found_user = user
#                         break

#                 if not found_user:
#                     print("User not found. Please try again.")
#                     self.logger.log_error(f"Login attempt for non-existing user: {email}")
#                     continue   


#                 while True:
#                     password = getpass.getpass("Enter a password: ")

#                     if found_user["password"] == password:
#                         print("--------Login successful----------")
#                         print("Role:", found_user["role"])
#                         return found_user   

#                     else:
#                         print("Incorrect password, try again!")
#                         self.logger.log_error(f"Incorrect password attempt for email: {email}")

#         except Exception as e:
#             print("Login error occurred:", e)
#             self.logger.log_error(e)
#             return None




from App.Utils.exception_handling import ExceptionHandler
from App.Database.db import Data
from App.Logs.logger import Logger
import getpass

from rich.console import Console
from rich.panel import Panel


class Login:

    def __init__(self):
        self.db = Data()
        self.file = "App/Database/users.json"
        self.logger = Logger()
        self.console = Console()

    # ================= BOX UI =================
    def show_box(self, title, message, status="success"):
        color = "green" if status == "success" else "red"
        self.console.print(Panel(f"[bold]{message}[/bold]", title=title, border_style=color))

    # ================= LOGIN =================
    def login_user(self):

        self.console.print(Panel("🔐 LOGIN FORM", style="cyan"))

        handler = ExceptionHandler()
        users = handler.handle_read(self.db.read_data, self.file)

        if not isinstance(users, list):
            users = []

        try:
            while True:

                email = input("Enter Email: ").strip()

                if "@" not in email or "." not in email:
                    self.show_box("ERROR", "Invalid email format", "error")
                    self.logger.log_error("Invalid email format entered")
                    continue

                
                found_user = next((user for user in users if user["email"] == email), None)

                if not found_user:
                    self.show_box("ERROR", "User not found", "error")
                    self.logger.log_error(f"Login attempt for non-existing user: {email}")
                    continue

                
                while True:
                    password = getpass.getpass("Enter Password: ")

                    if found_user["password"] == password:
                        self.show_box("SUCCESS", "Login successful 🎉")
                        self.console.print(f"[bold yellow]Role:[/bold yellow] {found_user['role']}")
                        return found_user

                    else:
                        self.show_box("ERROR", "Incorrect password", "error")
                        self.logger.log_error(f"Incorrect password attempt for email: {email}")

        except Exception as e:
            self.show_box("ERROR", "Login failed", "error")
            self.logger.log_error(e)
            return None