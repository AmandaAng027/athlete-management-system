"""
Module: Private_Coaching_Registration.py
Date of Creation: January 8, 2024
Author: Amanda Ang

Modification History:
- Jan. 8, 2024 - created widgets or the GUI
- Jan. 9, 2024 - added functional buttons
- Jan. 10, 2024 - added SQL queries
- Jan. 15, 2024 - added comments and docstrings
- Jan. 29, 2024 - automated date
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments
- Feb. 17, 2024 - modified data validation

Synopsis:
This module defines the PrivateCoachingRegistration class, allowing users to register private coaching sessions.
It includes GUI elements for capturing registration details, athlete selection, and coaching hours.

Functions:
- __init__(self, pcr_win): Initializes the PrivateCoachingRegistration class.
- get_athletes(self): Fetches and returns a list of athletes from the database.
- register_private_coaching(self): Registers private coaching based on user input.
- get_athlete_id_from_name(self, athlete_name): Fetches and returns the AthleteID corresponding to
                                                the selected athlete's name.
- open_private_coaching_registration(): Function to create and open the Private Coaching Registration window.

Global Variables:
None
"""

from datetime import datetime
from tkinter import *
from tkinter import messagebox

from Data_Access_Layer import *


def open_private_coaching_registration():
    """Function to create and open the Private Coaching Registration window."""
    pcr_win = Tk()
    PrivateCoachingRegistration(pcr_win)
    pcr_win.mainloop()


class PrivateCoachingRegistration:
    def __init__(self, pcr_win):
        """Initialize the PrivateCoachingRegistration class"""
        self.pcr_win = pcr_win
        self.pcr_win.title("Register Private Coaching")
        self.pcr_win.geometry("400x200")

        # Private Coaching Title
        lbl_text = "Private Coaching"
        lbl = Label(self.pcr_win, text=lbl_text, font=("Arial", 14, "bold"))
        lbl.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Reg. Date Widgets
        lbl_reg_date = Label(self.pcr_win, text="Registration Date: ")
        lbl_reg_date.grid(row=2, column=0, padx=10, sticky="w")
        current_date = datetime.now().strftime('%d/%m/%Y')
        self.label_reg_date = Label(self.pcr_win, text=current_date)
        self.label_reg_date.grid(row=2, column=1, padx=10, sticky="w")

        # Private Coach. Date Widgets
        lbl_private_coaching_date = Label(self.pcr_win, text="Date of Private Coaching (dd/mm/yyyy): ")
        lbl_private_coaching_date.grid(row=3, column=0, padx=10, sticky="w")
        self.entry_private_coaching_date = Entry(self.pcr_win)
        self.entry_private_coaching_date.grid(row=3, column=1, padx=10, sticky="w")

        # Athlete ID Widgets
        lbl_athlete_id = Label(self.pcr_win, text="Athlete:")
        lbl_athlete_id.grid(row=4, column=0, padx=10, sticky="w")

        # Fetch athlete names and IDs from the database
        athletes = self.get_athletes()
        athlete_names = [f"{athlete['FirstName']} {athlete['LastName']}" for athlete in athletes]
        athlete_ids = [athlete['AthleteID'] for athlete in athletes]

        # Create dropdown box for athletes
        self.athlete_var = StringVar(self.pcr_win)
        self.athlete_var.set("")
        self.athlete_menu = OptionMenu(self.pcr_win, self.athlete_var, *[""] + athlete_names)
        self.athlete_menu.grid(row=4, column=1, padx=10, sticky="w")

        # Private Coaching Widgets
        lbl_private_coaching = Label(self.pcr_win, text="Number of Hours (£9.50/hr):")
        lbl_private_coaching.grid(row=5, column=0, padx=10, sticky="w")
        private_coaching_choices = [f"{i} hr/s" for i in range(1, 6)]  # Since 1-5 hours only
        self.private_coaching_var = StringVar(self.pcr_win)
        self.private_coaching_var.set("")

        # Create dropdown box
        self.pc_menu = OptionMenu(self.pcr_win,
                                  self.private_coaching_var,
                                  *[""] + private_coaching_choices)
        self.pc_menu.grid(row=5, column=1, padx=10, sticky="w")

        # Register button
        btn_upd = Button(self.pcr_win, text="Register",
                         command=self.register_private_coaching)  # then redirect to transactions
        btn_upd.grid(row=6, column=1, padx=10, sticky="w")

    def get_athletes(self):
        """Fetches and returns the list of athletes from the database."""
        dal = DataAccessLayer()
        dal.open()

        # Fetch AthleteID, FirstName, and LastName from Athletes table
        # Query here---------------------------------------------------------------------------------------
        athletes = dal.execute_query("SELECT AthleteID, FirstName, LastName FROM Athletes")

        dal.close()

        # Convert the list of tuples to a list of dictionaries
        athlete_dicts = [{'AthleteID': athlete[0], 'FirstName': athlete[1], 'LastName': athlete[2]} for athlete in
                         athletes]

        return athlete_dicts

    def register_private_coaching(self):
        """Registers private coaching for the selected athlete."""
        selected_athlete_name = self.athlete_var.get()
        athlete_id = self.get_athlete_id_from_name(selected_athlete_name)
        coaching_hrs_str = self.private_coaching_var.get()
        private_coaching_date_str = self.entry_private_coaching_date.get()

        # Check if any required field is empty
        if not selected_athlete_name or not coaching_hrs_str or not private_coaching_date_str:
            messagebox.showerror("Error",
                                 "Please fill in all the private coaching fields.")
            return

        # Remove the "hrs" string and get only the numeric
        coaching_hrs_str = coaching_hrs_str.split()[0]

        try:
            coaching_hrs = float(coaching_hrs_str)
            reg_date = datetime.now().strftime('%Y-%m-%d')
            private_coaching_date = datetime.strptime(private_coaching_date_str,
                                                      '%d/%m/%Y').strftime('%Y-%m-%d')

            # To check if all fields are filled out
            if not all([athlete_id, coaching_hrs, reg_date, private_coaching_date]):
                messagebox.showerror("Error",
                                     "Please fill in all the private coaching fields.")
                return

            dal = DataAccessLayer()
            dal.open()

            # Fetch the cost of private coaching from the UtilityCosts table
            # Query here---------------------------------------------------------------------------------------
            cost_query = "SELECT Amount FROM UtilityCosts WHERE Expense = ?"
            cost_result = dal.execute_query(cost_query, 'Private Coaching')

            # Extract the cost value from the result and convert it to float
            cost = float(cost_result[0][0])

            # Calculate cost based on coaching hours
            total_cost = coaching_hrs * cost

            # Insert into Coaching Registration
            # Query here---------------------------------------------------------------------------------------
            cr_query = (
                "INSERT INTO CoachingRegistration (AthleteID, RegDate, Cost) "
                "OUTPUT INSERTED.CID "
                "VALUES (?, ?, ?)"
            )
            coaching_id = dal.execute_query(cr_query, athlete_id, reg_date, total_cost)[0][0]
            dal.commit()

            # Insert into Private Coaching Table
            # Query here---------------------------------------------------------------------------------------
            pc_query = (
                "INSERT INTO PrivateCoaching (Hours, Date, CoachingID) "
                "VALUES (?, ?, ?)"
            )
            dal.execute(pc_query, coaching_hrs, private_coaching_date, coaching_id)
            dal.commit()

            # Convert the reg date month and year to text like "January" and "2024"
            reg_month = datetime.strptime(self.label_reg_date["text"], '%d/%m/%Y').strftime('%B')
            reg_year = datetime.strptime(self.label_reg_date["text"], '%d/%m/%Y').strftime('%Y')

            # Insert into MonthlyExpenses table
            # Query here---------------------------------------------------------------------------------------
            me_query = (
                "INSERT INTO MonthlyExpenses (AthleteID, ExpenseType, Month, Year, Cost) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            dal.execute(me_query, athlete_id, "Private Coaching", reg_month, reg_year, total_cost)
            dal.commit()

            messagebox.showinfo("Success", "Coaching registration and private coaching updated successfully!")
            self.pcr_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating coaching registration: {e}")
            dal.rollback()
        finally:
            dal.close()

    def get_athlete_id_from_name(self, athlete_name):
        """Fetch and return the AthleteID corresponding to the selected athlete's name."""
        dal = DataAccessLayer()
        dal.open()

        # SQL query to fetch AthleteID based on the concatenated first and last names
        # Query here---------------------------------------------------------------------------------------
        query = "SELECT AthleteID FROM Athletes WHERE CONCAT(FirstName, ' ', LastName) = ?"
        result = dal.execute_query(query, athlete_name)

        dal.close()

        # Check if the query result is not empty
        if result:
            # Return the first column (AthleteID) of the first row from the result set
            return result[0][0]
        else:
            # Return None if no matching AthleteID is found
            return None
