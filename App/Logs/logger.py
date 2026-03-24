import json
from datetime import datetime


class Logger:

    def __init__(self):
        self.file = "App/Database/error.json"

    def log_error(self, error):
        data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(error)
        }

        try:
            logs = self._read_logs()
            logs.append(data)
            self._write_logs(logs)

        except Exception as e:
            print("Logging failed:", e)

    def _read_logs(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_logs(self, logs):
        try:
            with open(self.file, "w") as f:
                json.dump(logs, f, indent=4)

        except Exception as e:
            print("Write failed:", e)


# 🔥 IMPORTANT: backward compatibility (NO CHANGE needed anywhere else)

_logger = Logger()

def log_error(error):
    _logger.log_error(error)


# import json
# from datetime import datetime


# class Logger:

#     def __init__(self):
#         self.file = "App/Database/error.json"

#     def log_error(self, error):
#         data = {
#             "time": str(datetime.now()),
#             "error": str(error)
#         }

#         try:
#             try:
#                 with open(self.file, "r") as f:
#                     logs = json.load(f)

#                     if not isinstance(logs, list):
#                         logs = []

#             except FileNotFoundError:
#                 logs = []

#             except json.JSONDecodeError:
#                 logs = []

#             logs.append(data)

#             with open(self.file, "w") as f:
#                 json.dump(logs, f, indent=4)

#         except Exception as e:
#             print("Logging failed:", e)
#import json
# from datetime import datetime

# def log_error(error):
#     data = {
#         "time": str(datetime.now()),
#         "error": str(error)
#     }

#     try:
#         with open("App/Database/error.json", "r") as f:
#             logs = json.load(f)
#     except:
#         logs = []

#     logs.append(data)

#     with open("App/Database/error.json", "w") as f:
#         json.dump(logs, f, indent=4)

