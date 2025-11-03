#!/usr/bin/python3
"""
Module: 3-average_age
Objective: Compute a memory-efficient average age using a generator.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()


def calculate_average_age():
    """
    Calculate the average age of users using the generator stream_user_ages.
    Prints: Average age of users: <average>
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
