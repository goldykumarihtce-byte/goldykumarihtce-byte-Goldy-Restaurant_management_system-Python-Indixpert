

from App.Auth.Sign_up import Signup
from App.Auth.Login import Login
from App.Utils.exception_handling import ExceptionHandler
from App.Dashboard.dashboard import User_dashboard

from rich.console import Console
from rich.panel import Panel


class Menu:

    def __init__(self):
        self.handler = ExceptionHandler()
        self.console = Console()

    def user_menu(self):
        while True:

            
            self.console.print(
                Panel.fit(
                    "[bold cyan]RESTAURANT MANAGEMENT SYSTEM[/bold cyan]\n\n"
                    "1. Signup 🆕\n"
                    "2. Login 🔐\n"
                    "3. Exit 🔚",
                    border_style="green"
                )
            )

            try:
                option = input("\nEnter your choice (1-3): ")

                if not option.isdigit():
                    self.console.print("[red]Please enter a valid number[/red]")
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
                    self.console.print("[yellow]Exiting...[/yellow]")
                    return None

                else:
                    self.console.print("[red]Invalid option[/red]")

            except Exception as e:
                self.handler.logger.log_error(e)
                self.console.print("[red]Something went wrong![/red]")



def run_auth():
    obj = Menu()

    while True:
        user = obj.user_menu()

        if not user:
            break

        obj1 = User_dashboard(user)
        obj1.dashboardUser()