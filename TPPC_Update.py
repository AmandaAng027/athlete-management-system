"""
Module: TPPC_Update.py
Date of Creation: December 28, 2023
Author: Amanda Ang

Modification History:
- Dec. 28, 2023 - created widgets or the GUI
- Dec. 28, 2023 - added SQL queries
- Jan. 4, 2024 - re-organised the widgets
- Jan. 15, 2024 - added comments
- Jan. 20, 2024 - added data validations
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments
- Feb. 17, 2024 - modified data validation


Synopsis:
This module defines the TPPCUpdate class, providing a user interface to update Training Plans and Private Coaching details.
It includes functions to update Training Plan based on TPID and update Private Coaching hours based on Coaching ID.

Functions:
- __init__(self, tppc_win): Initializes the TPPCUpdate class.
- update_training_plan(self): Updates the Training Plan based on the selected TPID and training plan.
- update_private_coaching(self): Updates Private Coaching hours based on the selected Coaching ID and hours.
- open_tppc_registration(): Function to create and run the Update Training Plan and Private Coaching Update window.

Global Variables:
None
"""

from tkinter import *
from tkinter import messagebox, ttk

from Data_Access_Layer import *


def open_tppc_registration():
    """Create and run the Training Plan and Private Coaching update window."""
    tppc_win = Tk()
    TPPCUpdate(tppc_win)
    tppc_win.mainloop()


class TPPCUpdate:
    def __init__(self, tppc_win):
        """Initialize the UI window for Training Plan and Private Coaching"""
        self.tppc_win = tppc_win
        self.tppc_win.title("Update Training Plan and Private Coaching")
        self.tppc_win.geometry("400x400")

        # Training Plan Title
        lbl_txt = "Training Plan"
        lbl = Label(self.tppc_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # TPID Widgets
        lbl_training_plan_id = Label(self.tppc_win, text="TPID: ")
        lbl_training_plan_id.grid(row=1, column=0, padx=10, sticky="w")
        self.entry_training_plan_id = Entry(self.tppc_win)
        self.entry_training_plan_id.grid(row=1, column=1, padx=10, sticky="w")

        # Training Plan dropdown widgets
        lbl_training_plan = Label(self.tppc_win, text="Training plan:")
        lbl_training_plan.grid(row=2, column=0, padx=10, sticky="w")
        training_plan_choices = ['Beginner', 'Intermediate', 'Elite']
        self.training_plan_var = StringVar(self.tppc_win)
        self.training_plan_var.set("")
        self.training_plan_menu = OptionMenu(self.tppc_win,
                                             self.training_plan_var,
                                             *[""] + training_plan_choices)
        self.training_plan_menu.grid(row=2, column=1, padx=10, sticky="w")

        # Update Button
        btn_update = Button(self.tppc_win, text="Update", command=self.update_training_plan)
        btn_update.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Add horizontal separator between Private Coaching and Training Plan
        separator = ttk.Separator(self.tppc_win, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)

        # Private Coaching Title
        lbl_txt = "Private Coaching"
        lbl = Label(self.tppc_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Coaching ID Widgets
        lbl_coaching_id = Label(self.tppc_win, text="Coaching ID: ")
        lbl_coaching_id.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.entry_coaching_id = Entry(self.tppc_win)
        self.entry_coaching_id.grid(row=6, column=1, padx=10, sticky="w")

        # Private Coaching Widgets
        lbl_private_coaching = Label(self.tppc_win, text="Private coaching (£9.50/hr):")
        lbl_private_coaching.grid(row=7, column=0, padx=10, sticky="w")
        private_coaching_choices = [f"{i} hr/s" for i in range(1, 6)]
        self.private_coaching_var = StringVar(self.tppc_win)
        self.private_coaching_var.set("")
        self.private_coaching_menu = OptionMenu(self.tppc_win,
                                                self.private_coaching_var, *[""] + private_coaching_choices)
        self.private_coaching_menu.grid(row=7, column=1, padx=10, sticky="w")

        # Update button
        update_button = Button(self.tppc_win, text="Update", command=self.update_private_coaching)
        update_button.grid(row=8, column=1, padx=10, sticky="w")

        # Dictionary to store TPIDs and their associated training plans for later use
        self.tpid_training_plan_dict = {}

    def update_training_plan(self):
        """Update Training Plan based on the selected TPID."""
        try:
            dal = DataAccessLayer()
            dal.open()

            # Fetch existing TPIDs and their associated training plans from the TrainingPlan table
            # Query here---------------------------------------------------------------------------------------
            tpid_training_plan_query = "SELECT TPID, TrainingPlan FROM TrainingPlan"
            tpids_training_plan = dal.execute_query(tpid_training_plan_query)

            # Store the fetched TPIDs and their associated training plans for later use
            if tpids_training_plan:
                self.tpid_training_plan_dict = {tpid[0]: tpid[1] for tpid in tpids_training_plan}

            # Get the selected training plan associated with the chosen TPID
            selected_tpid = self.entry_training_plan_id.get().strip()
            selected_tp = self.training_plan_var.get().strip()

            # Check if either of the fields is empty
            if not selected_tpid or not selected_tp:
                messagebox.showerror("Error", "Please enter both TPID and training plan.")
                return

            # Check if the selected TPID exists in the fetched TPIDs
            if int(selected_tpid) not in self.tpid_training_plan_dict:
                messagebox.showerror("Error", "Selected TPID not found in the database!")
                return

            # Fetch the cost associated with the selected training plan from the UtilityCosts table
            # Query here---------------------------------------------------------------------------------------
            training_plan_cost_query = "SELECT Amount FROM UtilityCosts WHERE Expense = ?"
            training_plan_cost_result = dal.execute_query(training_plan_cost_query, selected_tp)

            if training_plan_cost_result:
                tp_cost = float(training_plan_cost_result[0][0])

                # Update the training plan with the selected TPID and its cost
                # Query here---------------------------------------------------------------------------------------
                update_query = "UPDATE TrainingPlan SET TrainingPlan = ?, Cost = ? WHERE TPID = ?"
                dal.execute(update_query, selected_tp, tp_cost, selected_tpid)

                dal.commit()

                # Query to update the corresponding monthly expenses
                # for the athletes associated with the updated Training Plan
                # Query here-------------------------------------------------------------------------------------------
                update_expense_query = (
                    "UPDATE MonthlyExpenses SET Cost = ? WHERE AthleteID IN "
                    "(SELECT Athletes.AthleteID FROM Athletes "
                    "INNER JOIN TrainingPlan ON Athletes.TrainingPlanID = TrainingPlan.TPID "
                    "WHERE TrainingPlan.TPID = ?) AND ExpenseType = 'Training Plan'"
                )
                dal.execute(update_expense_query, tp_cost, selected_tpid)
                dal.commit()
                messagebox.showinfo("Success", "Training plan updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating training plan: {e}")
            dal.rollback()
        finally:
            dal.close()

    def update_private_coaching(self):
        """Update Private Coaching hours based on the selected Coaching ID and hours."""
        try:
            dal = DataAccessLayer()
            dal.open()

            # Strip leading/trailing whitespace
            selected_coaching_id = self.entry_coaching_id.get().strip()
            selected_hours = self.private_coaching_var.get().strip()

            # Check if either of the fields is empty
            if not selected_coaching_id or not selected_hours:
                messagebox.showerror("Error", "Please enter both Coaching ID and number of hours.")
                return

            # Check if the selected Coaching ID exists
            # Query here---------------------------------------------------------------------------------------
            coaching_id_exists_query = "SELECT COUNT(*) FROM CoachingRegistration WHERE CID = ?"
            coaching_id_exists_result = dal.execute_query(coaching_id_exists_query, selected_coaching_id)

            # Check if the Coaching ID exists in the CoachingRegistration table
            if coaching_id_exists_result and coaching_id_exists_result[0][0] > 0:
                # Retrieve the hourly rate for private coaching from the utility table
                # Query here---------------------------------------------------------------------------------------
                pc_hourly_rate_query = "SELECT Amount FROM UtilityCosts WHERE Expense = 'Private Coaching'"
                pc_hourly_rate_result = dal.execute_query(pc_hourly_rate_query)

                # Check if the query for fetching private coaching hourly rate was successful
                if pc_hourly_rate_result:
                    pc_hourly_rate = float(pc_hourly_rate_result[0][0])

                    # Update the Private Coaching hours and corresponding expenses
                    # Query here---------------------------------------------------------------------------------------
                    update_coaching_query = "UPDATE PrivateCoaching SET Hours = ? WHERE RegistrationID = ?"
                    dal.execute(update_coaching_query, selected_hours, selected_coaching_id)

                    # Calculate the total cost for the private coaching based on hours and hourly rate
                    monthly_cost = selected_hours * pc_hourly_rate

                    # Update the monthly expenses for athletes associated with the updated Private Coaching
                    # Query here---------------------------------------------------------------------------------------
                    update_expense_query = (
                        "UPDATE MonthlyExpenses SET Cost = ? "
                        "WHERE AthleteID IN (SELECT AthleteID FROM CoachingRegistration WHERE CID = ?) "
                        "AND ExpenseType = 'Private Coaching'"
                    )
                    dal.execute(update_expense_query, monthly_cost, selected_coaching_id)

                    # Update the cost in the CoachingRegistration table
                    # Query here---------------------------------------------------------------------------------------
                    update_registration_cost_query = "UPDATE CoachingRegistration SET Cost = ? WHERE CID = ?"
                    dal.execute(update_registration_cost_query, monthly_cost, selected_coaching_id)

                    dal.commit()
                    messagebox.showinfo("Success",
                                        "Private coaching hours updated successfully!")
            else:
                messagebox.showerror("Error",
                                     "Selected Coaching ID not found in the database")

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error updating private coaching: {e}")
            dal.rollback()
        finally:
            dal.close()
