import sqlite3
import tkinter as tk

conn.sqlite3.connect('data.db')

cur = conn.cursor()

root = tk.Tk()
root.title("Database GUI")

#creating a drop down menu so the user can select the table they want to view
choose_option = tk.StringVar(root)
choose_option.set("Select Table") # default value for the dropdown menu
options = ["Category", "Location", "Material", "Max_capacity"] #options for the dropdown menu
dropdown = tk.OptionMenu(root, choose_option, options[0], *options)
dropdown.pack() # like hw 1, this pack() puts the dropdown menu in the tinker window