#!/usr/bin/python3
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to handle database connection setup and teardown."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def transactional(func):
    """Decorator to handle transaction commit or rollback automatically."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed, rolled back: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update a user's email with transaction handling."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully (if user exists).")
