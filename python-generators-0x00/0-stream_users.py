#!/usr/bin/python3
"""
Module: 0-stream_users
Objective: Create a generator that streams rows from an SQL database one by one.
"""

import mysql.connector


def stream_users():
    """
    Connects to the ALX_prodev database and yields rows from user_data one by one.
    Yields:
        dict: A dictionary containing user_id, name, email, and age for each user.
    """
    try:
        # Establish connection to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # replace with your MySQL root password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Use generator to yield one row at a time
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close resources properly
        if cursor:
            cursor.close()
        if connection:
            connection.close()
