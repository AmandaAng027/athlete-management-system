"""
Module: Athlete_Registration_Form.py
Date of Creation: December 21, 2023
Author: Amanda Ang

Modification History:
- Dec. 21, 2023 - created widgets or the GUI
- Dec. 28, 2023 - added functional buttons
- Jan. 5, 2024 - added comments
- Jan. 9, 2024 - organised the algorithm
- Jan. 14, 2024 - modified the functions
- Jan. 29, 2024 - automated reg. date
- Jan. 30, 2024 - added data validations
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments
- Feb. 17, 2024 - revised data validation

Synopsis:
This module defines the AthleteRegistration class, which represents the Athlete Registration Form for the
North Sussex Judo application.
It includes functionality for gathering athlete information and registering them, as well as connecting and
updating the database.

Functions:
- __init__(self, reg_win): Initializes the AthleteRegistration class.
- get_weight_class(self, weight): Determines the weight class based on the weight entered.
- register_process(self): Handles the registration process when the 'Register' button is clicked.
- open_register_window(): Opens the athlete registration window.

Global Variables:
None

"""

from datetime import datetime
from tkinter import *
from tkinter import messagebox

from Data_Access_Layer import *


def open_register_window():
    """Open the athlete registration window"""
    reg_win = Tk()
    AthleteRegistration(reg_win)
    reg_win.mainloop()


class AthleteRegistration:
    def __init__(self, reg_win):
        """Initialize the Athlete Registration Form"""
        self.reg_win = reg_win
        self.reg_win.title("Athlete Registration Form")
        self.reg_win.geometry("380x350")

        # Title
        lbl_txt = "Registration Form"
        lbl = Label(self.reg_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=0, padx=10, pady=5)

        # Creating labels and input fields for the registration form
        current_date = datetime.now().strftime('%d/%m/%Y')

        # Reg. Date Widgets
        lbl_reg_date = Label(self.reg_win, text="Registration Date: ")
        lbl_reg_date.grid(row=1, column=0, padx=10, pady=5)
        self.label_reg_date = Label(self.reg_win, text=current_date)
        self.label_reg_date.grid(row=1, column=1, padx=10, pady=5)

        # Athlete ID Widgets
        lbl_athlete_id = Label(self.reg_win, text="Athlete ID: ")
        lbl_athlete_id.grid(row=2, column=0, padx=10, pady=5)
        self.entry_athlete_id = Entry(self.reg_win)
        self.entry_athlete_id.grid(row=2, column=1, padx=10, pady=5)

        # First Name Widgets
        lbl_first_name = Label(self.reg_win, text="First name:")
        lbl_first_name.grid(row=3, column=0, padx=10, pady=5)
        self.entry_first_name = Entry(self.reg_win)
        self.entry_first_name.grid(row=3, column=1, padx=10, pady=5)

        # Last Name Widgets
        lbl_last_name = Label(self.reg_win, text="Last name:")
        lbl_last_name.grid(row=4, column=0, padx=10, pady=5)
        self.entry_last_name = Entry(self.reg_win)
        self.entry_last_name.grid(row=4, column=1, padx=10, pady=5)

        # Birthdate Widgets
        lbl_birthdate = Label(self.reg_win, text="Birthdate (mm/dd/yyyy):")
        lbl_birthdate.grid(row=5, column=0, padx=10, pady=5)
        self.entry_birthdate = Entry(self.reg_win)
        self.entry_birthdate.grid(row=5, column=1, padx=10, pady=5)

        # Weight Widgets
        lbl_weight = Label(self.reg_win, text="Weight (kg):")
        lbl_weight.grid(row=6, column=0, padx=10, pady=5)
        self.entry_weight = Entry(self.reg_win)
        self.entry_weight.grid(row=6, column=1, padx=10, pady=5)

        # Training Plan Widgets
        lbl_training_plan = Label(self.reg_win, text="Training plan:")
        lbl_training_plan.grid(row=7, column=0, padx=10, pady=5)

        # Create a dropdown for Training Plan
        training_plan_choices = ['Beginner', 'Intermediate', 'Elite']
        self.training_plan_var = StringVar(self.reg_win)
        self.training_plan_var.set("")
        self.training_plan_menu = OptionMenu(self.reg_win,
                                             self.training_plan_var,
                                             *training_plan_choices)
        self.training_plan_menu.grid(row=7, column=1, padx=10, pady=5)

        # Register Button
        btn_register = Button(self.reg_win, text="Register", width=20,
                              command=self.register_process)
        btn_register.grid(row=8, column=1, padx=10, pady=5)

    def get_weight_class(self, weight):
        """Determine the weight class based on the weight"""
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

    def register_process(self):
        """Handle the registration process when the 'Register' button is clicked"""
        # Retrieving input values from the form
        reg_date = datetime.now().strftime('%Y-%m-%d')
        athlete_id = self.entry_athlete_id.get()
        # Strip to remove leading/trailing whitespaces
        birthdate = self.entry_birthdate.get().strip()
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        training_plan = self.training_plan_var.get()
        selected_weight = self.entry_weight.get().strip()

        # Validate complete entries excluding birthdate
        if not all((reg_date, athlete_id, first_name, last_name, training_plan, selected_weight, birthdate)):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Validate athlete ID numeric
        if not athlete_id.isdigit():
            messagebox.showerror("Error", "Athlete ID must contain only numeric characters.")
            return

        # Validate first name and last name format (only when they are not empty)
        if (first_name or last_name) and (not first_name.isalpha() or not last_name.isalpha()):
            messagebox.showerror("Error", "First name and last name should only contain letters.")
            return

        # Attempt to convert the entered weight to a floating-point number
        try:
            selected_weight = float(selected_weight)
        except ValueError:
            # Display an error message for invalid weight input
            messagebox.showerror("Error", "Invalid weight entered.")
            return

        # Determine weight class
        selected_weight_class = self.get_weight_class(selected_weight)

        dal = DataAccessLayer()
        try:
            # Open the connection
            dal.open()

            # Retrieve training plan costs from the utility table
            # Query here-------------------------------------------------------------------------------------------
            training_plan_cost_query = "SELECT Amount FROM UtilityCosts WHERE Expense = ?"
            training_plan_cost = dal.execute_query(training_plan_cost_query, training_plan)
            if training_plan_cost:
                training_plan_cost = training_plan_cost[0][0]
            else:
                training_plan_cost = 0

            # Insert data into WeightClasses table
            # Query here-------------------------------------------------------------------------------------------
            weight_class_sql = (
                "INSERT INTO WeightClasses "
                "(Weight, WeightClass) "
                "OUTPUT INSERTED.WCID "
                "VALUES (?, ?);"
            )
            weight_class_id = dal.execute_query(weight_class_sql, selected_weight, selected_weight_class)[0][0]
            dal.commit()

            # Insert data into TrainingPlan table
            # Query here-------------------------------------------------------------------------------------------
            training_plan_sql = (
                "INSERT INTO TrainingPlan "
                "([TrainingPlan], Cost) "
                "OUTPUT INSERTED.TPID "
                "VALUES (?, ?);"
            )
            training_plan_id = dal.execute_query(training_plan_sql, training_plan, training_plan_cost)[0][0]
            dal.commit()

            # Insert data into Athletes table
            # Query here-------------------------------------------------------------------------------------------
            athlete_sql = (
                "INSERT INTO Athletes (AthleteID, FirstName, LastName, "
                "Birthdate, RegistrationDate, WeightClassID, TrainingPlanID)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            dal.execute(athlete_sql, athlete_id, first_name, last_name, birthdate, reg_date,
                        weight_class_id, training_plan_id)
            dal.commit()

            # Insert data into MonthlyExpenses table
            # Query here-------------------------------------------------------------------------------------------
            monthly_expense_sql = (
                "INSERT INTO MonthlyExpenses "
                "(AthleteID, ExpenseType, Month, Year, Cost) "
                "VALUES (?, ?, ?, ?, ?)"
            )

            # Extract month and year from the registration date
            reg_month = datetime.strptime(reg_date,
                                          '%Y-%m-%d').strftime('%B')
            reg_year = datetime.strptime(reg_date,
                                         '%Y-%m-%d').strftime('%Y')

            # Insert data into the MonthlyExpenses table
            dal.execute(monthly_expense_sql, athlete_id,
                        'Training Plan', reg_month, reg_year,
                        training_plan_cost)
            dal.commit()

            messagebox.showinfo("Success", "Data stored successfully!")
            self.reg_win.destroy()
        except pyodbc.Error as ex:
            messagebox.showerror("Error", f"Database Error: {ex}")
            dal.rollback()
        finally:
            dal.close()
