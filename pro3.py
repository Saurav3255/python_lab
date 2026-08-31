import pandas as pd

# -----------------------------------------
# 1. Read the input file
# -----------------------------------------

file_name = input("Enter the CSV/TSV file name: ")

# Automatically detect comma or tab separator
df = pd.read_csv(file_name, sep=None, engine="python")

print("\nDataset loaded successfully!")

# -----------------------------------------
# 2. Display dataset dimensions
# -----------------------------------------

rows, columns = df.shape

print("\nDataset Dimensions:")
print("Number of rows    :", rows)
print("Number of columns :", columns)

# -----------------------------------------
# 3. Display data types
# -----------------------------------------

print("\nData Types:")
print(df.dtypes)


# -----------------------------------------
# 4. Display first few records
# -----------------------------------------

print("\nFirst 5 Records:")
print(df.head())

# -----------------------------------------
# 5. Filter rows
# -----------------------------------------

print("\nAvailable columns:")
print(list(df.columns))

column_name = input("\nEnter the column name for filtering: ")

condition = input(
    "Enter condition (example: > 50, < 100, == 10): "
)

# Apply the condition
try:
    filtered_df = df.query(f"`{column_name}` {condition}")

    print("\nFiltered Data:")
    print(filtered_df)

except Exception as e:
    print("Invalid condition:", e)
    exit()

# -----------------------------------------
# 6. Save cleaned/filtered data
# -----------------------------------------

output_file = input(
    "\nEnter output file name (example: cleaned_data.csv): "
)

# Save as CSV or TSV depending on extension
if output_file.lower().endswith(".tsv"):
    filtered_df.to_csv(output_file, sep="\t", index=False)
else:
    filtered_df.to_csv(output_file, index=False)

print("\nFiltered data saved successfully to:", output_file)
