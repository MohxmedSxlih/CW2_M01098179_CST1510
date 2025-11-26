# Week 7: Secure Authentication System

**Student Name:** MOHAMED SALIH BIN MAJEED  
**Student ID:** M01098179  
**Course:** CST1510 - CW2 - Multi-Domain Intelligence Platform  

---

## 📌 Project Description

This project implements a secure authentication system using Python and the `bcrypt` library.  
It allows users to register and log in through a command-line interface while ensuring passwords are protected using secure hashing.

The system uses file-based storage to maintain user credentials and includes input validation to ensure data integrity.

---

## 🔐 Features

- Secure password hashing with bcrypt (automatic salting)
- User registration with duplicate username prevention
- Password verification using bcrypt
- Username and password validation
- File-based user data persistence (`users.txt`)
- Clear error messaging and user prompts

---

## 🛠️ Technical Implementation

- **Hashing Algorithm:** bcrypt with automatic salting  
- **Data Storage:** Plain text file (`users.txt`) using comma-separated values  
- **Password Security:** One-way hashing (no plaintext passwords saved)  
- **Username Validation:** 3–20 alphanumeric characters  
- **Password Validation:** 6–50 characters  

---

## 📂 File Structure

