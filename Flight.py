from gtts import gTTS
from tkinter import *
import tkinter.messagebox as messagebox
import sqlite3
import os
import pygame
import random

# ==========================
# DATABASE INITIALIZATION
# ==========================
def setup_database():
    """Create the airline management database and tables if they do not exist."""
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

# Run DB setup at program start
setup_database()


# ==========================
# TEXT-TO-SPEECH FUNCTION
# ==========================
def text_to_speech(text):
    """
    Converts given text into speech and plays it using pygame.
    The temporary MP3 file is deleted after playback.
    """
    try:
        tts = gTTS(text=text, lang='en')
        audio_file = "flight_info.mp3"
        tts.save(audio_file)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  # Wait until the audio finishes
            continue

        pygame.mixer.quit()
        os.remove(audio_file)
    except Exception as e:
        messagebox.showerror("TTS Error", f"Could not play audio: {e}")


# ==========================
# PASSENGER MANAGEMENT
# ==========================
def save_passenger():
    """Save passenger details into the database."""
    # Retrieve values from input fields
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    passport_number = passport_number_entry.get()
    contact_info = contact_info_entry.get()

    # Validation check
    if not all([name, age, gender, passport_number, contact_info]):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    # Check if passport number already exists
    cursor.execute("SELECT COUNT(*) FROM passengers WHERE passport_number = ?", (passport_number,))
    exists = cursor.fetchone()[0]

    if exists:
        messagebox.showerror("Duplicate Entry", "A passenger with this passport number already exists.")
    else:
        cursor.execute('''
            INSERT INTO passengers (name, age, gender, passport_number, contact_info)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, gender, passport_number, contact_info))
        conn.commit()
        messagebox.showinfo("Success", f"Passenger {name} added successfully.")
        
        # Optional: Announce passenger registration using TTS
        text_to_speech(f"Passenger {name} has been added successfully.")

        clear_passenger_fields()

    conn.close()


def clear_passenger_fields():
    """Clears passenger input fields after saving."""
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)
    passport_number_entry.delete(0, END)
    contact_info_entry.delete(0, END)


# ==========================
# BOOKING MANAGEMENT
# ==========================
def generate_seat_number():
    """Generate a random seat number in the format '001-A'."""
    seat_number = f"{random.randint(1, 150):03d}"
    seat_row = random.choice(['A', 'B', 'C', 'D'])
    return f"{seat_number}-{seat_row}"


def book_flight(passenger_id, flight_id):
    """Book a passenger on a flight if not already booked."""
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    # Verify passenger and flight IDs exist
    cursor.execute("SELECT COUNT(*) FROM passengers WHERE id = ?", (passenger_id,))
    passenger_exists = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM flights WHERE id = ?", (flight_id,))
    flight_exists = cursor.fetchone()[0]

    if not passenger_exists:
        messagebox.showerror("Error", "Passenger ID does not exist.")
        conn.close()
        return

    if not flight_exists:
        messagebox.showerror("Error", "Flight ID does not exist.")
        conn.close()
        return

    # Check if passenger already booked
    cursor.execute('''
        SELECT COUNT(*) FROM bookings
        WHERE passenger_id = ? AND flight_id = ?
    ''', (passenger_id, flight_id))
    already_booked = cursor.fetchone()[0]

    if already_booked:
        messagebox.showwarning("Booking Error", "This passenger is already booked on this flight.")
    else:
        seat_number = generate_seat_number()
        cursor.execute('''
            INSERT INTO bookings (passenger_id, flight_id, seat_number)
            VALUES (?, ?, ?)
        ''', (passenger_id, flight_id, seat_number))
        conn.commit()
        messagebox.showinfo("Success", f"Flight booked successfully! Seat number: {seat_number}")

        # Optional: Announce booking
        text_to_speech(f"Passenger {passenger_id} booked successfully on flight {flight_id}. Seat number {seat_number}.")

        clear_booking_fields()

    conn.close()


def submit_booking():
    """Handles the booking button click."""
    passenger_id = passenger_id_entry.get()
    flight_id = flight_id_entry.get()

    if not passenger_id.isdigit() or not flight_id.isdigit():
        messagebox.showwarning("Input Error", "Please enter valid numeric IDs.")
        return

    book_flight(int(passenger_id), int(flight_id))


def clear_booking_fields():
    """Clear booking input fields after successful booking."""
    passenger_id_entry.delete(0, END)
    flight_id_entry.delete(0, END)


# ==========================
# GUI SETUP
# ==========================
root = Tk()
root.title("Airline Management System")
root.geometry("1200x720")

# Left-side frame for inputs
left_frame = Frame(root, width=400, height=600, bg="lightblue")
left_frame.pack(side=LEFT, fill=BOTH, expand=True)

# Heading
Label(left_frame, text="Passenger Management", font=("Arial", 20, "bold"), bg="lightblue").place(x=170, y=100)

# Passenger input fields
Label(left_frame, text="Passenger Name", bg="lightblue").place(x=190, y=167)
name_entry = Entry(left_frame); name_entry.place(x=330, y=170)

Label(left_frame, text="Passenger Age", bg="lightblue").place(x=190, y=217)
age_entry = Entry(left_frame); age_entry.place(x=330, y=220)

Label(left_frame, text="Passenger Gender", bg="lightblue").place(x=190, y=267)
gender_entry = Entry(left_frame); gender_entry.place(x=330, y=270)

Label(left_frame, text="Passport Number", bg="lightblue").place(x=190, y=317)
passport_number_entry = Entry(left_frame); passport_number_entry.place(x=330, y=320)

Label(left_frame, text="Contact Info", bg="lightblue").place(x=190, y=367)
contact_info_entry = Entry(left_frame); contact_info_entry.place(x=330, y=370)

# Booking input fields
Label(left_frame, text="Passenger ID", bg="lightblue").place(x=190, y=457)
passenger_id_entry = Entry(left_frame); passenger_id_entry.place(x=330, y=460)

Label(left_frame, text="Flight ID", bg="lightblue").place(x=190, y=507)
flight_id_entry = Entry(left_frame); flight_id_entry.place(x=330, y=510)

# Buttons
Button(left_frame, text="Save Passenger", command=save_passenger, bg="green", fg="white").place(x=330, y=410)
Button(left_frame, text="Book Flight", command=submit_booking, fg="green", bg="white").place(x=330, y=550)

# Run GUI loop
root.mainloop()
