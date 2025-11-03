#!/usr/bin/python3
"""
seed.py - Setup MySQL database and seed data for the ALX Python Generators project.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here'  # ⚠️ Replace with your MySQL root password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully (if not existed).")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # ⚠️ Replace with your MySQL root password
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,2) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data from a CSV file into the user_data table."""
    try:
        cursor = connection.cursor()

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = float(row['age'])

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )

        connection.commit()
        print(f"Data inserted successfully from {csv_file}")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
