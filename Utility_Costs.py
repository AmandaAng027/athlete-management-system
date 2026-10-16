"""
Module: Utility_Costs.py
Date of Creation: January 27, 2024
Author: Amanda Ang

Modification History:
- Jan. 27, 2024 - created widgets or the GUI
- Jan. 27, 2024 - added SQL queries, comments, and data validations
- Jan. 31, 2024 - edited variable names
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the UtilityCosts class, providing a user interface for editing utility costs.
It includes functions to populate a Treeview with financial utilities from the database, and edit cost details.

Functions:
- __init__(self, uc_win): Initializes the UtilityCosts class and creates the utility costs window.
- populate_treeview(self): Populates the Treeview with data from the UtilityCosts table in the database.
- tv_mouse_release(self, event): Handles selection in the Treeview and populates Entry widgets with selected row's data.
- edit_cost(self): Edits the description and amount of the selected cost and updates the database.
- open_utility_costs(): Function to open the Utility Costs window.

Global Variables:
None
"""

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *

from Data_Access_Layer import *


def open_utility_costs():
    """Function to open the Utility Costs Window"""
    uc_win = Tk()
    UtilityCosts(uc_win)
    uc_win.mainloop()


class UtilityCosts:
    def __init__(self, uc_win):
        """Initialize the Utility Costs class"""
        self.uc_win = uc_win
        self.uc_win.title("Edit Utility Costs")
        self.uc_win.geometry("1070x280")

        # Cost ID Label
        lbl_cost_id = Label(self.uc_win, text="Cost ID: ")
        self.cost_id = Label(self.uc_win, text="")

        # Amount Label
        lbl_amount = Label(self.uc_win, text="Amount: ")
        self.entry_amount = Entry(self.uc_win)

        # Description Label
        lbl_description = Label(self.uc_win, text="Description: ")
        self.txt_description = Text(self.uc_win, wrap=WORD, height=2, width=30)

        # Expense Type Label
        lbl_expense_type = Label(self.uc_win, text="Expense Type: ")
        self.expense_type = Label(self.uc_win, text="")

        # Edit Button
        btn_edit = Button(self.uc_win, text="Edit", width=20, command=self.edit_cost)

        # Create Treeview
        cols = ("Cost ID", "Expense Type", "Description", "Amount")
        self.tv = ttk.Treeview(master=self.uc_win, columns=cols, show="headings")
        self.tv.bind("<ButtonRelease-1>", self.tv_mouse_release)
        self.tv.heading("Cost ID", text="Cost ID")
        self.tv.heading("Expense Type", text="Expense Type")
        self.tv.heading("Description", text="Description")
        self.tv.heading("Amount", text="Amount")

        # Center the treeview
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=180, anchor="center")

        # Grid and layout of the widgets on the window
        pad = 3
        lbl_cost_id.grid(row=1, column=1, padx=pad, pady=pad)
        self.cost_id.grid(row=1, column=2, padx=pad, pady=pad)
        lbl_expense_type.grid(row=2, column=1, padx=pad, pady=pad)
        self.expense_type.grid(row=2, column=2, padx=pad, pady=pad)
        lbl_amount.grid(row=3, column=1, padx=pad, pady=pad)
        self.entry_amount.grid(row=3, column=2, padx=pad, pady=pad)
        lbl_description.grid(row=4, column=1, padx=pad, pady=pad)
        self.txt_description.grid(row=4, column=2, padx=pad, pady=pad)
        btn_edit.grid(row=6, column=1, columnspan=2,
                      padx=pad, pady=pad)
        self.tv.grid(row=1, column=3, rowspan=7,
                     padx=pad, pady=pad)

        # Initialize DataAccessLayer object
        self.dal = DataAccessLayer()
        self.populate_treeview()

    def populate_treeview(self):
        """Populate the Treeview with data from the UtilityCosts table in the database"""
        try:
            # Open connection to the database
            self.dal.open()

            # Retrieve data from the UtilityCosts table
            # Query here-------------------------------------------------------------------------------------------
            query = "SELECT * FROM UtilityCosts"
            data = self.dal.execute_query(query)

            # Insert retrieved data into the Treeview
            for row in data:
                # Format the data before inserting into the Treeview
                formatted_row = [row[0], row[1], row[2], f"{row[3]:.2f}"]
                self.tv.insert("", "end", values=formatted_row)

        except pyodbc.Error as ex:
            messagebox.showerror("Error", f"Database Error: {ex}")

        finally:
            # Close the database connection
            self.dal.close()

    def tv_mouse_release(self, event):
        """Handle selection in Treeview."""
        selected_item = self.tv.focus()
        item_values = self.tv.item(selected_item, 'values')

        # Populate Entry widgets with selected row's data
        self.entry_amount.delete(0, END)
        self.txt_description.delete(1.0, END)

        if item_values:
            # Insert values into respective Entry widgets
            self.cost_id.config(text=item_values[0])
            self.expense_type.config(text=item_values[1])
            self.txt_description.insert(1.0, item_values[2])
            self.entry_amount.insert(0, item_values[3])

    def edit_cost(self):
        """Edit the description and amount of the selected cost and update the database"""
        # Handle selection in the Treeview
        selected_item = self.tv.focus()
        item_values = self.tv.item(selected_item, 'values')

        # Check if a row is selected in the Treeview
        if not selected_item:
            messagebox.showerror("Error", "Please select a row in the Treeview.")
            return

        if item_values:
            # Extract the cost ID from the selected row in the Treeview
            cost_id = item_values[0]

            # Get the updated description and amount from the Entry widgets
            updated_description = self.txt_description.get("1.0", "end-1c")
            updated_amount = self.entry_amount.get()

            # Check if the updated description or amount is empty
            if not updated_description.strip() or not updated_amount.strip():
                messagebox.showerror("Error", "Please fill out all the fields.")
                return

            # Check if the updated amount is a valid number
            if not updated_amount.replace('.', '', 1).isdigit():
                messagebox.showerror("Error", "Amount must be a valid number.")
                return

            # Update the description and amount in the UtilityCosts table
            try:
                self.dal.open()

                # Update the description and amount in the UtilityCosts table
                # Query here-------------------------------------------------------------------------------------------
                query = "UPDATE UtilityCosts SET Description = ?, Amount = ? WHERE CostID = ?"
                self.dal.execute(query, updated_description, updated_amount, cost_id)
                self.dal.commit()

                # Update the Treeview with the edited values
                self.tv.item(selected_item, values=(cost_id, item_values[1], updated_description, updated_amount))

                messagebox.showinfo("Success", "Data updated successfully.")

            except pyodbc.Error as ex:
                messagebox.showerror("Error", f"Database Error: {ex}")
                self.dal.rollback()

            finally:
                # Close the database connection
                self.dal.close()
