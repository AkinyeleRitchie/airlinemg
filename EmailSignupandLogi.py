# ---------------------------------------------------
# Airline Management System - Signup & Login
# ---------------------------------------------------
# This script handles:
# 1. User signup (Admin / Flight Attendant)
# 2. User login (redirects to the correct panel)
# 3. Database setup for user authentication
#
# After a successful login:
#   - Admins -> open admin.py
#   - Flight Attendants -> open flight.py
# ---------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess   # To run external scripts like admin.py / flight.py


# -----------------------------
# Database Setup
# -----------------------------
def setup_database():
    """Initialize the SQLite database and create users table if not exists."""
    conn = sqlite3.connect('airline_manage.db')
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


# -----------------------------
# Signup Function
# -----------------------------
def signup():
    """Register a new user and redirect to login page."""
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    position = entry_position.get()
    password = entry_password.get()

    # Ensure all fields are filled
    if not all([first_name, last_name, email, position, password]):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn = sqlite3.connect('airline_manage.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, position, password) 
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, position, password))

        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")

        # Clear input fields
        clear_fields()

        # Destroy signup window and open login page
        root.destroy()
        show_login_page()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists. Please log in instead.")
    finally:
        conn.close()


# -----------------------------
# Utility: Clear Input Fields
# -----------------------------
def clear_fields():
    """Reset signup form fields."""
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_password.delete(0, tk.END)


# -----------------------------
# Login Page
# -----------------------------
def show_login_page():
    """Display login form after signup or direct start."""
    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x300")

    # Labels & entry fields
    tk.Label(login_window, text="First Name").pack(pady=5)
    login_first_name = tk.Entry(login_window)
    login_first_name.pack(pady=5)

    tk.Label(login_window, text="Position (Flight Attendant/Admin)").pack(pady=5)
    login_position = tk.Entry(login_window)
    login_position.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    login_password = tk.Entry(login_window, show='*')
    login_password.pack(pady=5)

    def login():
        """Handle user login verification."""
        first_name = login_first_name.get()
        position = login_position.get()
        password = login_password.get()

        if not all([first_name, position, password]):
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        conn = sqlite3.connect('airline_manage.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE first_name = ? AND position = ? AND password = ?
        ''', (first_name, position, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", f"Welcome {first_name}! Login successful.")
            login_window.destroy()

            # Redirect user based on role
            if position.lower() == "admin":
                open_admin_page()
            elif position.lower() == "flight attendant":
                open_flight_attendant_page()
            else:
                messagebox.showerror("Error", "Invalid position. Please choose Admin or Flight Attendant.")
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    # Login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    login_window.mainloop()


# -----------------------------
# External Process Launchers
# -----------------------------
def open_admin_page():
    """Open admin.py in a new process (Admin Panel)."""
    subprocess.Popen(["python", "admin.py"])  # Or "python3" on Linux/macOS


def open_flight_attendant_page():
    """Open flight.py in a new process (Flight Attendant Panel)."""
    subprocess.Popen(["python", "flight.py"])  # Or "python3" on Linux/macOS


# -----------------------------
# Main Signup Form
# -----------------------------
def main_app():
    """Display signup form."""
    global entry_first_name, entry_last_name, entry_email, entry_position, entry_password, root

    root = tk.Tk()
    root.title("Airline Management - Signup")
    root.geometry("400x400")

    # Labels and entry fields
    tk.Label(root, text="First Name").pack(pady=5)
    entry_first_name = tk.Entry(root)
    entry_first_name.pack(pady=5)

    tk.Label(root, text="Last Name").pack(pady=5)
    entry_last_name = tk.Entry(root)
    entry_last_name.pack(pady=5)

    tk.Label(root, text="Email").pack(pady=5)
    entry_email = tk.Entry(root)
    entry_email.pack(pady=5)

    tk.Label(root, text="Position (Flight Attendant/Admin)").pack(pady=5)
    entry_position = tk.Entry(root)
    entry_position.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)
    entry_password = tk.Entry(root, show='*')
    entry_password.pack(pady=5)

    # Signup button
    signup_button = tk.Button(root, text="Sign Up", command=signup)
    signup_button.pack(pady=20)

    root.mainloop()


# -----------------------------
# App Entry Point
# -----------------------------
if __name__ == "__main__":
    setup_database()   # Ensure DB exists
    main_app()         # Start with signup
