# Database Access Guide - HealthConnect

This guide explains how to access and view the SQLite database for the HealthConnect application.

## Database File Location

**File:** `healthconnect.db`
**Path:** `healthconnect\healthconnect.db`

---

## Method 1: Python Script (Fastest)

### View All Database Contents

```bash
python view_db.py
```

This will display:
- All patients (users)
- All doctors
- All consultations with patient-doctor mapping
- All appointments
- All medicine orders
- All contact messages
- Database statistics (counts)

### Sample Output:
```
[DOCTORS]
ID: 1 | Username: dr_ravi | Name: Dr. Ravi Kumar
   Specialization: General Physician | Experience: 10 years
   Fee: Rs.500.0 | Available: Yes
```

---

## Method 2: DB Browser for SQLite (GUI - Best for Editing)

### Download & Install
1. Visit: https://sqlitebrowser.org/dl/
2. Download for Windows
3. Install (free, no signup required)

### Open Database
1. Launch "DB Browser for SQLite"
2. Click **"Open Database"** button
3. Navigate to: `D:\genAI\healthconnect\healthconnect.db`
4. Select the file and click "Open"

### Features:
- **Browse Data tab**: View all tables and records
- **Execute SQL tab**: Run custom SQL queries
- **Edit data**: Double-click to edit any field
- **Export**: Export to CSV, JSON, SQL
- **Database Structure tab**: View table schemas

---

## Method 3: Python Interactive Shell

```bash
# Activate virtual environment
venv\Scripts\activate

# Open Python shell
python

# Run these commands:
>>> import sqlite3
>>> conn = sqlite3.connect('healthconnect.db')
>>> cursor = conn.cursor()

# View all doctors
>>> cursor.execute('SELECT * FROM doctors')
>>> for row in cursor.fetchall():
...     print(row)

# View all patients
>>> cursor.execute('SELECT * FROM users')
>>> for row in cursor.fetchall():
...     print(row)

# View consultations
>>> cursor.execute('SELECT * FROM consultations')
>>> for row in cursor.fetchall():
...     print(row)

# Close connection
>>> conn.close()
>>> exit()
```

---

## Method 4: SQLite Command Line (Advanced)

### Install SQLite CLI
Download from: https://www.sqlite.org/download.html

### Access Database
```bash
# Navigate to project folder
cd healthconnect

# Open database
sqlite3 healthconnect.db

# View tables
.tables

# View schema
.schema doctors

# Query data
SELECT * FROM doctors;
SELECT * FROM users;
SELECT * FROM consultations;

# Format output
.mode column
.headers on
SELECT * FROM doctors;

# Exit
.quit
```

---

## Method 5: Using Database Helper Functions

### In Python Script or Flask Shell

```python
import database as db

# Get all doctors
doctors = db.get_all_doctors()
for doctor in doctors:
    print(dict(doctor))

# Get a specific user
user = db.get_user_by_username('test_user')
if user:
    print(dict(user))

# Get doctor consultations
doctor_id = 1
consultations = db.get_doctor_consultations(doctor_id)
for consult in consultations:
    print(dict(consult))

# Get user appointments
user_id = 1
appointments = db.get_user_appointments(user_id)
for appt in appointments:
    print(dict(appt))
```

---

## Database Schema

### Tables Overview

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **users** | Patient accounts | username, password, email, phone |
| **doctors** | Doctor accounts | username, full_name, specialization, fee |
| **consultations** | Consultation requests | user_id, doctor_id, problem, status |
| **appointments** | Scheduled appointments | user_id, doctor_id, date, time |
| **medicine_orders** | Medicine orders | user_id, prescription_file, address |
| **contact_messages** | Contact form data | name, email, message |

---

## Common SQL Queries

### View All Doctors
```sql
SELECT id, full_name, specialization, experience_years, consultation_fee
FROM doctors
WHERE available = 1;
```

### View All Patients
```sql
SELECT id, username, full_name, email, phone, created_at
FROM users;
```

### View Consultations with Patient & Doctor Names
```sql
SELECT
    c.id,
    c.fullname as patient,
    d.full_name as doctor,
    c.problem,
    c.status,
    c.created_at
FROM consultations c
LEFT JOIN doctors d ON c.doctor_id = d.id
ORDER BY c.created_at DESC;
```

### View Appointments with Details
```sql
SELECT
    a.id,
    u.full_name as patient,
    d.full_name as doctor,
    a.appointment_date,
    a.appointment_time,
    a.reason,
    a.status
FROM appointments a
LEFT JOIN users u ON a.user_id = u.id
LEFT JOIN doctors d ON a.doctor_id = d.id
ORDER BY a.appointment_date DESC;
```

### Count Statistics
```sql
SELECT
    (SELECT COUNT(*) FROM users) as total_patients,
    (SELECT COUNT(*) FROM doctors) as total_doctors,
    (SELECT COUNT(*) FROM consultations) as total_consultations,
    (SELECT COUNT(*) FROM appointments) as total_appointments;
```

---

## Backup Database

### Manual Backup
```bash
# Copy the database file
copy healthconnect.db healthconnect_backup_2025-10-19.db
```

### Programmatic Backup
```python
import shutil
from datetime import datetime

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2('healthconnect.db', f'healthconnect_backup_{timestamp}.db')
print(f"Backup created: healthconnect_backup_{timestamp}.db")
```

---

## Reset Database

### Clear All Data (Keep Structure)
```python
import database as db

conn = db.get_db_connection()
cursor = conn.cursor()

# Delete all data
cursor.execute('DELETE FROM contact_messages')
cursor.execute('DELETE FROM medicine_orders')
cursor.execute('DELETE FROM appointments')
cursor.execute('DELETE FROM consultations')
cursor.execute('DELETE FROM users')
# Don't delete doctors - they're sample data

conn.commit()
conn.close()
print("Database cleared!")
```

### Completely Reinitialize
```bash
# Delete the database file
del healthconnect.db

# Recreate it
python database.py
```

---

## Troubleshooting

### Database Locked Error
**Cause:** Another process is accessing the database
**Solution:**
- Close DB Browser if open
- Stop the Flask app
- Wait a few seconds and retry

### File Not Found
**Cause:** Database not initialized
**Solution:**
```bash
python database.py
```

### Permission Denied
**Cause:** File permissions issue
**Solution:**
- Run as administrator
- Check file is not read-only

---

## Quick Reference Commands

```bash
# View database contents
python view_db.py

# Initialize/reset database
python database.py

# Access with Python
python
>>> import database as db
>>> db.get_all_doctors()

# Backup database
copy healthconnect.db backup_healthconnect.db
```

---

## Security Notes

⚠️ **Important:**
- Database passwords are stored in **plain text** (for development only)
- For production, implement password hashing (bcrypt)
- Never commit `healthconnect.db` to version control
- Add to `.gitignore`: `*.db`

---

## Need Help?

- Check if database exists: `dir healthconnect.db`
- View database size: `dir healthconnect.db`
- Test connection: `python -c "import sqlite3; conn = sqlite3.connect('healthconnect.db'); print('Connected!'); conn.close()"`

---

**Last Updated:** October 2025
