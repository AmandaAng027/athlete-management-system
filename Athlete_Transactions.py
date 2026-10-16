"""
Module: Athlete_Transactions.py
Date of Creation: December 28, 2023
Author: Amanda Ang

Modification History:
- Dec. 28, 2023 - created widgets or the GUI
- Dec. 30, 2023 - re-organised the GUI widgets
- Jan. 4, 2024 - added functional buttons
- Jan. 19, 2024 - added comments
- Jan. 22, 2024 - re-organised the GUI widgets
- Jan. 28, 2024 - modified the SQL queries
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the AthleteTransactions class, which represents the Athlete Transactions window.
It is responsible for displaying and managing monthly expenses of athletes in the North Sussex Judo application.

Functions:
- __init__(self, at_win): Initializes the AthleteTransactions class.
- display_athlete_cost(self): Displays athlete expenses based on the selected month and year.
- open_athlete_transactions(): Function to create and open the AthleteTransactions window.

Global Variables:
None

"""

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *

from Data_Access_Layer import *


def open_athlete_transactions():
    """Function to create and open the AthleteTransactions window."""
    at_win = Toplevel()
    AthleteTransactions(at_win)


class AthleteTransactions:
    def __init__(self, at_win):
        """Initialize the AthleteTransactions class with at_win"""
        self.at_win = at_win
        self.at_win.title("Athlete Transactions")
        self.at_win.geometry("915x430")

        # Labels and input fields
        lbl_txt = "Total Monthly Expenses of the Athlete"
        lbl = Label(self.at_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        lbl_month = Label(self.at_win, text="Month:")
        lbl_month.grid(row=1, column=0, pady=10, padx=(5, 0), sticky="e")

        # List of Months
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.selected_month = StringVar()
        self.selected_month.set(months[0])  # Set default month

        # Create combobox for Months
        month_combobox = Combobox(self.at_win, textvariable=self.selected_month,
                                  values=months, state='readonly')
        month_combobox.grid(row=1, column=1, pady=10, padx=(0, 5), sticky="w")

        lbl_year = Label(self.at_win, text="Year:")
        lbl_year.grid(row=1, column=2, pady=10, padx=(5, 0), sticky="e")

        # List of Years
        years = list(range(2024, 2031))
        self.selected_year = StringVar()
        self.selected_year.set(str(years[0]))  # Set default year
        year_combobox = Combobox(self.at_win, textvariable=self.selected_year, values=years, state='readonly')
        year_combobox.grid(row=1, column=3, pady=10, padx=(0, 5), sticky="w")

        # Button to trigger displaying athlete costs
        btn_enter = Button(self.at_win, text="Enter", width=10,
                           command=self.display_athlete_cost)
        btn_enter.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        # Treeview to display expenses
        cols = ("Athlete ID", "Full Name", "Training Plan Cost", "Competitions Cost",
                "Private Coaching Cost", "Total Cost")
        self.tv = ttk.Treeview(master=self.at_win, columns=cols, show="headings")
        self.tv.heading("Athlete ID", text="Athlete ID")
        self.tv.heading("Full Name", text="Full Name")
        self.tv.heading("Training Plan Cost", text="Training Plan Cost")
        self.tv.heading("Competitions Cost", text="Competitions Cost")
        self.tv.heading("Private Coaching Cost", text="Private Coaching Cost")
        self.tv.heading("Total Cost", text="Total Cost")

        # Layout
        pad = 7

        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=150, anchor="center")

        self.tv.grid(row=5, column=0, columnspan=5, padx=pad, pady=pad)

        # Label to display the overall cost for the selected month and year
        self.overall_cost_label = Label(self.at_win, text="Overall Cost for the Month: £0")
        self.overall_cost_label.grid(row=6, column=0, columnspan=2, pady=(20, 10), padx=pad, sticky="w")

    def display_athlete_cost(self):
        """Display athlete expenses based on input."""
        selected_month = self.selected_month.get()
        selected_year = self.selected_year.get()
        dal = DataAccessLayer()
        try:
            dal.open()

            # The SQL query is designed to aggregate monthly expenses for each athlete based on the selected month
            # and year, calculating TrainingCost, CompetitionCost, CoachingCost, and TotalCost. It utilizes a LEFT
            # JOIN between the Athletes and MonthlyExpenses tables, grouping the results by athlete ID and full name.
            # Query here---------------------------------------------------------------------------------------------
            expenses_query = (
                "SELECT "
                "   Athletes.AthleteID, "
                "   CONCAT(Athletes.FirstName, ' ', Athletes.LastName) AS FullName, "
                "SUM(CASE WHEN MonthlyExpenses.ExpenseType = 'Training Plan' THEN MonthlyExpenses.Cost ELSE 0 END) AS "
                "TrainingCost,"
                "SUM(CASE WHEN MonthlyExpenses.ExpenseType = 'Competition' THEN MonthlyExpenses.Cost ELSE 0 END) AS "
                "CompetitionCost,"
                "SUM(CASE WHEN MonthlyExpenses.ExpenseType = 'Private Coaching' THEN MonthlyExpenses.Cost ELSE 0 END) "
                "AS CoachingCost,"
                "   SUM(MonthlyExpenses.Cost) AS TotalCost "
                "FROM "
                "   Athletes "
                "LEFT JOIN "
                "   MonthlyExpenses ON Athletes.AthleteID = MonthlyExpenses.AthleteID "
                "WHERE "
                "   MonthlyExpenses.Month = ? AND MonthlyExpenses.Year = ? "
                "GROUP BY "
                "   Athletes.AthleteID, CONCAT(Athletes.FirstName, ' ', Athletes.LastName)"
            )
            expenses_data = dal.execute_query(expenses_query, selected_month, selected_year)

            # Update the label to display the overall cost in the specified format
            overall_cost = sum(row[-1] for row in expenses_data) if expenses_data else 0
            self.overall_cost_label.config(text=f"Overall Cost for the Month: £{overall_cost}")

            # Clear existing data in the Treeview
            for item in self.tv.get_children():
                self.tv.delete(item)

            # Insert data into the treeview
            for row in expenses_data:
                athlete_id, full_name, training_cost, competition_cost, coaching_cost, total_cost = row
                self.tv.insert("", "end", values=(
                    athlete_id, full_name, f"£{training_cost}", f"£{competition_cost}", f"£{coaching_cost}",
                    f"£{total_cost}"))

                # Center align columns in the Treeview
            for column in ("Training Plan Cost", "Competitions Cost", "Private Coaching Cost", "Total Cost"):
                self.tv.column(column, anchor="center")

        except Exception as e:
            # Display error if an exception occurs
            messagebox.showerror("Error", f"Error fetching costs/Invalid input: {e}")

        finally:
            dal.close()
