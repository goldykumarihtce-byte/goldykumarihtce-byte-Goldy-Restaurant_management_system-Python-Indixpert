from App.Logs.logger import Logger


class ExceptionHandler:

    def __init__(self):
        self.logger = Logger()

    def handle_read(self, func, file):
        try:
            return func(file)

        except FileNotFoundError as e:
            self.logger.log_error(e)
            print("File not found")
            return []

        except Exception as e:
            self.logger.log_error(e)
            print("Error while reading file")
            return []

    
    def handle_write(self, func, file, data):
        try:
            func(file, data)

        except Exception as e:
            self.logger.log_error(e)
            print("Error while writing file")

    
    def value_error(self):
        print("Invalid input! Please enter correct value.")


    def handle_exception(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            self.logger.log_error(e)
            print("Something went wrong!")
            return None