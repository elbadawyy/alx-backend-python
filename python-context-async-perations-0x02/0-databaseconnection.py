import sqlite3


class DatabaseConnection:
    """A custom context manager to handle opening and closing a database connection."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection and return the connection object."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the connection is properly closed, even if an error occurs."""
        if self.conn:
            if exc_type:
                # If there was an error, rollback any pending transaction
                self.conn.rollback()
            else:
                # Commit if everything ran successfully
                self.conn.commit()
            self.conn.close()


# ✅ Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
