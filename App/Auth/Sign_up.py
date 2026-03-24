from App.Utils.exception_handling import ExceptionHandler
from App.Database.db import Data
from App.Logs.logger import Logger
import uuid
import getpass


class Signup:

    def __init__(self):
        self.db = Data()
        self.file = "App/Database/users.json"
        self.logger = Logger()

    def signup_user(self):

        print("\n-----SIGN UP------\n")

        handler = ExceptionHandler()

        try:

            users = handler.handle_read(self.db.read_data, self.file)

            if not isinstance(users, list):
                users = []

            userid = str(uuid.uuid4().hex[:6])
            print("Id:", userid)

            
            while True:
                username = input("Enter username: ").strip()

                if username.isalpha():
                    break
                else:
                    print("Username should contain only alphabets")
                    self.logger.log_error("Invalid username entered during signup")

            
            while True:
                email = input("Enter Email: ")

                if "@" not in email or "." not in email:
                    print("Invalid email format")
                    self.logger.log_error(f"Invalid email format during signup: {email}")
                    continue

                duplicate = False

                for user in users:
                    if user["email"] == email:
                        print("Email already registered")
                        self.logger.log_error(f"Duplicate signup attempt: {email}")
                        duplicate = True
                        break

                if duplicate:
                    continue

                break

            
            while True:
                password = getpass.getpass("Enter password: ")

                if password.isalnum():
                    break
                else:
                    print("Password should contain letters and numbers only")
                    self.logger.log_error("Invalid password format during signup")

            user_data = {
                "userid": userid,
                "username": username,
                "email": email,
                "password": password,
                "role": "staff"
            }

            users.append(user_data)

            self.db.write_data(self.file, users)

            print("-------Signup successful----------")

            return user_data

        except Exception as e:

            print("Signup failed")
            self.logger.log_error(e)

            return None








          