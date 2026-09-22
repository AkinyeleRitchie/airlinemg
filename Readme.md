# Readme for Python Airline Management project

# Airline Management System – Admin Panel

This project is a **Tkinter-based Airline Management System** designed for administrators to manage flight information. It integrates a **SQLite database** for storing flight, passenger, and booking data, and also uses **Text-to-Speech (TTS)** functionality to announce flight details.

---

## ✨ Features
- **Database Setup**
  - Automatically creates SQLite tables for `flights`, `passengers`, and `bookings`.
- **Flight Management**
  - Add new flights  
  - Search flights by flight number  
  - Update existing flight details  
  - Delete flights from the database
- **Text-to-Speech Announcements**
  - Announces flight details (using `gTTS` and `pygame`) when a flight is added, updated, or searched.
- **GUI (Tkinter)**
  - Easy-to-use graphical interface for administrators
  - Input fields for flight details
  - Buttons for `Add`, `Search`, `Update`, and `Delete`

---

## 🛠️ Technologies Used
- **Python 3**
- **SQLite3** – Database
- **Tkinter** – GUI
- **gTTS (Google Text-to-Speech)** – Voice announcements
- **pygame** – Audio playback
- **Pillow (PIL)** – Image handling (optional, if extended)

---

## 📂 Project Structure
- `main.py` / `mainn.py` - Entry points for running the application.
- `Admin.py` - Handles administrative workflows and permissions.
- `Flight.py` - Manages flight-related logic and data structures.
- `Email_Signup.py` / `EmailSignupandLogin.py` - Manages authentication modules.
- `tts.py` - Text-to-speech functionality.
- `*.db` - Local databases used for data storage.

## Getting Started
1. Clone the repository.
2. Ensure you have Python installed.
3. Run the application using:
   ```bash
   python main.py
