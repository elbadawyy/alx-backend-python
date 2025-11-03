#!/usr/bin/python3
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    """Decorator that logs SQL queries before execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage (will print query + results)
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
