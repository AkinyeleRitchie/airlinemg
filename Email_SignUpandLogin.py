
import tkinter as tk
from tkinter import messagebox
import sqlite3


# ============================
# DATABASE SETUP
# ============================
def setup_database():
    """
    Create the database file (airline_management.db) if it doesn't exist.
    Also ensures a 'users' table is created for storing signup data.
    """
    conn = sqlite3.connect('airline_management.db')  # ✅ fixed typo in filename
    cursor = conn.cursor()

    # Create table with basic constraints
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


# ==============================
# SIGNUP LOGIC
# ==============================
def signup():
    """
    Handles signup by inserting user details into the database.
    After successful signup → redirects to login page.
    """
    first_name = entry_first_name.get().strip()
    last_name = entry_last_name.get().strip()
    email = entry_email.get().strip()
    position = entry_position.get().strip()
    password = entry_password.get().strip()

    # Validate inputs
    if not first_name or not last_name or not email or not position or not password:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    try:
        # Insert new user
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, position, password) 
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, position, password))

        conn.commit()
        messagebox.showinfo("Success", f"Account created successfully for {first_name}!")

        # Reset fields after successful signup
        clear_fields()

        # Close signup window and show login page
        root.destroy()
        show_login_page()

    except sqlite3.IntegrityError:
        # Prevent duplicate email registrations
        messagebox.showerror("Error", "Email already exists. Try logging in instead.")
    finally:
        conn.close()


def clear_fields():
    """Clear all input fields on the signup form."""
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_password.delete(0, tk.END)


# ==============================
# LOGIN LOGIC
# ==============================
def show_login_page():
    """
    Opens a login window where users can log into their account.
    Validates against stored data in the database.
    """
    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x300")

    # -------- UI Components --------
    tk.Label(login_window, text="First Name").pack(pady=5)
    login_first_name = tk.Entry(login_window)
    login_first_name.pack(pady=5)

    tk.Label(login_window, text="Position (Flight Attendant/Admin)").pack(pady=5)
    login_position = tk.Entry(login_window)
    login_position.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    login_password = tk.Entry(login_window, show='*')
    login_password.pack(pady=5)

    # -------- LOGIN FUNCTION --------
    def login():
        first_name = login_first_name.get().strip()
        position = login_position.get().strip()
        password = login_password.get().strip()

        if not first_name or not position or not password:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute('''
            SELECT * FROM users 
            WHERE first_name = ? AND position = ? AND password = ?
        ''', (first_name, position, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", f"Welcome {first_name}! You are logged in.")
            login_window.destroy()  # Close login window after success
        else:
            messagebox.showerror("Error", "Invalid credentials. Try again.")

    # -------- BUTTON --------
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    login_window.mainloop()


# ==============================
# MAIN APPLICATION (SIGNUP)
# ==============================
def main_app():
    """Main signup window (entry point of the program)."""
    global entry_first_name, entry_last_name, entry_email, entry_position, entry_password, root

    root = tk.Tk()
    root.title("Airline Management Signup")
    root.geometry("400x400")

    # -------- UI Components --------
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

    # -------- Buttons --------
    signup_button = tk.Button(root, text="Sign Up", command=signup)
    signup_button.pack(pady=20)

    login_redirect = tk.Button(root, text="Already have an account? Login", command=lambda: [root.destroy(), show_login_page()])
    login_redirect.pack(pady=10)

    root.mainloop()


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    setup_database()
    main_app()
