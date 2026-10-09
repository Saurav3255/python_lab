
"""
Program: In-Memory Inventory Tracker with Dictionary Merging
Author: Saurav 241492

Description:
Manages inventory across multiple store locations using dictionaries.
Uses key checks, get(), dictionary comprehension, and update()
to merge stock records and calculate total inventory.

Input: Product stock dictionaries for multiple stores.
Output: Merged inventory and total stock of each product.
"""

# Inventory of different store locations
store1 = {"Laptop": 10, "Mouse": 25, "Keyboard": 15}
store2 = {"Laptop": 5, "Mouse": 10, "Monitor": 8}
store3 = {"Laptop": 7, "Keyboard": 12, "Monitor": 4}


# Function to merge inventories
def merge_inventory(*stores):
    inventory = {}

    for store in stores:
        for product, quantity in store.items():
            if product in inventory:
                inventory[product] += quantity
            else:
                inventory[product] = quantity

    return inventory


# Function to safely get product stock
def get_stock(inventory, product):
    return inventory.get(product, 0)


# Function to filter products by minimum stock
def filter_inventory(inventory, minimum):
    return {
        product: quantity
        for product, quantity in inventory.items()
        if quantity >= minimum
    }


# Main program
if __name__ == "__main__":
    # Merge all store inventories
    inventory = merge_inventory(store1, store2, store3)

    print("Store 1 Inventory:", store1)
    print("Store 2 Inventory:", store2)
    print("Store 3 Inventory:", store3)

    print("\nMerged Inventory:", inventory)

    # Check product existence
    product = "Laptop"
    if product in inventory:
        print(f"{product} stock:", get_stock(inventory, product))
    else:
        print(f"{product} not found.")

    # Safely access a missing product
    print("Phone stock:", get_stock(inventory, "Phone"))

    # Filter products with at least 15 units
    print("Products with stock >= 15:", filter_inventory(inventory, 15))

    # Update inventory using another stock record
    new_stock = {"Laptop": 3, "Phone": 6}
    inventory.update({
        product: inventory.get(product, 0) + quantity
        for product, quantity in new_stock.items()
    })

    print("Updated Inventory:", inventory)