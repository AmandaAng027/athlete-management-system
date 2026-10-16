"""
Module: User_Registration.py
Date of Creation: January 29, 2024
Author: Amanda Ang

Modification History:
- Jan. 29, 2024 - created widgets or the GUI
- Jan. 29, 2024 - added SQL queries
- Jan. 31, 2024 - added data validations
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the User class, providing a user interface for user registration, designed for NSJ administrators.
It includes functions to create a new user account, perform data validation, and toggle password visibility.

Functions:
- __init__(self, user_win): Initializes the User class and creates the user registration window.
- toggle_password_visibility(self): Toggles the visibility of the password.
- create_account_process(self): Processes user input, validates data, and creates a new user account.
- open_login_window(self): Opens the login window and destroys the current window.
- open_user_registration(): Function to create and run the user registration window.

Global Variables:
None
"""

from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from Data_Access_Layer import DataAccessLayer


def open_user_registration():
    """Open the athlete registration window"""
    user_win = Tk()
    User(user_win)
    user_win.mainloop()


class User:
    def __init__(self, user_win):
        """Initialize the User Registration Window"""
        self.user_win = user_win
        self.user_win.title("User Registration")
        self.user_win.geometry("530x290")

        # Title
        lbl_txt = "Create a New Account"
        lbl = Label(self.user_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=0, padx=10, pady=5)

        # Reg. Date Label
        lbl_reg_date = Label(self.user_win, text="Date Created: ")
        current_date = datetime.now().strftime('%d/%m/%Y')
        self.label_reg_date = Label(self.user_win, text=current_date)
        lbl_reg_date.grid(row=1, column=0, padx=10, pady=5)
        self.label_reg_date.grid(row=1, column=1, padx=10, pady=5)

        # First name label
        lbl_first_name = Label(self.user_win, text="First name: ")
        lbl_first_name.grid(row=2, column=0, padx=10, pady=5)
        self.entry_first_name = Entry(self.user_win, width=30)
        self.entry_first_name.grid(row=2, column=1, padx=10, pady=5)

        # Last name label
        lbl_last_name = Label(self.user_win, text="Last name:")
        lbl_last_name.grid(row=3, column=0, padx=10, pady=5)
        self.entry_last_name = Entry(self.user_win, width=30)
        self.entry_last_name.grid(row=3, column=1, padx=10, pady=5)

        # Username label
        lbl_username = Label(self.user_win, text="Username:")
        lbl_username.grid(row=4, column=0, padx=10, pady=5)
        self.entry_username = Entry(self.user_win, width=30)
        self.entry_username.grid(row=4, column=1, padx=10, pady=5)

        # Password label
        lbl_password = Label(self.user_win, text="Password:")
        lbl_password.grid(row=5, column=0, padx=10, pady=5)
        self.entry_password = Entry(self.user_win, show="*", width=30)
        self.entry_password.grid(row=5, column=1, padx=10, pady=5)

        # Show password button
        btn_password_visibility = Button(self.user_win, text="Show", command=self.toggle_password_visibility)
        btn_password_visibility.grid(row=5, column=2, padx=10, pady=5)

        # Email label
        lbl_email = Label(self.user_win, text="Email:")
        lbl_email.grid(row=6, column=0, padx=10, pady=5)
        self.entry_email = Entry(self.user_win, width=30)
        self.entry_email.grid(row=6, column=1, padx=10, pady=5)

        # Create Account label
        btn_create = Button(self.user_win, text="Create Account", width=15, command=self.create_account_process)
        btn_create.grid(row=7, column=1, padx=10, pady=5)

    def toggle_password_visibility(self):
        """Toggle visibility of the password in the password entry field."""
        current_state = self.entry_password.cget("show")
        if current_state == "*":
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def create_account_process(self):
        """Process user input, validate data, and create a new user account."""
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        reg_date = datetime.now().strftime('%Y-%m-%d')

        # Check if all fields are filled out
        if not all((first_name, last_name, username, password, email)):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if first and last name contains special characters or digits
        if not (first_name.isalpha() and last_name.isalpha()):
            messagebox.showerror("Error", "First name and last name "
                                          "cannot contain special characters or digits.")
            return

        # Email must include '@' and  '.'
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Invalid email address.")
            return

        try:
            # Establish connection to database
            dal = DataAccessLayer()
            dal.open()

            # Check if the username already exists in the Users table
            # Query here---------------------------------------------------------------------------------------
            existing_user = dal.fetch_one("SELECT UserID FROM Users WHERE Username=?", username)

            # If the username already exists, display an error message and abort account creation
            if existing_user:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
                return

            # Insert user registration data into the Users table
            # Query here---------------------------------------------------------------------------------------
            dal.execute("INSERT INTO Users (FirstName, LastName, Username, Password, Email, DateCreated) "
                        "VALUES (?, ?, ?, ?, ?, ?)", first_name, last_name, username, password, email, reg_date)

            dal.commit()
            messagebox.showinfo("Success", "Account created successfully.")

            self.open_login_window()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Close database connection
            dal.close()

    def open_login_window(self):
        """Open the login window and destroy the current window"""
        self.user_win.destroy()
        from Login_Window import open_login_window
        open_login_window()
