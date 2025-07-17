# Secure File Sharing System

This project implements a secure file-sharing system between two types of users: **Operator Users (Admins)** and **Client Users**. The backend is built with Django, MongoEngine (MongoDB), and Redis, and provides REST APIs for authentication, file upload, secure link generation, and file download.

---

## Features

### Operator (Admin) User

- **Login**: Authenticate as an operator (admin) user.
- **Upload File**: Upload files (`.pptx`, `.docx`, `.xlsx` only).

### Client User

- **Sign Up**: Register as a client user.
- **Login**: Authenticate as a client user.
- **List Files**: View all files uploaded by operators.
- **Generate Download Link**: Request a secure, time-limited download link for a file.
- **Download File**: Download files via a secure, temporary link.

---

## Security

- **Role-based Access**: Only operators can upload files; only clients can generate download links.
- **File Type Restriction**: Only specific file types are allowed for upload.
- **JWT Authentication**: All protected endpoints require a valid JWT token.
- **Temporary Download Links**: Download links are valid for 10 minutes and are stored in Redis.
- **No orphaned access**: If a user or file is missing, access is denied.
- **File Upload Restrictions**: Only Ops Users can upload files, and only specific file types are allowed.

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

- `POST /api/auth/signup/` — Client user signup
- `POST /api/auth/login/` — Login (returns JWT and user role)

### File Operations

- `POST /api/file/upload/` — Upload a file (operator only, JWT required)
- `POST /api/file/generateLink/` — Generate a secure download link for a file (client only, JWT required)
- `GET /api/media/<file_id>/` — Download a file using a secure link (valid for 10 minutes)
- `GET /api/links/` — List all files (client only, JWT required)

### Test

- `GET /api/test/` — Test endpoint for JWT validation

---

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**  
   Create a `.env` file with:
   ```
   MONGO_DB_NAME=your_db_name
   MONGO_URI=mongodb://localhost:27017/your_db_name
   REDIS_URL=redis://localhost:6379/0
   ```
4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## Notes

- Ensure MongoDB and Redis are running and accessible.
- JWT secret is set via Django's `SECRET_KEY` in `settings.py`.
- File uploads are stored in the `uploads/` directory.
- Download links are managed via Redis and expire after 10 minutes.
- The project uses custom JWT logic (not SimpleJWT) for authentication.

---

**Author:** Vaibhav Bhardwaj
