import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess  # To run the main.py file after successful login


# =============================
# DATABASE SETUP
# =============================
def setup_database():
    """
    Creates the airline_manage.db SQLite database (if it doesn't exist).
    Also creates the 'users' table where signup information will be stored.
    """
    conn = sqlite3.connect('airline_manage.db')  # Database connection
    cursor = conn.cursor()

    # Create a table if it does not already exist
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
    Handles the user signup process.
    Collects input from fields and inserts into the database.
    Redirects to login page after successful signup.
    """
    first_name = entry_first_name.get().strip()
    last_name = entry_last_name.get().strip()
    email = entry_email.get().strip()
    position = entry_position.get().strip()
    password = entry_password.get().strip()

    # Input validation
    if not first_name or not last_name or not email or not position or not password:
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
        messagebox.showinfo("Success", "User registered successfully")

        # Clear form fields after signup
        clear_fields()

        # Close signup window and open login page
        root.destroy()
        show_login_page()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists. Try logging in.")
    finally:
        conn.close()


def clear_fields():
    """Clears all input fields on the signup form."""
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
    Opens the login window after signup or directly if called.
    Allows users to log in based on their stored credentials.
    """
    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x300")

    # ----------- UI Elements -----------
    tk.Label(login_window, text="First Name").pack(pady=5)
    login_first_name = tk.Entry(login_window)
    login_first_name.pack(pady=5)

    tk.Label(login_window, text="Position (Flight Attendant/Admin)").pack(pady=5)
    login_position = tk.Entry(login_window)
    login_position.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    login_password = tk.Entry(login_window, show='*')
    login_password.pack(pady=5)

    # ----------- Login Function -----------
    def login():
        first_name = login_first_name.get().strip()
        position = login_position.get().strip()
        password = login_password.get().strip()

        if not first_name or not position or not password:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        conn = sqlite3.connect('airline_manage.db')
        cursor = conn.cursor()

        # Verify user details
        cursor.execute('''
            SELECT * FROM users 
            WHERE first_name = ? AND position = ? AND password = ?
        ''', (first_name, position, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", f"Welcome {first_name}! Login successful.")
            login_window.destroy()  # Close login window
            open_main_page()  # Redirect to main page
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    # ----------- Buttons -----------
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    login_window.mainloop()


# ==============================
# REDIRECT TO MAIN.PY
# ==============================
def open_main_page():
    """
    Opens the 'main.py' script as a new process.
    Make sure main.py exists in the same directory.
    """
    try:
        subprocess.Popen(["python", "main.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "main.py not found. Please check the file location.")


# ==============================
# MAIN APPLICATION (SIGNUP FORM)
# ==============================
def main_app():
    """Launches the signup form as the main application window."""
    global entry_first_name, entry_last_name, entry_email, entry_position, entry_password, root

    root = tk.Tk()
    root.title("Airline Management Signup")
    root.geometry("400x400")

    # ----------- UI Elements -----------
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

    # ----------- Signup Button -----------
    signup_button = tk.Button(root, text="Sign Up", command=signup)
    signup_button.pack(pady=20)

    # ----------- Extra Navigation Button -----------
    # Allow user to skip signup and go directly to login page
    login_redirect_button = tk.Button(root, text="Already have an account? Login", command=lambda: [root.destroy(), show_login_page()])
    login_redirect_button.pack(pady=10)

    root.mainloop()


# ==============================
# RUN PROGRAM
# ==============================
if __name__ == "__main__":
    setup_database()
    main_app()
