contacts = {}

while True:
    print("\n1.Add  2.View  3.Search  4.Update  5.Delete  6.Exit")
    ch = input("Choice: ")

    if ch == "1":
        name = input("Name: ").title()
        contacts[name] = input("Phone: ")
        print("Added")

    elif ch == "2":
        for name, phone in contacts.items():
            print(name, ":", phone)

    elif ch == "3":
        key = input("Search: ").lower()
        print([n for n in contacts.keys() if key in n.lower()])

    elif ch == "4":
        name = input("Name: ").title()
        if name in contacts:
            contacts[name] = input("New phone: ")

    elif ch == "5":
        name = input("Name: ").title()
        contacts.pop(name, None)

    elif ch == "6":
        break