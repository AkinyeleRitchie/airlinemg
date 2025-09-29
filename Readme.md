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

