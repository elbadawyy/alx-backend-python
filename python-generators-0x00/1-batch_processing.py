#!/usr/bin/python3
"""
Module: 1-batch_processing
Objective: Create a generator to fetch and process user data in batches efficiently.
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Args:
        batch_size (int): Number of rows to fetch per batch.
    Yields:
        list[dict]: A batch (list) of user rows.
    """
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # replace with your MySQL root password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users, filtering users over age 25.
    Args:
        batch_size (int): Number of users per batch.
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users older than 25
        processed_batch = (user for user in batch if user['age'] > 25)
        for user in processed_batch:
            print(user)
