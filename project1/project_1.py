import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

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

#this is the main loop that runs the tkinter window and keeps it open
root.mainloop()

