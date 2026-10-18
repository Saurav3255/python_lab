
"""
Program: Object Persistence Engine via Serialization
Author: Saurav 241492

Description:
Uses pickle and shelve to serialize Python objects,
save their states to disk, and restore them later.

Input: Object details and a menu choice.
Output: Saved object data or restored object states.
"""

import pickle
import shelve
import os


# A sample class whose objects will be persisted
class Student:
    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks

    def display(self):
        print(f"Name: {self.name}")
        print(f"Roll Number: {self.roll_no}")
        print(f"Marks: {self.marks}")

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, "
            f"roll_no={self.roll_no!r}, marks={self.marks!r})"
        )


# Save and restore objects using pickle
def save_with_pickle(student, filename="student.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(student, file)
    print("Object saved using pickle.")


def load_with_pickle(filename="student.pkl"):
    if not os.path.exists(filename):
        print("No pickle file found.")
        return None

    with open(filename, "rb") as file:
        student = pickle.load(file)

    print("Object restored using pickle.")
    return student


# Save and restore objects using shelve
def save_with_shelve(student, key="student"):
    with shelve.open("student_db") as database:
        database[key] = student
    print("Object saved using shelve.")


def load_with_shelve(key="student"):
    with shelve.open("student_db") as database:
        if key not in database:
            print("No saved object found in shelve.")
            return None

        student = database[key]

    print("Object restored using shelve.")
    return student


# Main program
if __name__ == "__main__":
    while True:
        print("\n===== OBJECT PERSISTENCE ENGINE =====")
        print("1. Create and save object using pickle")
        print("2. Load object using pickle")
        print("3. Create and save object using shelve")
        print("4. Load object using shelve")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter student name: ")
            roll_no = input("Enter roll number: ")

            try:
                marks = float(input("Enter marks: "))
                student = Student(name, roll_no, marks)
                save_with_pickle(student)
            except ValueError:
                print("Please enter valid marks.")

        elif choice == "2":
            student = load_with_pickle()
            if student is not None:
                student.display()

        elif choice == "3":
            name = input("Enter student name: ")
            roll_no = input("Enter roll number: ")

            try:
                marks = float(input("Enter marks: "))
                student = Student(name, roll_no, marks)
                save_with_shelve(student)
            except ValueError:
                print("Please enter valid marks.")

        elif choice == "4":
            student = load_with_shelve()
            if student is not None:
                student.display()

        elif choice == "5":
            print("Exiting Object Persistence Engine.")
            break

        else:
            print("Invalid choice. Please try again.")
