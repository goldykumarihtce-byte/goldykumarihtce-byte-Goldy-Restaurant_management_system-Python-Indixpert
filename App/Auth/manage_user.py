
from App.Auth.Sign_up import Signup
from App.Auth.Login import Login
from App.Utils.exception_handling import ExceptionHandler
from App.Dashboard.dashboard import User_dashboard


class Menu:

    def __init__(self):
        self.handler = ExceptionHandler()

    def user_menu(self):
        while True:

            print("\n=========== RESTAURANT MANAGEMENT SYSTEM ===============\n")
            print("1. Signup")
            print("2. Login")
            print("3. Exit")

            try:
                option = input("\nPlease select any option: ")

                if not option.isdigit():
                    print("Please enter a valid number")
                    continue

                option = int(option)

                if option == 1:
                    signup = Signup()
                    user = signup.signup_user()

                    if user:
                        return user

                elif option == 2:
                    login = Login()
                    user = login.login_user()

                    if user:
                        return user

                elif option == 3:
                    print("Exit")
                    return None

                else:
                    print("Invalid option")

            except Exception as e:
                self.handler.logger.log_error(e)
                print("Something went wrong!")



def run_auth():
    obj = Menu()

    while True:
        user = obj.user_menu()

        if not user:
                break

        obj1 = User_dashboard(user)
        obj1.dashboardUser()
        


