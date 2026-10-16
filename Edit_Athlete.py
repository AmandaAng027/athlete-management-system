"""
Module: Edit_Athlete.py
Date of Creation: January 5, 2024
Author: Amanda Ang

Modification History:
- Jan. 5, 2024 - created widgets or the GUI
- Jan. 10, 2024 - added functional buttons and SQL queries
- Jan. 12, 2024 - organised the codes and naming conventions
- Jan. 15, 2024 - added docstrings
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the EditAthlete class, which represents the Edit Athlete window
in the North Sussex Judo application. It includes functionality for displaying athlete information,
editing athlete details, and updating the database with the changes.

Functions:
- __init__(self, ea_win): Initializes the EditAthlete class.
- display_athlete_data(self): Displays athletes' information in the Treeview.
- tv_mouse_release(self, event): Handles selection in Treeview.
- get_weight_class(self, weight): Gets the weight class based on the provided weight.
- edit_athlete(self): Edits athlete information and updates the database.
- reset(self): Resets Entry widgets and Treeview.

Global Variables:
None
"""

from tkinter import *
from tkinter import ttk, messagebox

from Data_Access_Layer import *


def open_edit_athlete():
    """Function to create and open the Edit Athlete window."""
    ea_win = Tk()
    EditAthlete(ea_win)
    ea_win.mainloop()


class EditAthlete:
    def __init__(self, ea_win):
        """Initialize the EditAthlete class."""
        self.ea_win = ea_win
        self.ea_win.title("Edit Athlete")
        self.ea_win.geometry("840x300")

        # Athlete ID Label
        lbl_athlete_id = Label(self.ea_win, text="Athlete ID: ")
        self.athlete_id = Label(self.ea_win, text="")

        # First Name Label
        lbl_first_name = Label(self.ea_win, text="First Name: ")
        self.entry_first_name = Entry(self.ea_win)

        # Last Name Label
        lbl_last_name = Label(self.ea_win, text="Last Name: ")
        self.entry_last_name = Entry(self.ea_win)

        # Weight Label
        lbl_weight = Label(self.ea_win, text="Weight: ")
        self.entry_weight = Entry(self.ea_win)

        # Weight Class ID Label
        lbl_weightclass_id = Label(self.ea_win, text="Weight Class ID: ")
        self.weightclass_id = Label(self.ea_win, text="")

        # Edit Athlete Button
        btn_edit = Button(self.ea_win, text="Edit Athlete", width=20,
                          command=self.edit_athlete)

        # Treeview for displaying Athlete information and handling selection
        cols = ("Athlete ID", "First Name", "Last Name", "Weight", "Weight Class ID")
        self.tv = ttk.Treeview(master=self.ea_win, columns=cols, show="headings")
        self.tv.bind("<ButtonRelease-1>", self.tv_mouse_release)
        self.tv.heading("Athlete ID", text="Athlete ID")
        self.tv.heading("First Name", text="First Name")
        self.tv.heading("Last Name", text="Last Name")
        self.tv.heading("Weight", text="Weight")
        self.tv.heading("Weight", text="Weight Class ID")
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=120, anchor="center")  # Center the treeview

        # Grid and layout of the widgets on the window
        pad = 3
        lbl_athlete_id.grid(row=1, column=1, padx=pad, pady=pad)
        self.athlete_id.grid(row=1, column=2, padx=pad, pady=pad)
        lbl_weightclass_id.grid(row=2, column=1, padx=pad, pady=pad)
        self.weightclass_id.grid(row=2, column=2, padx=pad, pady=pad)
        lbl_first_name.grid(row=3, column=1, padx=pad, pady=pad)
        self.entry_first_name.grid(row=3, column=2, padx=pad, pady=pad)
        lbl_last_name.grid(row=4, column=1, padx=pad, pady=pad)
        self.entry_last_name.grid(row=4, column=2, padx=pad, pady=pad)
        lbl_weight.grid(row=5, column=1, padx=pad, pady=pad)
        self.entry_weight.grid(row=5, column=2, padx=pad, pady=pad)
        btn_edit.grid(row=6, column=1, columnspan=2, padx=pad, pady=pad)
        self.tv.grid(row=1, column=3, rowspan=7, padx=pad, pady=pad)

        # Initialize DataAccessLayer object
        self.dal = DataAccessLayer()
        self.display_athlete_data()  # Call method after initializing DataAccessLayer

    def display_athlete_data(self):
        """Display athletes' information in the Treeview."""
        self.dal.open()  # Open database connection

        # Retrieve essential information about athletes. Utilizes a LEFT JOIN with the 'WeightClasses' table based on
        # 'WeightClassID' for a comprehensive athlete overview.
        # Query here-------------------------------------------------------------------------------------------
        query = """
            SELECT Athletes.AthleteID, Athletes.FirstName, Athletes.LastName,
            WeightClasses.Weight, WeightClasses.WCID
            FROM Athletes
            LEFT JOIN WeightClasses ON Athletes.WeightClassID = WeightClasses.WCID
                """
        athlete_data = self.dal.execute_query(query)

        # Remove unwanted characters in rows and insert into Treeview
        for row in athlete_data:
            modified_row = [str(val).replace(",", "").
                            replace("'", "").replace("(", "").
                            replace(")", "") if val else "" for val in row]
            self.tv.insert("", "end", values=modified_row)

        self.dal.close()

    def tv_mouse_release(self, event):
        """Handle selection in Treeview."""
        # Get the selected item
        selected_item = self.tv.focus()
        # Get values of the selected item
        item_values = self.tv.item(selected_item, 'values')

        # Populate Entry widgets with selected row's data
        self.entry_first_name.delete(0, END)
        self.entry_last_name.delete(0, END)
        self.entry_weight.delete(0, END)

        if item_values:
            # Insert values into respective Entry widgets
            self.athlete_id.config(text=item_values[0])
            self.entry_first_name.insert(0, item_values[1])
            self.entry_last_name.insert(0, item_values[2])
            self.entry_weight.insert(0, item_values[3])
            self.weightclass_id.config(text=item_values[4])

    def get_weight_class(self, weight):
        """Get the weight class based on the provided weight."""
        if 1 <= weight < 73:
            return "Flyweight"
        elif 73 <= weight < 81:
            return "Lightweight"
        elif 81 <= weight < 90:
            return "Light-Middleweight"
        elif 90 <= weight < 100:
            return "Middleweight"
        elif 100 <= weight < 101:
            return "Light-Heavyweight"
        else:
            return "Heavyweight"

    def edit_athlete(self):
        """Edit athlete information."""
        # Get data from the GUI elements
        athlete_id = self.athlete_id.cget("text")
        weightclass_id = self.weightclass_id.cget("text")
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        weight = self.entry_weight.get()

        # Validate if any of the fields are empty
        if not all((athlete_id, weightclass_id, first_name, last_name, weight)):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Validate first name and last name
        if not (first_name.isalpha() and last_name.isalpha()):
            messagebox.showerror("Error", "First name and last name should only contain letters.")
            return

        # Validate and convert weight to a numeric value
        if not weight:
            messagebox.showerror("Error", "Weight field cannot be empty.")
            return

        try:
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Weight should be a numeric value.")
            return

        try:
            # Create Data Access Layer instance and open the connection
            dal = DataAccessLayer()
            dal.open()

            # Update Athletes table with the provided data
            # Query here-------------------------------------------------------------------------------------------
            update_athlete = "UPDATE Athletes SET FirstName=?, LastName=? WHERE AthleteID=?"
            dal.execute(update_athlete, first_name, last_name, athlete_id)

            # Update WeightClasses table with the new weight value
            # Query here-------------------------------------------------------------------------------------------
            update_weight = "UPDATE WeightClasses SET Weight = ? WHERE WCID = ?"
            dal.execute(update_weight, weight, weightclass_id)

            # Update WeightClasses table with weight class based on weight range
            # Query here-------------------------------------------------------------------------------------------
            weight_class = self.get_weight_class(weight)
            update_weight_class = (
                "UPDATE WeightClasses SET WeightClass = ? "
                "WHERE WCID = ?"
            )
            dal.execute(update_weight_class, weight_class, weightclass_id)

            # Commit the changes and show success message
            dal.commit()
            messagebox.showinfo("Success", "Athlete information updated successfully!")

            # Reset the GUI elements
            self.reset()

        except Exception as e:
            # Handle exceptions and show an error message
            messagebox.showerror("Error", f"Error updating athlete information: {e}")

            # Rollback changes if an error occurs
            dal.rollback()

        finally:
            # Close the database connection in the 'finally' block to ensure it's closed
            dal.close()

    def reset(self):
        """Reset Entry widgets and Treeview."""
        self.entry_first_name.delete(0, END)
        self.entry_last_name.delete(0, END)
        self.entry_weight.delete(0, END)

        # Clear Treeview
        self.tv.delete(*self.tv.get_children())

        # Reload Athlete data in the Treeview
        self.display_athlete_data()
