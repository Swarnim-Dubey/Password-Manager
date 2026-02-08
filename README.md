# 🔐 Password Manager (Desktop Vault)

A secure, modern desktop password manager built with Python, featuring strong encryption, a clean GUI, and local-first privacy.

---

## 📌 Overview

**Password Manager** is a lightweight yet secure desktop application that allows users to store, manage, and retrieve credentials safely using a **master password–protected encrypted vault**.

All sensitive data is encrypted locally and stored in a SQLite database — **no cloud, no tracking, no external servers**.

This project is designed for **personal use**, **learning secure software design**, and as a **portfolio-grade desktop application**.

---

## 💡 Motivation

Managing multiple online accounts often leads to:
- Password reuse  
- Weak or predictable passwords  
- Insecure storage practices  

This application solves that problem by providing a **locally encrypted vault** that only the user can unlock using a master password.

---

## 🚀 Features

### 🔐 Security
- Master password protection using **bcrypt hashing**
- AES-256 encryption for all stored credentials
- Encryption keys derived from the master password
- Base64 encoding for safe handling of encrypted data
- Master password is **never stored in plain text**

### 🖥️ Desktop Application
- Modern GUI built with **PySide6 (Qt)**
- Custom frameless window with animations
- Category-based credential organization
- Secure re-authentication before revealing passwords

### 📂 Data Handling
- Local SQLite database
- App data stored securely in the OS user directory
- Credential-level deletion (no accidental bulk deletes)
- Hot-reload UI after add/delete operations

### 📦 Distribution
- Standalone `.exe` built using PyInstaller
- Installer created with Inno Setup
- No Python or dependencies required on target systems

---

## 🛠️ Tech Stack

| Component | Technology |
|---------|------------|
| Language | Python |
| GUI | PySide6 (Qt) |
| Database | SQLite |
| Encryption | AES-256 (Fernet) |
| Hashing | bcrypt |
| Encoding | Base64 |
| Packaging | PyInstaller |
| Installer | Inno Setup |

---

## 🔐 Security Architecture

- Master password → **bcrypt hash** → stored securely
- Master password → **SHA-256 derived key** → AES-256 encryption
- Credential passwords → encrypted → Base64 encoded
- Only encrypted data is persisted in the database
- Decryption occurs **only in memory after authentication**

> ⚠️ Note: Base64 is not encryption — it is used only for safe storage of encrypted bytes.

---

## 🛣️ Future Updates (Planned)

The following enhancements are planned for future releases:

- 🔑 Built-in strong password generator
- 🔄 Optional encrypted cloud synchronization
- ⏱ Automatic vault locking after inactivity
- 📋 Clipboard auto-clear after copying passwords
- 🧠 Security audit & threat modeling
- 🧩 Plugin system for extensibility
- 🌐 Browser extension integration
- 📱 Mobile companion application
- 🧾 Import/export support (CSV / encrypted backup)
- 🎨 Theme customization (light/dark modes)

---

## ⚠️ Disclaimer

This project is intended for **educational and personal use**.  
While strong cryptographic primitives are used, the application has **not undergone a formal security audit**.  
Use at your own discretion.

---

## 🙌 Author

Built with care and curiosity by **ME 😂**  
If you find this project useful, feel free to ⭐ star the repository.

---

## 📜 License

MIT License — free to use, modify, and distribute.
