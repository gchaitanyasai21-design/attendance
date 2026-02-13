# College Attendance App

Simple Flask app for student attendance tracking.

## Features
- Student login with `roll_no` and password (default password for new students is roll number)
- Student dashboard shows:
  - Total classes
  - Attended classes
  - Attendance percentage
  - Current shortage to reach 75%
  - Classes needed continuously to recover to 75%
- Password features:
  - Forgot password using OTP
  - OTP verification and reset password
  - Change password after login
- Admin page to:
  - Add students
  - Add attendance records

## Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start app:
   ```bash
   python app.py
   ```
3. Open:
   - `http://127.0.0.1:5000/login`
   - `http://127.0.0.1:5000/admin`
   - `http://127.0.0.1:5000/forgot-password`

## Demo Login
- Roll No: `25H71A05Z2`
- Password: `25H71A05Z2`

> Database file (`attendance.db`) is created automatically on first run.

## Email OTP Setup (optional)
Set environment variables before running app:

- `SMTP_HOST` (example: `smtp.gmail.com`)
- `SMTP_PORT` (example: `587`)
- `SMTP_USER` (sender email)
- `SMTP_PASSWORD` (app password)
- `SMTP_USE_TLS` (`1` or `0`)
- `MAIL_FROM` (optional, defaults to `SMTP_USER`)

If SMTP is not configured, the app shows a dev OTP message for testing.