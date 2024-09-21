import sqlite3

# SQL commands to create tables
sql_commands = """
-- Create the students table
CREATE TABLE students033 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT NOT NULL
);

-- Create the attendance table
CREATE TABLE attendance033 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    date DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Create the performance table
CREATE TABLE performance033 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
"""

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Execute the SQL commands
cursor.executescript(sql_commands)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")
