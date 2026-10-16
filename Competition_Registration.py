"""
Module: Competition_Registration.py
Date of Creation: January 4, 2024
Author: Amanda Ang

Modification History:
- Jan. 4, 2024 - created widgets or the GUI
- Jan. 4, 2024 - added functional buttons and SQL queries
- Jan. 29, 2024 - automated the date
- Jan 30, 2024 - added comments
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the CompetitionRegistration class, representing the Competition Registration Form
for the North Sussex Judo application.
It provides functionality to register athletes for competitions, display treeview of athletes,
and update the database.

Functions:
- __init__(self, cr_win): Initializes the CompetitionRegistration class.
- display_athlete_data(self): Displays athletes' information in the Treeview.
- tv_mouse_release(self, event): Handles selection in the Treeview.
- register_athlete(self): Registers an athlete for a competition.
- is_weight_category_compatible(self, athlete_weight, competition_weight): Checks if the athlete's weight category is
                                                                    compatible with the competition's weight category.
- reset(self): Resets Treeview and reloads athlete data.
- open_competition_registration(): Opens the Competition Registration Form window.

Global Variables:
None
"""

from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *

from Data_Access_Layer import *


def open_competition_registration():
    """Function to create and open the Competition Registration Form window."""
    cr_win = Tk()
    CompetitionRegistration(cr_win)
    cr_win.mainloop()


class CompetitionRegistration:
    def __init__(self, cr_win):
        """Initialize the CompetitionRegistration class."""
        self.cr_win = cr_win
        self.cr_win.title("Competition Registration Form")
        self.cr_win.geometry("850x250")

        # Athlete ID Label
        lbl_athlete_id = Label(self.cr_win, text="Athlete ID: ")
        self.athlete_id = Label(self.cr_win, text="")

        # Reg. Date Label
        lbl_reg_date = Label(self.cr_win, text="Registration Date: ")

        # Current date as the default value for the Reg. Date Label
        current_date = datetime.now().strftime('%d/%m/%Y')
        self.label_reg_date = Label(self.cr_win, text=current_date)

        # Competition ID Label
        lbl_competition_id = Label(self.cr_win, text="Competition ID: ")
        self.entry_competition_id = Entry(self.cr_win)

        # Register Btn
        btn_register = Button(self.cr_win, text="Register",
                              command=self.register_athlete)

        # Create Treeview for Athlete selection and information
        cols = ("Athlete ID", "First Name", "Last Name", "Skill Level", "Weight Category")
        self.tv = ttk.Treeview(master=self.cr_win, columns=cols, show="headings")
        self.tv.bind("<ButtonRelease-1>", self.tv_mouse_release)
        self.tv.heading("Athlete ID", text="Athlete ID")
        self.tv.heading("First Name", text="First Name")
        self.tv.heading("Last Name", text="Last Name")
        self.tv.heading("Skill Level", text="Skill Level")
        self.tv.heading("Weight Category", text="Weight Category")
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=120, anchor="center")

        # Grid layout for widgets
        pad = 3
        lbl_athlete_id.grid(row=1, column=1, padx=pad, pady=pad)
        self.athlete_id.grid(row=1, column=2, padx=pad, pady=pad)
        lbl_reg_date.grid(row=2, column=1, padx=pad, pady=pad)
        self.label_reg_date.grid(row=2, column=2, padx=pad, pady=pad)
        lbl_competition_id.grid(row=3, column=1, padx=pad, pady=pad)
        self.entry_competition_id.grid(row=3, column=2, padx=pad, pady=pad)
        btn_register.grid(row=4, column=1, columnspan=2, padx=pad, pady=pad)

        self.tv.grid(row=1, column=3, rowspan=7,
                     padx=pad, pady=pad)

        # Open DAL
        self.dal = DataAccessLayer()
        self.display_athlete_data()

    def display_athlete_data(self):
        """Fetch athletes' information from the database and populate the Treeview."""
        self.dal.open()  # Open database connection

        # SQL query to fetch athlete data with specific columns
        # The query uses LEFT JOINs with the TrainingPlan and WeightClasses tables to retrieve
        # corresponding information. It includes a filter to select athletes with TrainingPlan 'Intermediate' or
        # 'Elite'.
        # Query here-------------------------------------------------------------------------------------------
        query = """
                SELECT Athletes.AthleteID, Athletes.FirstName,Athletes.LastName, 
                TrainingPlan.TrainingPlan AS SkillLevel,
                WeightClasses.WeightClass AS WeightCategory FROM Athletes
                LEFT JOIN 
                TrainingPlan ON Athletes.TrainingPlanID = TrainingPlan.TPID
                LEFT JOIN 
                WeightClasses ON Athletes.WeightClassID = WeightClasses.WCID
                WHERE TrainingPlan.TrainingPlan IN ('Intermediate', 'Elite')

                       """
        athlete_data = self.dal.execute_query(query)

        # Process each row of athlete data before inserting into the Treeview
        for row in athlete_data:
            # Remove unwanted characters (e.g., commas, single quotes, parentheses) from each value in the row
            modified_row = [str(val).replace(",", "").
                            replace("'", "").replace("(", "").
                            replace(")", "") if val else "" for val in row]
            # Insert the modified row into the Treeview
            self.tv.insert("", "end", values=modified_row)

        self.dal.close()

    def tv_mouse_release(self, event):
        """Handle the mouse release event in the Treeview for athlete selection."""
        selected_item = self.tv.focus()
        item_values = self.tv.item(selected_item, 'values')
        if item_values:
            # Insert values into respective Entry widgets
            self.athlete_id.config(text=item_values[0])

    def register_athlete(self):
        """Register athlete for a competition."""
        athlete_id = self.athlete_id.cget("text")
        reg_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date
        competition_id = self.entry_competition_id.get()

        #  Check if all fields are filled out
        if not all([athlete_id, competition_id]):
            messagebox.showerror("Error",
                                 "Please fill in all the competition registration fields.")
            return

        dal = DataAccessLayer()
        try:
            dal.open()

            # Check if the competition ID exists in the database
            # Query here-------------------------------------------------------------------------------------------
            check_query = "SELECT COUNT(*) FROM Competitions WHERE CompetitionID = ?"
            result = dal.fetch_one(check_query, competition_id)
            if result == 0:
                messagebox.showerror("Error", "Competition not found.")
                return

            # Check if the athlete is already registered for the competition
            # Query here-------------------------------------------------------------------------------------------
            existing_registration_query = (
                "SELECT COUNT(*) FROM AthleteCompetitions WHERE CompetitionID = ? AND AthleteID = ?"
            )

            # Fetch the count of existing registrations for the athlete and competition combination
            existing_registration = dal.fetch_one(existing_registration_query, competition_id, athlete_id)

            # If the athlete is already registered, display an error message and return
            if existing_registration > 0:
                messagebox.showerror("Error", "Athlete is already registered for this competition.")
                return

            # Query to fetch the weight category of the athlete
            # Query here-------------------------------------------------------------------------------------------
            weight_category_query = """
                           SELECT WeightClasses.WeightClass
                           FROM Athletes
                           INNER JOIN WeightClasses ON Athletes.WeightClassID = WeightClasses.WCID
                           WHERE Athletes.AthleteID = ?
                       """

            # Fetch the weight category of the athlete from the database
            athlete_weight_category = dal.fetch_one(weight_category_query, athlete_id)

            # Fetch competition's weight category
            # Query here-------------------------------------------------------------------------------------------
            competition_weight_category_query = "SELECT Category FROM Competitions WHERE CompetitionID = ?"
            competition_weight_category = dal.fetch_one(competition_weight_category_query, competition_id)

            # Check if the athlete's weight category is compatible with the competition's weight category
            is_compatible = self.is_weight_category_compatible(athlete_weight_category, competition_weight_category)
            print("Is weight category compatible:", is_compatible)

            # Ensure case-sensitive comparison
            if athlete_weight_category != competition_weight_category:
                is_compatible = False

            # Trim leading and trailing whitespace
            athlete_weight_category = athlete_weight_category.strip()
            competition_weight_category = competition_weight_category.strip()

            # Print the trimmed athlete weight category and competition weight category for debugging purposes
            # To ensure there are no leading or trailing whitespaces that might affect the comparison
            print("Athlete Weight Category (after trimming):", athlete_weight_category)
            print("Competition Weight Category (after trimming):", competition_weight_category)

            # If the athlete's weight category is not compatible with the competition's weight category,
            # display an error message and return
            if not is_compatible:
                messagebox.showerror("Error", "Invalid weight category for the competition.")
                return

            # Query to fetch the registration cost for the competition from the utility table
            # Query here-------------------------------------------------------------------------------------------
            competition_cost_query = "SELECT Amount FROM UtilityCosts WHERE Expense = 'Competition'"
            competition_cost_result = dal.fetch_one(competition_cost_query)
            if competition_cost_result:
                competition_cost = float(competition_cost_result)
            else:
                # If the registration cost is not found, display an error message and return
                messagebox.showerror("Error", "Competition registration "
                                              "cost not found in the utility table.")
                return

            # Insert athlete into AthleteCompetitions table
            # Query here-------------------------------------------------------------------------------------------
            ac_query = (
                "INSERT INTO AthleteCompetitions (CompetitionID, AthleteID, "
                "Cost, RegDate) VALUES (?, ?, ?, ?)"
            )
            dal.execute(ac_query, competition_id, athlete_id, competition_cost, reg_date)
            dal.commit()

            # Extract the month from the registration date string and format it to the full month name (e.g., 'January')
            reg_month = datetime.strptime(reg_date, '%Y-%m-%d').strftime('%B')
            reg_year = datetime.strptime(reg_date, '%Y-%m-%d').strftime('%Y')

            # SQL query to insert monthly expense record into the MonthlyExpenses table
            # Query here-------------------------------------------------------------------------------------------
            me_query = (
                "INSERT INTO MonthlyExpenses (AthleteID, ExpenseType, "
                "Month, Year, Cost) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            # Execute the SQL query to insert monthly expense record
            dal.execute(me_query, athlete_id, "Competition", reg_month, reg_year, competition_cost)
            # Commit the transaction
            dal.commit()

            self.reset()

            # Display a success message indicating athlete registration for the competition was successful
            messagebox.showinfo("Success",
                                "Athlete registered successfully in the competition!")
            # Close the Competition Registration Form window
            self.cr_win.destroy()

        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter a valid value.")
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error updating competition information: {e}")
            dal.rollback()
        finally:
            dal.close()

    def is_weight_category_compatible(self, athlete_weight, competition_weight):
        """Check if the athlete's weight category is compatible with the competition's weight category."""
        # Check if the athlete's weight category is equal to the competition's weight category
        return athlete_weight == competition_weight

    def reset(self):
        """Reset Treeview and reload athlete data."""
        # Clearing the Treeview
        self.tv.delete(*self.tv.get_children())

        # Reload Athlete data in the Treeview
        self.display_athlete_data()
