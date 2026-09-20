# Program 4: Interactive Command-Line Task Scheduler
# Demonstrates Boolean logic, short-circuit evaluation,
# if-elif-else, nested conditions, loops and break.

tasks = []

while True:
    print("\n===== TASK SCHEDULER =====")
    print("1. Add Task")
    print("2. Run Tasks")
    print("3. Show Tasks")
    print("4. Exit")

    choice = input("Enter your choice: ")

    # Add a new task
    if choice == "1":
        task_name = input("Enter task name: ")

        enabled = input("Is the task enabled? (yes/no): ").lower() == "yes"
        condition = input("Is the task condition satisfied? (yes/no): ").lower() == "yes"

        task = {
            "name": task_name,
            "enabled": enabled,
            "condition": condition
        }

        tasks.append(task)
        print("Task added successfully!")

    # Run scheduled tasks
    elif choice == "2":
        if not tasks:
            print("No tasks are scheduled.")
        else:
            print("\n--- Running Tasks ---")

            for task in tasks:

                # Short-circuit evaluation using AND
                if task["enabled"] and task["condition"]:
                    print("Executing:", task["name"])

                # OR and NOT are also used
                elif not task["enabled"] or not task["condition"]:
                    print("Skipping:", task["name"])

                else:
                    print("Task cannot be processed.")

    # Display all tasks
    elif choice == "3":
        if not tasks:
            print("No tasks available.")
        else:
            print("\n--- Scheduled Tasks ---")

            for i, task in enumerate(tasks, start=1):
                print(
                    i,
                    ".",
                    task["name"],
                    "| Enabled:", task["enabled"],
                    "| Condition:", task["condition"]
                )

    # Exit
    elif choice == "4":
        print("Exiting Task Scheduler...")
        break

    # Invalid choice
    else:
        print("Invalid choice! Please enter 1, 2, 3 or 4.")