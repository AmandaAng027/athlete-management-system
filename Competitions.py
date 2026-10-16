"""
Module: Competitions.py
Date of Creation: December 28, 2023
Author: Amanda Ang

Modification History:
- Dec. 28, 2023 - created widgets or the GUI
- Dec. 29, 2023 - added functional buttons
- Jan. 4, 2024 - organised the GUI widgets
- Jan 19, 2024 - added SQL queries
- Jan 28, 2024 - added comments
- Jan 29, 2024 - tried to fix the error
- Jan 30, 2024 - fixed the logical error
- Feb 2, 2024 - added documentation
- Feb. 5, 2024 - added comments
- Feb. 13, 2024 - modified data validation

Synopsis:
This module defines the Competitions class, which represents the Competitions window
in the North Sussex Judo application. It includes functionality for displaying upcoming
competitions, creating new competitions, and registering athletes for competitions.

Functions:
- __init__(self, comp_win): Initializes the Competitions class.
- display_athlete_data(self): Displays athletes' information in the Treeview.
- get_reg_date(self): Registers the competition date.
- reset(self): Resets Treeview and reloads athlete data.

Global Variables:
None
"""

from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
# In order to make .exe file to work
import tkcalendar
from babel import numbers as babel_numbers

from Data_Access_Layer import *


def open_competitions():
    """Function to create and open the Competitions window."""
    comp_win = Toplevel()
    Competitions(comp_win)


def open_competition_registration():
    """Function to open competition registration window."""
    from Competition_Registration import open_competition_registration
    open_competition_registration()


class Competitions:
    def __init__(self, comp_win):
        """Initialize the Competitions class with comp_win"""
        self.comp_win = comp_win
        self.comp_win.title("Competitions")
        self.comp_win.geometry("820x420")

        # Menu bar
        menuBar = Menu(self.comp_win)
        menuBar.add_command(label="Register Athlete for Competition",
                            command=open_competition_registration)
        self.comp_win.config(menu=menuBar)

        # Title
        lbl_txt = "Upcoming Competitions"
        lbl = Label(self.comp_win, text=lbl_txt, font=("Arial", 15, "bold"))
        lbl.grid(row=0, column=1, pady=10, padx=1)

        # Treeview of the Competitions information
        cols = ("Competition ID", "Competitors", "Category", "Competition Date")
        self.tv = ttk.Treeview(master=self.comp_win, columns=cols, show="headings")
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=200, anchor="center")

        # Create Buttons and Labels
        btn_create = Button(self.comp_win, text="Create Competition",
                            command=self.get_reg_date)
        lbl_competition_date = Label(self.comp_win, text="Competition Date: ")
        self.competition_date = DateEntry(self.comp_win,
                                          date_pattern='dd-mm-yyyy', width=12)
        lbl_category = Label(self.comp_win, text="Category:")

        # Categories for creating the competitions
        categories = [
            'Flyweight', 'Lightweight', 'Light-Middleweight',
            'Middleweight', 'Light-Heavyweight', 'Heavyweight'
        ]

        # Create Combobox for the list of categories
        self.category_var = StringVar()
        self.category_var.set(categories[0])
        self.category_dropdown = ttk.Combobox(self.comp_win, textvariable=self.category_var, values=categories,
                                              state="readonly")

        # Reset Btn
        btn_reset = Button(self.comp_win, text="Reset", width=15, command=self.reset)

        # Adjust layout and positioning of widgets
        self.competition_date.grid(row=7, column=1, sticky="w")
        btn_create.grid(row=9, column=0, pady=15, sticky="ee")
        lbl_competition_date.grid(row=7, column=0, sticky="e")
        lbl_category.grid(row=8, column=0, sticky="e")
        self.category_dropdown.grid(row=8, column=1, sticky="w")
        btn_reset.grid(row=8, column=2)

        # Layout
        pad = 7
        self.tv.grid(row=3, column=0, columnspan=5, padx=pad, pady=pad)

        # Initialize DataAccessLayer and display initial data
        self.dal = DataAccessLayer()
        self.display_athlete_data()

    def display_athlete_data(self):
        """Display athletes information in the Treeview"""
        try:
            self.dal.open()

            # SQL query to fetch information for displaying competitions and athletes in the Treeview
            # It retrieves data by joining the AthleteCompetitions, Athletes, and Competitions tables
            # This query selects Competition ID, concatenated athlete names, competition category, and competition date
            # Query here-------------------------------------------------------------------------------------------
            query = """
                SELECT 
                    AthleteCompetitions.CompetitionID, 
                    CONCAT(Athletes.FirstName, ' ', Athletes.LastName) AS Competitors, 
                    Competitions.Category, 
                    Competitions.Date AS CompetitionDate 
                FROM 
                    AthleteCompetitions
                INNER JOIN Athletes ON 
                AthleteCompetitions.AthleteID = Athletes.AthleteID
                INNER JOIN Competitions ON 
                AthleteCompetitions.CompetitionID = Competitions.CompetitionID
            """
            athlete_data = self.dal.execute_query(query)

            # Remove the comma, parenthesis, and quotation marks in rows
            for row in athlete_data:
                modified_row = [str(val).replace(",", "").
                                replace("'", "").replace("(", "").
                                replace(")", "") if val else "" for val in row]
                self.tv.insert("", "end", values=modified_row)
        except Exception as e:
            print(f"Error displaying athlete data: {e}")
            messagebox.showerror("Error", f"Error displaying athlete data: {e}")
        finally:
            self.dal.close()

    def get_reg_date(self):
        """Register the competition date."""
        competition_date_str = self.competition_date.get()
        competition_date = datetime.strptime(competition_date_str, '%d-%m-%Y')

        category = self.category_var.get()

        # Ensure both fields are filled
        if not (competition_date_str and category):
            messagebox.showerror("Error",
                                 "Please enter both Competition Date and Category")
            return

        # Check if the selected date is the second Saturday of the month
        if (competition_date.weekday() != 5) or (competition_date.weekday() == 5 and competition_date.day < 8) or (
                competition_date.day > 14):
            messagebox.showerror("Error",
                                 "Competitions are held only on the second Saturday of each month")
            return

        # Formatted Date
        formatted_date = competition_date.strftime('%Y-%m-%d')

        try:
            self.dal.open()

            # Insert competition date and category into the Competitions table
            # Query here-------------------------------------------------------------------------------------------
            insert_query = "INSERT INTO Competitions (Date, Category) VALUES (?, ?)"
            self.dal.execute(insert_query, formatted_date, category)

            self.dal.commit()
            messagebox.showinfo("Success",
                                "Competition date registered successfully!")
            self.reset()
        except Exception as e:
            print(f"Error inserting competition date: {e}")
            messagebox.showerror("Error",
                                 f"Error inserting competition date: {e}")
            self.dal.rollback()
        finally:
            self.dal.close()

    def reset(self):
        """Reset Treeview and reload athlete data."""
        # Clearing the Treeview
        self.tv.delete(*self.tv.get_children())

        # Reload Athlete data in the Treeview
        self.display_athlete_data()
