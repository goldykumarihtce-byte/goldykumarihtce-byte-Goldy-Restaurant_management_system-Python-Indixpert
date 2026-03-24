
import json

class Data:

    def read_data(self, file):

        with open(file, "r") as f:
            data = json.load(f)

        return data


    def write_data(self, file, data):

        with open(file, "w") as f:
            json.dump(data, f, indent=4)