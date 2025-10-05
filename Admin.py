# ------------------------------
# Airline Management System (Admin Panel)
# ------------------------------
# Features:
# - Add, Search, Update, and Delete Flights
# - Uses SQLite for persistent storage
# - GUI built with Tkinter
# - Text-to-Speech announcements using gTTS + pygame
# - Can be extended later for passengers & bookings
# ---------------------------

from gtts import gTTS
from tkinter import *
import tkinter.messagebox as messagebox
import sqlite3
import os
import pygame

# -------------------------------
# Database Setup
# -------------------------------
def setup_database():
    """Initialize the SQLite database with flights, passengers, and bookings tables."""
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()
    
    # Create flights table
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
    
    # Create passengers table
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
    
    # Create bookings table
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
    
    conn.commit()
    conn.close()

setup_database()  # Ensure database is ready before GUI starts


# -------------------------------
# Text-to-Speech (gTTS + pygame)
# -------------------------------
def text_to_speech(text):
    """Convert text to speech and play it using pygame."""
    tts = gTTS(text=text, lang='en')
    audio_file = "flight_info.mp3"
    tts.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    # Keep program running until audio finishes
    while pygame.mixer.music.get_busy():
        continue
    
    pygame.mixer.quit()
    os.remove(audio_file)  # Remove temp audio file after playing


# -------------------------------
# Utility: Clear all entry fields
# -------------------------------
def clear_entries():
    """Clear all entry fields after an action."""
    flight_number_entry.delete(0, END)
    origin_entry.delete(0, END)
    destination_entry.delete(0, END)
    departure_time_entry.delete(0, END)
    arrival_time_entry.delete(0, END)


# -------------------------------
# Add Flight
# -------------------------------
def add():
    """Add a new flight to the database."""
    flight_number = flight_number_entry.get()
    origin = origin_entry.get()
    destination = destination_entry.get()
    departure_time = departure_time_entry.get()
    arrival_time = arrival_time_entry.get()

    if flight_number and origin and destination and departure_time and arrival_time:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (flight_number, origin, destination, departure_time, arrival_time))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Flight added successfully!")
        
        # Announce the added flight
        flight_info = (f"Flight {flight_number} from {origin} to {destination} "
                       f"has been successfully added. Departure at {departure_time} "
                       f"and arrival at {arrival_time}.")
        text_to_speech(flight_info)
        
        clear_entries()
    else:
        messagebox.showinfo("Alert", "Please fill in all fields.")


# -------------------------------
# Search Flight
# -------------------------------
def search():
    """Search for a flight by its number and announce details."""
    flight_number = flight_number_entry.get()

    if flight_number:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT flight_number, origin, destination, departure_time, arrival_time
            FROM flights
            WHERE flight_number = ?
        ''', (flight_number,))
        
        result = cursor.fetchone()
        conn.close()

        if result:
            flight_info = (f"Flight {result[0]} from {result[1]} to {result[2]} "
                           f"departs at {result[3]} and arrives at {result[4]}.")
            text_to_speech(flight_info)
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please enter a flight number to search.")


# -------------------------------
# Update Flight
# -------------------------------
def update():
    """Update existing flight details in the database."""
    flight_number = flight_number_entry.get()
    origin = origin_entry.get()
    destination = destination_entry.get()
    departure_time = departure_time_entry.get()
    arrival_time = arrival_time_entry.get()

    if flight_number and origin and destination and departure_time and arrival_time:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE flights 
            SET origin = ?, destination = ?, departure_time = ?, arrival_time = ? 
            WHERE flight_number = ?
        ''', (origin, destination, departure_time, arrival_time, flight_number))

        conn.commit()

        if cursor.rowcount > 0:  # FIXED: used rowcount instead of xcount
            messagebox.showinfo("Success", f"Flight {flight_number} updated successfully.")
            
            flight_info = (f"Flight {flight_number} has been successfully updated. "
                           f"It will now depart from {origin} to {destination} at {departure_time} "
                           f"and arrive at {arrival_time}.")
            text_to_speech(flight_info)
            clear_entries()
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please fill in all fields.")


# -------------------------------
# Delete Flight
# -------------------------------
def delete():
    """Delete a flight from the database."""
    flight_number = flight_number_entry.get()

    if flight_number:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM flights WHERE flight_number = ?
        ''', (flight_number,))
        
        conn.commit()

        if cursor.rowcount > 0:  # FIXED: used rowcount instead of xcount
            messagebox.showinfo("Success", f"Flight {flight_number} deleted successfully.")
            flight_info = f"Flight {flight_number} has been successfully deleted."
            text_to_speech(flight_info)
            clear_entries()
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")

        conn.close()
    else:
        messagebox.showinfo("Alert", "Please enter a flight number to delete.")


# -------------------------------
# Tkinter GUI Setup
# -------------------------------
root = Tk()
root.title("Airline Management System")

# Right frame (Admin panel)
right_frame = Frame(root, width=400, height=600, bg="lightgray")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Heading
heading_label = Label(right_frame, text="ADMINISTRATOR'S PANEL", 
                      font=("Arial", 20, "bold"), bg="lightgray")
heading_label.place(x=100, y=15)

# Labels for inputs
Label(right_frame, text="Flight Number", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=120)
Label(right_frame, text="Origin", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=170)
Label(right_frame, text="Destination", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=220)
Label(right_frame, text="Departure Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=270)
Label(right_frame, text="Arrival Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=320)

# Input fields
flight_number_entry = Entry(right_frame)
origin_entry = Entry(right_frame)
destination_entry = Entry(right_frame)
departure_time_entry = Entry(right_frame)
arrival_time_entry = Entry(right_frame)

# Place input fields
flight_number_entry.place(x=280, y=125)
origin_entry.place(x=280, y=175)
destination_entry.place(x=280, y=225)
departure_time_entry.place(x=280, y=275)
arrival_time_entry.place(x=280, y=325)

# Buttons for actions
add_button = Button(right_frame, text="Add Flight", command=add)
add_button.place(x=180, y=380)

search_button = Button(right_frame, text="Search Flight", command=search)
search_button.place(x=280, y=380)

update_button = Button(right_frame, text="Update Flight", command=update)
update_button.place(x=180, y=430)

delete_button = Button(right_frame, text="Delete Flight", command=delete)
delete_button.place(x=280, y=430)

# Window size
root.geometry("1200x720")
root.mainloop()
