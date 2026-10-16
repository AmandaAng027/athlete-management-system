"""
Module: __Home_Window.py
Date of Creation: December 20, 2023
Author: Amanda Ang

Modification History:
- Dec. 21, 2023 - created widgets or the GUI
- Dec. 28, 2023 - added functional buttons
- Jan. 4, 2024 - added comments
- Jan. 9, 2024 - organised the codes and naming conventions
- Jan. 12, 2024 - repositioned widgets
- Jan. 14, 2024 - added docstrings
- Jan. 28, 2024 - added a new button
- Jan. 29, 2024 - fixed the keyboard interrupt error
- Feb. 2, 2024 - added documentation

Synopsis:
This module defines the HomeWindow class, which represents the starting window of the North Sussex Judo application.
It includes functionality for displaying the buttons for opening login and user registration windows.

Functions:
- __init__(self, home_win): Initializes the HomeWindow class.
- exit(self): Closes the main window.
- open_login_window(self): Destroys the home window and opens the login window.
- open_user_registration(self): Opens the user registration window.
- open_home_window(): Opens the home window by creating an instance of HomeWindow class.

Global Variables:
None

"""

import tkinter as tk


def open_home_window():
    """Open the home window by creating an instance of HomeWindow class."""
    home_win = tk.Tk()
    HomeWindow(home_win)


class HomeWindow:
    def __init__(self, home_win):
        """Initialize the HomeWindow class."""
        self.home_win = home_win
        self.home_win.title("North Sussex Judo Home")
        self.home_win.geometry("400x200")

        self.home_win.columnconfigure(0, weight=1)

        # Create menubar
        menuBar = tk.Menu(self.home_win)
        menuFile = tk.Menu(menuBar, tearoff=0)
        menuFile.add_command(label="Exit", command=self.exit)
        menuBar.add_cascade(label="File", menu=menuFile)

        # Add consistent padding
        pad = 10

        # Create label/title
        lbl_txt = "North Sussex Judo"
        lbl = tk.Label(self.home_win, text=lbl_txt, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=0, columnspan=2, pady=pad)

        # Create Login button
        btn_login = tk.Button(self.home_win, text="Login", font=("Arial", 14, "bold"),
                              command=self.open_login_window)
        btn_login.grid(row=1, column=0, columnspan=2, pady=pad)

        # Create a Create Account button
        btn_create = tk.Button(self.home_win, text="Create Account", font=("Arial", 14, "bold"),
                               command=self.open_user_registration)
        btn_create.grid(row=2, column=0, columnspan=2, pady=pad)

        self.home_win.config(menu=menuBar)
        self.home_win.mainloop()

    def exit(self):
        """Closes the main window"""
        self.home_win.destroy()
        return

    def open_login_window(self):
        """Destroys the home window then opens the login window"""
        self.home_win.destroy()
        from Login_Window import open_login_window
        open_login_window()

    def open_user_registration(self):
        """Open the user registration window"""
        from User_Registration import open_user_registration
        open_user_registration()


if __name__ == "__main__":
    """Initialize the home window as the main entry point of the program"""
    open_home_window()
