# ---------------------------------------
# Airline Management Database Setup Script
# ---------------------------------------
# This script initializes the SQLite database for
# the Airline Management System.
#
# It creates three tables:
# 1. flights   - Stores flight details
# 2. passengers - Stores passenger information
# 3. bookings  - Stores passenger bookings for flights
#
# Running this script ensures that the database is ready
# before launching the main application.
# ----------------------------------------

import sqlite3


def setup_database():
    """Create the SQLite database with flights, passengers, and bookings tables."""
    
    # Connect to (or create) the database file
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()
    
    # ------------------------
    # Create flights table
    # ------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number VARCHAR NOT NULL,
            origin VARCHAR NOT NULL,
            destination VARCHAR NOT NULL,
            departure_time VARCHAR NOT NULL,
            arrival_time VARCHAR NOT NULL
        )
    ''')
     
    # ------------------------
    # Create passengers table
    # ------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            passport_number TEXT UNIQUE NOT NULL,
            contact_info TEXT NOT NULL
        )
    ''')
    
    # ------------------------
    # Create bookings table
    # ------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            seat_number TEXT,
            FOREIGN KEY(passenger_id) REFERENCES passengers(id),
            FOREIGN KEY(flight_id) REFERENCES flights(id)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("✅ Database setup complete! Tables are ready.")


# Run setup when script is executed
if __name__ == "__main__":
    setup_database()
