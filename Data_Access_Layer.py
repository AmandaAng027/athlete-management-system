"""
Module: DataAccessLayer.py
Date of Creation: December 20, 2023
Author: Amanda Ang

Modification History:
- Dec 20, 2023 - established the connection between the database and the application
- Dec. 27, 2023 - added a function 'fetch_one'
- Jan. 19, 2024 - added docstrings and comments
- Feb. 2, 2024 - added documentation


Synopsis:
This module defines the DataAccessLayer class, responsible for handling the interaction with the database.
It includes methods for establishing connections, executing SQL commands and queries, and managing transactions.

Functions:
- __init__(self): Initializes a DataAccessLayer instance.
- open(self): Establishes a connection to the database.
- execute(self, sql, *param): Executes SQL commands.
- commit(self): Commits the current transaction.
- rollback(self): Rolls back the current transaction.
- execute_query(self, sql, *param): Executes a SQL query and returns results as a list of tuples.
- close(self): Closes the cursor and the connection to the database.
- fetch_one(self, query, *args): Executes a SQL query and fetches the first row.

Global Variables:
- cs: Connection string to connect to the database.

"""

import pyodbc


class DataAccessLayer:
    # Connection string to connect to the database
    cs = """
        Driver={ODBC Driver 17 for SQL Server};
        Server=LAPTOP-LLLCJJDT\\SQLEXPRESS;
        Database=North Sussex Judo;
        Trusted_Connection=yes;
    """

    def __init__(self):
        """Initialize DataAccessLayer instance."""
        # Database connection
        self.cn = None
        # Cursor to execute SQL queries
        self.cursor = None

    def open(self):
        """Establish a connection to the database."""
        self.cn = pyodbc.connect(DataAccessLayer.cs)
        self.cursor = self.cn.cursor()
        return

    def execute(self, sql, *param):
        """Execute SQL Commands."""
        self.cursor.execute(sql, param)
        return

    def commit(self):
        """Commit the current transaction."""
        self.cn.commit()
        return

    def rollback(self):
        """Roll back the current transaction."""
        self.cn.rollback()
        return

    def execute_query(self, sql, *param):
        """Execute a SQL Query and return as a list of tuples."""
        self.cursor.execute(sql, *param)
        db_set = self.cursor.fetchall()
        return db_set

    def close(self):
        """Close the cursor and the connection to the database."""
        self.cursor.close()
        self.cn.close()
        return

    def fetch_one(self, query, *args):
        """Execute a SQL query and fetch the first row."""
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row[0] if row else None
