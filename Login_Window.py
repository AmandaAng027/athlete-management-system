"""
Module: Login_Window.py
Date of Creation: December 20, 2023
Created by: Amanda Ang

Modification History:
- December 20, 2023 - created widgets or the GUI
- Dec. 20, 2023 - added functional buttons
- Jan. 4, 2024 - added comments
- Jan. 28, 2024 - added SQL query
- Feb. 2, 2024 - added documentation
- Feb. 5, 2024 - added comments

Synopsis:
This module defines the LoginWindow class, representing the Login Window in the North Sussex Judo application.
It provides a simple username and password login interface, with functionality to validate credentials against a database.

Functions:
- __init__(self, login_win): Initializes the Login Window.
- toggle_password_visibility(self): Toggles the visibility of the password entry field.
- login_process(self, event=None): Processes the login attempt, validating user credentials, and opening the main window.
- open_login_window(): Opens the login window.

Global Variables:
None
"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from Data_Access_Layer import DataAccessLayer


def open_login_window():
    """Open the login window."""
    login_win = Tk()
    LoginWindow(login_win)
    login_win.mainloop()


class LoginWindow:
    def __init__(self, login_win):
        """Initialize the Login Window."""
        self.login_win = login_win
        self.login_win.title("Login Window")
        self.login_win.geometry("350x180")

        # Create and place the login label
        lbl_txt = "Login"
        lbl = Label(self.login_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=1, padx=10, pady=5)

        # Create labels, entry fields, and login button
        lbl_username = Label(self.login_win, text="Username: ", font=("Arial", 12, "bold"))
        lbl_password = Label(self.login_win, text="Password: ", font=("Arial", 12, "bold"))
        self.entry_password = Entry(self.login_win, show="*")
        self.entry_username = Entry(self.login_win)
        btn_login = Button(self.login_win, text="Login", command=self.login_process)
        btn_show_password = Button(self.login_win, text="Show", command=self.toggle_password_visibility)

        # Place labels, entry fields, and button in the window using grid layout
        lbl_username.grid(row=1, column=0, padx=10, pady=5)
        lbl_password.grid(row=2, column=0, padx=10, pady=5)
        self.entry_password.grid(row=2, column=1, padx=10, pady=5)
        self.entry_username.grid(row=1, column=1, padx=10, pady=5)
        btn_login.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        btn_show_password.grid(row=2, column=2, padx=5, pady=5)

        # Bind the 'Return' or 'Enter' key to trigger the login process
        self.login_win.bind('<Return>', self.login_process)

    def toggle_password_visibility(self):
        """Toggle the visibility of the password entry field."""
        current_show_state = self.entry_password.cget("show")
        # Toggle the visibility based on the current state
        if current_show_state == "":
            # If the password is currently hidden, show it
            self.entry_password.config(show="*")
        else:
            # If the password is currently visible, hide it
            self.entry_password.config(show="")

    def login_process(self, event=None):
        from Main_Window import open_main_window
        # Get username and password entered by the user
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if all the fields are filled out
        if not all((username, password)):
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            # Establish connection to database
            dal = DataAccessLayer()
            dal.open()

            # Query database to check if the provided credentials match any user record
            # Query here-------------------------------------------------------------------------------------------
            user_record = dal.fetch_one("SELECT * FROM Users WHERE Username=? AND Password=?",
                                        username, password)

            if user_record:
                # Successful login message and open the main window
                messagebox.showinfo("Success", "Login successful.")
                self.login_win.destroy()
                open_main_window()
            else:
                # Invalid login message
                messagebox.showerror("Error", "Invalid username or password. Please consider "
                                              "creating an account if necessary.")

        except Exception as e:
            # Error message for any exceptions during the login process
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Close database connection
            dal.close()
