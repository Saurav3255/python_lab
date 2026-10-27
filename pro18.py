
"""
Program: GUI Student Record Manager with File Storage
Author: Saurav 241492

Description:
Creates a Tkinter GUI to manage student records using
Entry, Radiobutton, Checkbutton, Text, messagebox, and filedialog.
Records are stored persistently in a JSON file.

Input: Student details, gender, course, and hobbies.
Output: Student records displayed in the GUI and saved to disk.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os


class StudentRecordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")
        self.root.geometry("950x650")

        self.records = {}
        self.storage_file = os.path.abspath("students.json")

        self.name_var = tk.StringVar()
        self.roll_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Male")
        self.course_var = tk.StringVar(value="CSE")
        self.sports_var = tk.BooleanVar()
        self.music_var = tk.BooleanVar()
        self.reading_var = tk.BooleanVar()

        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        form = ttk.LabelFrame(self.root, text="Student Details", padding=10)
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Roll Number:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.roll_var, width=25).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Name:").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.name_var, width=25).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Age:").grid(row=2, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.age_var, width=25).grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Gender:").grid(row=0, column=2, sticky="w")
        gender_frame = ttk.Frame(form)
        gender_frame.grid(row=0, column=3, sticky="w")

        for gender in ("Male", "Female", "Other"):
            ttk.Radiobutton(
                gender_frame, text=gender,
                variable=self.gender_var, value=gender
            ).pack(side="left", padx=3)

        ttk.Label(form, text="Course:").grid(row=1, column=2, sticky="w")
        ttk.Combobox(
            form, textvariable=self.course_var,
            values=("CSE", "IT", "ECE", "ME", "Civil", "Other"),
            state="readonly", width=20
        ).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Hobbies:").grid(row=2, column=2, sticky="w")
        hobby_frame = ttk.Frame(form)
        hobby_frame.grid(row=2, column=3, sticky="w")

        ttk.Checkbutton(
            hobby_frame, text="Sports", variable=self.sports_var
        ).pack(side="left")
        ttk.Checkbutton(
            hobby_frame, text="Music", variable=self.music_var
        ).pack(side="left")
        ttk.Checkbutton(
            hobby_frame, text="Reading", variable=self.reading_var
        ).pack(side="left")

        ttk.Label(form, text="Address / Notes:").grid(
            row=3, column=0, sticky="nw"
        )
        self.notes_text = tk.Text(form, width=65, height=3)
        self.notes_text.grid(
            row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w"
        )

        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", padx=10)

        actions = [
            ("Add / Update", self.add_or_update),
            ("Search", self.search_record),
            ("Delete", self.delete_record),
            ("Clear Form", self.clear_form),
            ("Open File", self.open_file),
            ("Save As", self.save_as),
        ]

        for label, command in actions:
            ttk.Button(buttons, text=label, command=command).pack(
                side="left", padx=4, pady=5
            )

        table_frame = ttk.LabelFrame(
            self.root, text="Saved Student Records", padding=8
        )
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("roll", "name", "age", "gender", "course", "hobbies")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        headings = {
            "roll": "Roll Number",
            "name": "Name",
            "age": "Age",
            "gender": "Gender",
            "course": "Course",
            "hobbies": "Hobbies",
        }

        for col, heading in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def get_form_data(self):
        roll = self.roll_var.get().strip()
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()

        if not roll or not name or not age_text:
            raise ValueError("Roll number, name, and age are required.")

        try:
            age = int(age_text)
            if not 1 <= age <= 120:
                raise ValueError
        except ValueError:
            raise ValueError("Age must be an integer between 1 and 120.")

        hobbies = [
            hobby for hobby, selected in (
                ("Sports", self.sports_var.get()),
                ("Music", self.music_var.get()),
                ("Reading", self.reading_var.get()),
            ) if selected
        ]

        return {
            "roll": roll,
            "name": name,
            "age": age,
            "gender": self.gender_var.get(),
            "course": self.course_var.get(),
            "hobbies": hobbies,
            "notes": self.notes_text.get("1.0", "end-1c").strip(),
        }

    def add_or_update(self):
        try:
            record = self.get_form_data()
        except ValueError as error:
            messagebox.showerror("Invalid Details", str(error))
            return

        self.records[record["roll"]] = record
        self.save_records()
        self.refresh_table()
        messagebox.showinfo("Success", "Student record saved.")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for roll, record in sorted(self.records.items()):
            self.tree.insert("", "end", iid=roll, values=(
                roll,
                record["name"],
                record["age"],
                record["gender"],
                record["course"],
                ", ".join(record["hobbies"]),
            ))

    def select_record(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        record = self.records.get(selected[0])
        if not record:
            return

        self.clear_form()
        self.roll_var.set(record["roll"])
        self.name_var.set(record["name"])
        self.age_var.set(str(record["age"]))
        self.gender_var.set(record["gender"])
        self.course_var.set(record["course"])

        self.sports_var.set("Sports" in record["hobbies"])
        self.music_var.set("Music" in record["hobbies"])
        self.reading_var.set("Reading" in record["hobbies"])

        self.notes_text.insert("1.0", record.get("notes", ""))

    def search_record(self):
        roll = self.roll_var.get().strip()

        if not roll:
            messagebox.showwarning(
                "Search", "Enter a roll number to search."
            )
            return

        if roll not in self.records:
            messagebox.showinfo("Search", "Student record not found.")
            return

        self.tree.selection_set(roll)
        self.tree.focus(roll)
        self.tree.see(roll)
        self.select_record()

    def delete_record(self):
        roll = self.roll_var.get().strip()

        if roll not in self.records:
            messagebox.showwarning(
                "Delete", "Enter or select a valid roll number."
            )
            return

        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete the record for roll number {roll}?"
        ):
            del self.records[roll]
            self.save_records()
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Deleted", "Student record deleted.")

    def clear_form(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.course_var.set("CSE")
        self.sports_var.set(False)
        self.music_var.set(False)
        self.reading_var.set(False)
        self.notes_text.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    def save_records(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as file:
                json.dump(self.records, file, indent=4)
        except OSError as error:
            messagebox.showerror("Save Error", str(error))

    def load_records(self):
        if not os.path.exists(self.storage_file):
            self.refresh_table()
            return

        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Invalid record file structure.")

            for roll, record in data.items():
                if (
                    not isinstance(record, dict)
                    or record.get("roll") != roll
                    or not isinstance(record.get("name"), str)
                    or not isinstance(record.get("age"), int)
                    or isinstance(record.get("age"), bool)
                    or not 1 <= record["age"] <= 120
                    or not isinstance(record.get("hobbies"), list)
                    or not all(isinstance(h, str) for h in record["hobbies"])
                ):
                    raise ValueError("Invalid student record format.")

            self.records = data
            self.refresh_table()

        except (OSError, json.JSONDecodeError, ValueError) as error:
            messagebox.showerror("Load Error", str(error))

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Student Records",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Invalid record file structure.")

            for roll, record in data.items():
                if (
                    not isinstance(record, dict)
                    or record.get("roll") != roll
                    or not isinstance(record.get("name"), str)
                    or not isinstance(record.get("age"), int)
                    or isinstance(record.get("age"), bool)
                    or not 1 <= record["age"] <= 120
                    or not isinstance(record.get("hobbies"), list)
                    or not all(isinstance(h, str) for h in record["hobbies"])
                ):
                    raise ValueError("Invalid student record format.")

            self.records = data
            self.storage_file = path
            self.refresh_table()
            messagebox.showinfo("Success", "Records loaded successfully.")

        except (OSError, json.JSONDecodeError, ValueError) as error:
            messagebox.showerror("Open Error", str(error))

    def save_as(self):
        path = filedialog.asksaveasfilename(
            title="Save Student Records As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if not path:
            return

        previous_path = self.storage_file
        self.storage_file = path
        self.save_records()

        if not os.path.exists(path):
            self.storage_file = previous_path
            return

        messagebox.showinfo("Success", f"Records saved to:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordManager(root)
    root.mainloop()
