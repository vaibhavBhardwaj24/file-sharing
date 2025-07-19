# Secure File Sharing System

This project implements a secure file-sharing system between two types of users: **Operator Users (Admins)** and **Client Users**. The backend is built with Django, MongoEngine (MongoDB), Redis, and Celery, and provides REST APIs for authentication, file upload, secure link generation, and file download.

---

## Features

### Operator (Admin) User

- **Login**: Authenticate as an operator (admin) user.
- **Upload File**: Upload files (`.pptx`, `.docx`, `.xlsx` only).

### Client User

- **Sign Up**: Register as a client user (requires email verification).
- **Email Verification**: Receive a verification email with a link (valid for 10 minutes) to activate your account. Email is sent asynchronously using Celery.
- **Login**: Authenticate as a client user (only after verifying email).
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
- **Email Verification**: Client users must verify their email before accessing client features. Verification links expire after 10 minutes.

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

- `POST /api/auth/signup/` — Client user signup (triggers verification email)
- `POST /api/auth/login/` — Login (returns JWT and user role)
- `POST /api/verify-email/<token>/` — Verify client account using the token sent via email

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
   DOMAIN=localhost:8000  # or your deployed domain, used for email verification links
   ```
4. **Configure Email Backend**
   - The project uses Gmail SMTP for sending emails. Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `settings.py` or as environment variables. `EMAIL_HOST_PASSWORD` should be an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if using Gmail.
5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
6. **Start Celery worker** (in a separate terminal):
   ```bash
   celery -A fileShare worker --loglevel=info
   ```

---

## Postman Collection

You can use the provided Postman collection to test all API endpoints easily:

- [Postman Collection Link](https://orange-meadow-104008.postman.co/workspace/My-Workspace~bc342ba6-c01a-4032-87c7-b7d00cf0c543/collection/33668151-0dcff038-0c87-4669-bc59-0eab935499df?action=share&creator=33668151&active-environment=33668151-acc0649b-9770-4678-8bb8-f92631378a1c)

---

## Notes

- Ensure MongoDB and Redis are running and accessible.
- JWT secret is set via Django's `SECRET_KEY` in `settings.py`.
- File uploads are stored in the `uploads/` directory.
- Download links are managed via Redis and expire after 10 minutes.
- The project uses custom JWT logic (not SimpleJWT) for authentication.
- Celery is required for sending verification emails. Make sure the Celery worker is running for user signup and verification to work.
- The `DOMAIN` environment variable is used to generate verification links in emails.

---

**Author:** Vaibhav Bhardwaj
