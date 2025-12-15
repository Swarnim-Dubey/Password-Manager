# Password-Manager
A secure desktop password manager built with Python, using AES‑256 encryption and Base64 encoding.


📌 Overview
This project is a secure desktop-based Password Manager built with Python. It allows users to safely store, retrieve, and manage their credentials in an encrypted local database. The app is designed to be lightweight, user-friendly, and secure — perfect for personal use or as a learning project.

💡 Idea
Managing multiple accounts often leads to weak or reused passwords. This Password Manager addresses that problem by:

Storing credentials in a local SQLite database.

Encoding sensitive data with Base64 before encryption.

Protecting access with a master password (hashed with bcrypt).

Encrypting credentials using AES-256 for strong security.

Providing a simple GUI for easy interaction.

🚀 Execution Roadmap
1. Core Setup
- Initialize SQLite database with tables for users and credentials.

- Implement master password setup and verification using bcrypt.

- Configure AES-256 encryption logic.

- Use Base64 encoding to safely store encrypted binary data in the database.

2. Authentication
- First-time setup: prompt user to create a master password.

- Store master password hash securely.

- On subsequent runs: verify master password before unlocking vault.

3. Credential Management
- Add new credentials (service, username, password).

- Convert password string into Base64.

- Encrypt Base64 string using AES-256.

- Store encrypted data in the database.

- Retrieve credentials by decrypting with AES-256 and decoding from Base64.

- Copy credentials to clipboard with auto-clear feature.

4. GUI Development
- Built with PyQt for UI.

Screens:

- Login screen (master password).

- Dashboard (view, add, search credentials).

5. Security Enhancements
- Auto-lock after inactivity.

- Clipboard auto-clear after a few seconds.

- Optional two-factor authentication.

6. Packaging
- Bundle into a standalone executable using PyInstaller.

- Cross-platform support (Windows, Mac, Linux).

🔐 How Encryption Works
- The password storage process follows a layered protection model:

1. String Input

- User enters a password in plain text.

2. Base64 Encoding

- The string is converted into Base64.

- This ensures safe representation of the data.

3. AES-256 Encryption

- The Base64-encoded string is encrypted using AES-256.

- The encryption key is derived from the master password.

4. Database Storage

- The final AES-encrypted data is stored in the SQLite database.

5. Retrieval Process

- Encrypted data is decrypted with AES-256.

- The result is decoded from Base64 back into the original password string.

⚙️ Tech Stack
- Language: Python

- GUI Framework: Tkinter / PyQt

- Database: SQLite

- Security: bcrypt (hashing), Base64 (encoding), AES-256 (encryption)

- Packaging: PyInstaller

🔮 Future Improvements
- Password generator for strong random passwords.

- Cloud sync for encrypted vaults.

- Advanced password analytics.
