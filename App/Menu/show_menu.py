from App.Database.db import Data

def showMenu():
    db = Data()
    menu = db.read_data("App/Database/menu.json")

    if not menu:
        print("Menu is empty")
        return

    print("\n========== 🍽️ FOOD MENU 🍽️ ==========")

    print("\n🥦 VEG ITEMS")
    print("-" * 50)

    for item in menu:
        if item["type"] == "veg":
            print(f"{item['id']:2}. {item['name']:20} Half: ₹{item['half_price']} | Full: ₹{item['full_price']}")

    print("\n🍗 NON-VEG ITEMS")
    print("-" * 50)

    for item in menu:
        if item["type"] == "non-veg":
            print(f"{item['id']:2}. {item['name']:20} Half: ₹{item['half_price']} | Full: ₹{item['full_price']}")

    print("\n======================================\n")

# from App.Database.db import Data

# def showMenu():
#     db = Data()
#     menu = db.read_data("App/Database/menu.json")

#     if not menu:
#         print("Menu is empty")
#         return

#     for i, item in enumerate(menu, start=1):
#         print(f"{item['id']} . {item['name']} - ₹{item['price']}")