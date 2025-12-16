# 🔐 Password Manager 
A secure password manager built with Python, using AES‑256 encryption and Base64 encoding.

## 📌 Overview
A secure, lightweight desktop-based Password Manager built with Python. This application allows users to safely store, retrieve, and manage credentials using strong encryption and a local SQLite database. It is ideal for personal use or as a learning-focused security project.

## 💡 Idea
Managing multiple online accounts often leads to password reuse and weak security. This Password Manager addresses that issue by providing a secure, encrypted vault protected by a master password.

## 🚀 Features
- Secure local credential storage using SQLite  
- Master password protection with bcrypt hashing  
- AES-256 encryption for stored credentials  
- Base64 encoding for safe handling of encrypted data  
- Simple and intuitive desktop GUI

## 🛠️ Tech Stack
- **Language:** Python  
- **GUI Framework:** PyQt  
- **Database:** SQLite  
- **Security:** bcrypt, AES-256, Base64  
- **Packaging:** PyInstaller  

## 🔐 Security Architecture
- The master password is hashed using bcrypt and never stored in plain text  
- Credential passwords are Base64-encoded before encryption  
- AES-256 encrypts all stored credentials  
- Encryption keys are derived from the master password  
- Only encrypted data is stored in the database  
