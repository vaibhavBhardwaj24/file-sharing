# Secure File Sharing System

This project implements a secure file-sharing system between two different types of users: **Operation Users (Ops Users)** and **Client Users**. The system is built using Django and provides REST APIs for all major actions.

## Features

### Ops User (Operation User)

- **Login**: Authenticate as an Ops User.
- **Upload File**: Upload files (only `.pptx`, `.docx`, `.xlsx` formats allowed).

### Client User

- **Sign Up**: Register as a Client User. Returns an encrypted URL for further actions.
- **Email Verification**: Receive a verification email to activate the account.
- **Login**: Authenticate as a Client User.
- **Download File**: Download files via a secure, encrypted URL (accessible only by Client Users).
- **List Files**: View all files uploaded by Ops Users.

## Security Requirements

- **File Upload Restrictions**: Only Ops Users can upload files, and only specific file types are allowed.
- **Encrypted Download URLs**: Download links are encrypted and can only be accessed by authenticated Client Users.
- **Access Control**: If any user other than the intended Client User tries to access a download URL, access is denied.

## API Endpoints

### Ops User

- `POST /api/ops/login/` — Login as Ops User
- `POST /api/ops/upload/` — Upload a file (pptx, docx, xlsx only)

### Client User

- `POST /api/client/signup/` — Sign up as Client User (returns encrypted URL)
- `GET /api/client/verify-email/` — Verify email via link
- `POST /api/client/login/` — Login as Client User
- `GET /api/client/files/` — List all uploaded files
- `GET /api/client/download/<encrypted_url>/` — Download file via secure link

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Notes

- Ensure you have configured email backend settings in `settings.py` for email verification.
- All sensitive actions are protected by authentication and role-based access control.
- The system uses Django's built-in security features and custom logic for encrypted URLs.

---

**Author:** Vaibhav Bhardwaj
