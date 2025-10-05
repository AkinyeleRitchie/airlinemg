# ----------------------------------------
# Airline Management System - User Signup GUI
# ----------------------------------------
# Features:
# - Uses SQLite for user storage
# - Signup form with First Name, Last Name, Email, Position, Password
# - Prevents duplicate email registration
# - Clears fields after successful signup
#
# Tables:
#   users(id, first_name, last_name, email, position, password)
#
# NOTE: Passwords are stored in plain text in this version.
#       In production, you should hash passwords (e.g., bcrypt).
# ------------------------------------------

import tkinter as tk
from tkinter import messagebox
import sqlite3


# ------------------------------------------
# Database setup
# ------------------------------------------
def setup_database():
    """Create the users table if it doesn’t already exist."""
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            position TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# ------------------------------------------
# Signup Logic
# ------------------------------------------
def signup():
    """Insert a new user into the database after validating inputs."""
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    position = entry_position.get()
    password = entry_password.get()

    # Validation: Ensure all fields are filled
    if first_name == "" or last_name == "" or email == "" or position == "" or password == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    try:
        # Insert user into database
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, position, password) 
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, position, password))

        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
        clear_fields()  # Reset form after signup

    except sqlite3.IntegrityError:
        # Email must be unique
        messagebox.showerror("Error", "Email already exists")
    finally:
        conn.close()


# ------------------------------------------
# Clear input fields
# ------------------------------------------
def clear_fields():
    """Clear all entry fields after signup."""
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_password.delete(0, tk.END)


# ------------------------------------------
# Main Application GUI
# ------------------------------------------
def main_app():
    """Build and run the Tkinter signup window."""
    global entry_first_name, entry_last_name, entry_email, entry_position, entry_password

    root = tk.Tk()
    root.title("Airline Management - Signup")
    root.geometry("400x450")
    root.config(bg="#f0f0f0")  # Light background for better visuals

    # Title Label
    tk.Label(root, text="User Signup", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

    # First Name
    tk.Label(root, text="First Name", bg="#f0f0f0").pack(pady=5)
    entry_first_name = tk.Entry(root, width=30)
    entry_first_name.pack(pady=5)

    # Last Name
    tk.Label(root, text="Last Name", bg="#f0f0f0").pack(pady=5)
    entry_last_name = tk.Entry(root, width=30)
    entry_last_name.pack(pady=5)

    # Email
    tk.Label(root, text="Email", bg="#f0f0f0").pack(pady=5)
    entry_email = tk.Entry(root, width=30)
    entry_email.pack(pady=5)

    # Position
    tk.Label(root, text="Position (Flight Attendant/Admin)", bg="#f0f0f0").pack(pady=5)
    entry_position = tk.Entry(root, width=30)
    entry_position.pack(pady=5)

    # Password
    tk.Label(root, text="Password", bg="#f0f0f0").pack(pady=5)
    entry_password = tk.Entry(root, show='*', width=30)  # Mask password input
    entry_password.pack(pady=5)

    # Signup Button
    signup_button = tk.Button(root, text="Sign Up", command=signup, bg="green", fg="white", width=15)
    signup_button.pack(pady=20)

    # Quit Button
    quit_button = tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white", width=15)
    quit_button.pack(pady=5)

    root.mainloop()


# ------------------------------------------
# Entry Point
# ------------------------------------------
if __name__ == "__main__":
    setup_database()  # Ensure database exists
    main_app()        # Launch the signup app
