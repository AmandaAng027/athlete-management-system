"""
Module: Main_Window.py
Date of Creation: December 21, 2023
Created by: Amanda Ang

Modification History:
- Dec. 21, 2023 - created widgets or the GUI
- Dec. 28, 2023 - added functional buttons
- Jan. 4, 2024 - importing modules
- Jan. 9, 2024 - organised the codes and import statements
- Jan. 15, 2024 - added a remove function
- Jan. 29, 2024 - added comments and docstrings
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the MainWindow class, representing the main window in the North Sussex Judo application and
displays all athletes in the Treeview.
It serves as the main window for opening secondary windows and includes a function to remove an athlete.

Functions:
- __init__(self, main_win): Initializes the Main Window.
- display_athlete_data(self): Displays athletes' information in the Treeview.
- remove_athlete(self): Removes the selected athlete from the Treeview and database.
- menu_item_exit_click(self): Closes the main window.
- reset(self): Resets Treeview and reloads athlete data.
- open_main_window(): Opens the main window.
- open_register_window(): Opens the athlete registration window.
- open_edit_athlete(): Opens the edit athlete window.
- open_athlete_transactions(): Opens the athlete transactions window.
- open_competitions(): Opens the competitions window.
- open_tppc_registration(): Opens the TPPC registration window.
- open_private_coaching_registration(): Opens the private coaching registration window.
- open_utility_costs(): Opens the utility costs window.

Global Variables:
None
"""

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *

from Data_Access_Layer import *


def open_main_window():
    """Open the main window."""
    main_win = Tk()
    MainWindow(main_win)
    main_win.mainloop()


def open_register_window():
    """Open the registration window"""
    from Athlete_Registration_Form import open_register_window
    open_register_window()


def open_edit_athlete():
    """Open the edit athlete window"""
    from Edit_Athlete import open_edit_athlete
    open_edit_athlete()


def open_athlete_transactions():
    """Open the athlete transactions window"""
    from Athlete_Transactions import open_athlete_transactions
    open_athlete_transactions()


def open_competitions():
    """Open the competitions window"""
    from Competitions import open_competitions
    open_competitions()


def open_tppc_registration():
    """Open the TPPC registration window"""
    from TPPC_Update import open_tppc_registration
    open_tppc_registration()


def open_private_coaching_registration():
    """Open the private coaching registration window"""
    from Private_Coaching_Registration import open_private_coaching_registration
    open_private_coaching_registration()


def open_utility_costs():
    """Open the utility costs window"""
    from Utility_Costs import open_utility_costs
    open_utility_costs()


class MainWindow:
    def __init__(self, main_win):
        """Initialize the Main Window."""
        self.main_win = main_win
        self.main_win.title("Main Window")
        self.main_win.geometry("920x450")

        # Create the menu bar
        menuBar = Menu(self.main_win)
        menuFile = Menu(menuBar, tearoff=0)
        menuRegister = Menu(menuBar, tearoff=0)
        menuUpdate = Menu(menuBar, tearoff=0)

        # Add cascading menus to the menu bar
        menuBar.add_cascade(label="File", menu=menuFile)
        menuBar.add_cascade(label="Register", menu=menuRegister)
        menuBar.add_cascade(label="Update", menu=menuUpdate)

        # Add commands to the file menu
        menuFile.add_command(label="Exit",
                             command=self.menu_item_exit_click)

        # Add commands to the register menu
        menuRegister.add_command(label="Competitions",
                                 command=open_competitions)
        menuRegister.add_command(label="Private Coaching",
                                 command=open_private_coaching_registration)

        # Add commands to the update menu
        menuUpdate.add_command(label="Training Plan and Private Coaching",
                               command=open_tppc_registration)
        menuUpdate.add_command(label="Utility Costs",
                               command=open_utility_costs)

        # Configure menu bar
        self.main_win.config(menu=menuBar)

        # Treeview to display all athletes information
        cols = ("Athlete ID", "First Name", "Last Name", "Weight (kg)",
                "Weight Class", "Training Plan")
        self.tv = ttk.Treeview(master=self.main_win, columns=cols, show="headings")
        self.tv.heading("Athlete ID", text="Athlete ID")
        self.tv.heading("First Name", text="First Name")
        self.tv.heading("Last Name", text="Last Name")
        self.tv.heading("Weight (kg)", text="Weight (kg)")
        self.tv.heading("Weight Class", text="Weight Class")
        self.tv.heading("Training Plan", text="Training Plan")

        # Layout
        pad = 7

        # Configure column headings and layout
        for col in cols:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=150, anchor="center")

        # Grid layout for the Treeview
        self.tv.grid(row=6, column=1, columnspan=5, padx=pad, pady=pad)

        # Label for the window title
        lbl_txt = "North Sussex Judo Athletes"
        lbl = Label(self.main_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=1, columnspan=5, pady=10)

        # Add Athlete Button
        btn_add_athlete = Button(self.main_win, text="Register Athlete",
                                 width=40, command=open_register_window)
        btn_add_athlete.grid(row=7, column=2, pady=pad, padx=pad)

        # Separator between buttons
        separator = ttk.Separator(self.main_win, orient='vertical')
        separator.grid(row=7, column=3, rowspan=5, sticky='ns',
                       pady=pad, padx=pad)

        # Remove Athlete Button
        btn_remove_athlete = Button(self.main_win, text="Remove Athlete",
                                    width=40, command=self.remove_athlete)
        btn_remove_athlete.grid(row=8, column=2, pady=pad, padx=pad)

        # Edit Athlete Button
        btn_edit_athlete = Button(self.main_win, text="Edit Athlete",
                                  width=40, command=open_edit_athlete)
        btn_edit_athlete.grid(row=7, column=5, sticky="w", padx=(5, 0))

        # View Transactions Button
        btn_view_transactions = Button(self.main_win, text="View Athletes Transactions",
                                       width=40, command=open_athlete_transactions)
        btn_view_transactions.grid(row=8, column=5, sticky="w", padx=(5, 0))

        # Reset Button
        btn_reset = Button(self.main_win, text="Reset",
                           width=40, command=self.reset)
        btn_reset.grid(row=9, column=2, pady=pad, padx=pad)

        self.dal = DataAccessLayer()
        self.display_athlete_data()  # Display athletes' information in the Treeview

    def display_athlete_data(self):
        """Display athletes information in the Treeview"""
        self.dal.open()  # Open database connection

        # SQL query to retrieve detailed information about athletes.
        # The query uses LEFT JOINs with WeightClasses and TrainingPlan tables based on
        # corresponding foreign keys to gather complete data even if certain fields are null.
        # Query here-------------------------------------------------------------------------------------------
        query = """
                    SELECT Athletes.AthleteID, Athletes.FirstName, Athletes.LastName,
                    WeightClasses.Weight, WeightClasses.WeightClass, TrainingPlan.TrainingPlan
                    FROM Athletes
                    LEFT JOIN WeightClasses ON Athletes.WeightClassID = WeightClasses.WCID
                    LEFT JOIN TrainingPlan ON Athletes.TrainingPlanID = TrainingPlan.TPID
                """
        athlete_data = self.dal.execute_query(query)

        # Insert fetched athlete data into the Treeview
        for row in athlete_data:
            modified_row = [str(val).replace(",", "").
                            replace("'", "").replace("(", "").
                            replace(")", "") if val else "" for val in row]
            self.tv.insert("", "end", values=modified_row)

        # Close database connection
        self.dal.close()

    def remove_athlete(self):
        """Remove selected athlete from the Treeview and database"""
        selected_item = self.tv.selection()

        # Check if an athlete is selected
        if selected_item:
            confirmation = messagebox.askyesno("Confirmation",
                                               "Are you sure you want to delete this athlete?")

            # Confirm deletion with the user
            if confirmation:
                # Athlete ID is the first value
                aid = self.tv.item(selected_item)['values'][0]
                self.dal.open()

                try:
                    # Delete records from related tables first
                    # Query here---------------------------------------------------------------------------------------
                    query_competitions = "DELETE FROM AthleteCompetitions WHERE AthleteID = ?"
                    self.dal.execute(query_competitions, aid)

                    # Query here---------------------------------------------------------------------------------------
                    query_expenses = "DELETE FROM MonthlyExpenses WHERE AthleteID = ?"
                    self.dal.execute(query_expenses, aid)

                    # Query here---------------------------------------------------------------------------------------
                    query_coaching_registration = "DELETE FROM CoachingRegistration WHERE AthleteID = ?"
                    self.dal.execute(query_coaching_registration, aid)

                    # Delete the athlete record
                    # Query here---------------------------------------------------------------------------------------
                    query_athlete = "DELETE FROM Athletes WHERE AthleteID = ?"
                    self.dal.execute(query_athlete, aid)

                    # Commit the changes
                    self.dal.commit()
                    messagebox.showinfo("Success", "Athlete removed successfully!")

                    # Remove the selected item from the Treeview
                    self.tv.delete(selected_item)

                except Exception as e:
                    # Roll back changes and display error message in case of an exception
                    self.dal.rollback()
                    messagebox.showerror("Error", f"Error removing athlete: {e}")

                finally:
                    self.dal.close()

    def menu_item_exit_click(self):
        """Closes the main window"""
        self.main_win.destroy()
        return

    def reset(self):
        """Reset Treeview and reload athlete data."""
        # Clearing the Treeview
        self.tv.delete(*self.tv.get_children())

        # Reload Athlete data in the Treeview
        self.display_athlete_data()
