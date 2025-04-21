import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

conn = sqlite3.connect('data.db')

cur = conn.cursor()

root = tk.Tk()
root.title("Materials information")
root.geometry("800x600")

#creating a drop down menu so the user can select the table they want to view
choose_option = tk.StringVar(root)
choose_option.set("Select Table") # default value for the dropdown menu
options = ["Category", "Location", "Material", "Max_capacity"] #options for the dropdown menu
dropdown = tk.OptionMenu(root, choose_option, *options)
dropdown.pack() # like hw 1, this pack() puts the dropdown menu in the tinker window

#found online that treeview is used to display the data in a table format
tree = ttk.Treeview(root, show="headings") # hide the treeview headings which it the empty column
tree.pack_forget() # hide the treeview until a table is selected and the button is clicked

beginning_message = tk.Label(root, text="Welcome to the Materials Information System \n Please select a table from the dropdown menu to view its data.")
beginning_message.pack()

#creating a function to display the data in the treeview when the user selects a table from the dropdown menu
def show_table():
    # Clear the treeview if there is another table already displayed
    tree.delete(*tree.get_children())

    # Get the selected table from the dropdown menu
    selected_table = choose_option.get()

    if selected_table == "Select Table":
        messagebox.showerror("Error", "Please select a table to display.")
        return
    # Hide the message label when a table is selected
    beginning_message.pack_forget()

    tree.pack()  # Show the treeview
    #show the buttons for CRUD operations
    button_insert.pack()
    button_update.pack()
    button_delete.pack()
    # Execute a query to get the data from the selected table
    cur.execute(f"SELECT * FROM {selected_table}")

    # Get the column names from the cursor description
    columns = [description[0] for description in cur.description]

    # Create columns in the treeview based on the selected table's columns
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")
    #the anchor="w" makes the text in the column left aligned

    # Insert data into the treeview
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

#button to show the table when clicked
button_display = tk.Button(root, text="Display Table", command=show_table)
button_display.pack()

# Add CRUD and predefined SQL functionality

# Function to insert a new record into the selected table
        # Function to insert a new record into the selected table
def insert():
    selected_table = choose_option.get()
    if selected_table == "Select Table":
        messagebox.showerror("Error", "Please select a table to insert data.")
        return

    # Prompt user for input with a form
    new_data = simpledialog.askstring("Insert Record", f"Enter data for {selected_table} (comma-separated):")
    if not new_data:
        messagebox.showerror("Error", "No data entered. Please provide the required information.")
        return

    # Split the input and validate the number of values
    values = tuple(new_data.split(","))
    cur.execute(f"PRAGMA table_info({selected_table})")  # Get table column info
    column_count = len(cur.fetchall())  # Count the number of columns in the table

    if len(values) != column_count:
        messagebox.showerror("Error", f"Incorrect number of values. {selected_table} requires {column_count} values.")
        return

    # Insert the data into the table
    placeholders = ", ".join(["?" for _ in values])
    try:
        cur.execute(f"INSERT INTO {selected_table} VALUES ({placeholders})", values)
        conn.commit()
        messagebox.showinfo("Success", "Record inserted successfully!")
        show_table()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to insert record: {e}")

# Function to delete a selected record
def delete():
    selected_table = choose_option.get()
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return
    record = tree.item(selected_item)["values"]
    primary_key = record[0]  # Assuming the first column is the primary key
    cur.execute(f"DELETE FROM {selected_table} WHERE rowid = ?", (primary_key,))
    conn.commit()
    messagebox.showinfo("Success", "Record deleted successfully!")
    show_table()

# Function to update a selected record
def update():
    selected_table = choose_option.get()
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to update.")
        return
    record = tree.item(selected_item)["values"]
    updated_data = simpledialog.askstring("Update Record", f"Enter new data for {selected_table} (comma-separated):", initialvalue=",".join(map(str, record)))
    if updated_data:
        values = tuple(updated_data.split(","))
        placeholders = ", ".join([f"{col}=?" for col in tree["columns"]])
        cur.execute(f"UPDATE {selected_table} SET {placeholders} WHERE rowid = ?", (*values, record[0]))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        show_table()


#buttons for CRUD operations and it will only show up after the user selects a table from the dropdown menu and clicks the display button
button_insert = tk.Button(root, text="Insert Record", command=insert)
button_insert.pack_forget()

button_update = tk.Button(root, text="Update Record", command=update)
button_update.pack_forget()

button_delete = tk.Button(root, text="Delete Record", command=delete)
button_delete.pack_forget()


# Function to execute a predefined join query
def predefined_join_query():
    query = """
    SELECT Material.name AS Material, Location.location_name AS Location, Category.category_name AS Category
    FROM Material
    JOIN Location ON Material.location_id = Location.location_id
    JOIN Category ON Material.category_id = Category.category_id
    """
    cur.execute(query)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]

    # Clear the treeview and display the query results
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")
    for row in rows:
        tree.insert("", tk.END, values=row)



# Buttons for predefined SQL queries
button_join_query = tk.Button(root, text="Show Join Query Results", command=predefined_join_query)
button_join_query.pack()
#this is the main loop that runs the tkinter window and keeps it open
root.mainloop()

