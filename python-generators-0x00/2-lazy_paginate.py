#!/usr/bin/python3
"""
Module: 2-lazy_paginate
Objective: Lazily load paginated user data from MySQL using a generator.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from user_data table.
    Args:
        page_size (int): Number of users per page.
        offset (int): Offset for pagination.
    Returns:
        list[dict]: List of user records for that page.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads each page of users only when needed.
    Args:
        page_size (int): Number of users per page.
    Yields:
        list[dict]: Each page of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
