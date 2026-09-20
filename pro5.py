import os
import sys

print("Current:", os.getcwd())
print("Files:", os.listdir())

folder = input("Enter folder: ")

if os.path.isdir(folder):
    os.chdir(folder)

workspace = "workspace"
os.makedirs(workspace, exist_ok=True)

ext = input("Enter extension (.txt): ")

print("Matching files:")
for f in os.listdir():
    if f.endswith(ext):
        print(f)

file = sys.argv[1] if len(sys.argv) > 1 else input("Log file: ")

try:
    with open(file, "r") as f:
        print("\nContent:", f.read())

except FileNotFoundError:
    with open(file, "w") as f:
        f.write("New log created.\n")
    print("New log created.")

print("Program completed.")