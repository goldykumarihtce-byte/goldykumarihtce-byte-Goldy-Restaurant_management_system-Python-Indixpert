from App.Dashboard.Admin_dashboard import Admin_dashboard
from App.Dashboard.Staff_dashboard import Staff_dashboard
from App.Logs.logger import log_error

class User_dashboard:

    def __init__(self, user):
        self.user = user

    def dashboardUser(self):
        try:
            role = self.user.get("role")  

            if role == "admin":
                admin = Admin_dashboard()
                admin.admin_dashboard_menu()

            elif role == "staff":
                
                staff = Staff_dashboard()
                staff.staffdashboard_menu()

            else:
                print("Invalid role")

        except Exception as e:
            print("Application error occurred", e)
            log_error(e)




