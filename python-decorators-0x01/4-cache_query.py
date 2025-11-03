import sqlite3
import functools
import time

query_cache = {}


def with_db_connection(func):
    """Decorator to handle opening and closing of the database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """Decorator that caches query results to avoid redundant database calls."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Cache hit! Returning cached result.")
            return query_cache[query]
        else:
            print("Cache miss! Executing query and caching result.")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call — query executes and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — uses cached result instead of hitting the database again
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users_again)