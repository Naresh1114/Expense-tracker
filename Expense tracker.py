import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# File to store data
DATA_FILE = "expenses.csv"

# Ensure data file exists
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category", "Amount"])

# Add expense to the file
def add_expense():
    description = description_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if not description or not category or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description, category, amount])

    description_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Expense added successfully!")
    load_expenses()

# Load expenses into the table
def load_expenses():
    for row in expense_table.get_children():
        expense_table.delete(row)

    try:
        with open(DATA_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expense_table.insert("", tk.END, values=(row["Date"], row["Description"], row["Category"], row["Amount"]))
    except FileNotFoundError:
        pass

# Calculate total expenses
def calculate_total():
    total = 0
    try:
        with open(DATA_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            total = sum(float(row["Amount"]) for row in reader)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data found!")

# Initialize data file
initialize_data_file()

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")

# Input fields
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill=tk.X)

tk.Label(input_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
description_entry = tk.Entry(input_frame, width=20)
description_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
category_entry = tk.Entry(input_frame, width=20)
category_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Expense", command=add_expense, bg="lightgreen")
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Expense table
table_frame = tk.Frame(root, padx=10, pady=10)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Date", "Description", "Category", "Amount")
expense_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    expense_table.heading(col, text=col)
    expense_table.column(col, width=150)
expense_table.pack(fill=tk.BOTH, expand=True)

# Total button
total_button = tk.Button(root, text="Calculate Total", command=calculate_total, bg="lightblue")
total_button.pack(pady=10)

# Load initial data
load_expenses()

# Start the application
root.mainloop()
