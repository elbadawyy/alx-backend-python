# 🐍 Python Generators - Task 0: Getting Started

## 📘 Project Overview
This project sets up the **MySQL database** for the ALX Python Generators module.  
It creates the `ALX_prodev` database and seeds it with sample user data from a CSV file.

---

## 🎯 Objective
- Create and connect to a MySQL database (`ALX_prodev`).
- Define the table **`user_data`**.
- Populate it with data from **`user_data.csv`**.
- Validate that the connection, table, and data insertion work properly.

---

## 🧩 Functions Implemented

| Function | Description |
|-----------|--------------|
| `connect_db()` | Connects to the MySQL server (no database selected). |
| `create_database(connection)` | Creates the database `ALX_prodev` if not already present. |
| `connect_to_prodev()` | Connects directly to the `ALX_prodev` database. |
| `create_table(connection)` | Creates the `user_data` table if it does not exist. |
| `insert_data(connection, data)` | Inserts CSV data into the `user_data` table. |

---

## 🧠 Sample Output

```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67),
 ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119),
 ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49)]