import sqlite3
from datetime import datetime
import os

DATABASE = 'healthconnect.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table (for patients)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            full_name TEXT,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            experience_years INTEGER,
            qualification TEXT,
            consultation_fee REAL,
            available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Consultations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_id INTEGER,
            fullname TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            city TEXT NOT NULL,
            service_type TEXT NOT NULL,
            problem TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            prescription TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')

    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')

    # Medicine orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicine_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            fullname TEXT NOT NULL,
            phone TEXT NOT NULL,
            zipcode TEXT NOT NULL,
            town TEXT NOT NULL,
            landmark TEXT NOT NULL,
            prescription_file TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Contact messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Insert sample doctors if none exist
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        sample_doctors = [
            ('dr_ravi', 'doctor123', 'Dr. Ravi Kumar', 'General Physician', 'ravi.kumar@healthconnect.com', '+91 98765 43210', 10, 'MBBS, MD', 500.0),
            ('dr_meera', 'doctor123', 'Dr. Meera Sharma', 'Pediatrician', 'meera.sharma@healthconnect.com', '+91 98765 43211', 8, 'MBBS, DCH', 600.0),
            ('dr_arjun', 'doctor123', 'Dr. Arjun Reddy', 'Cardiologist', 'arjun.reddy@healthconnect.com', '+91 98765 43212', 15, 'MBBS, DM (Cardiology)', 800.0),
            ('dr_priya', 'doctor123', 'Dr. Priya Nair', 'Dermatologist', 'priya.nair@healthconnect.com', '+91 98765 43213', 7, 'MBBS, MD (Dermatology)', 550.0),
            ('dr_rahul', 'doctor123', 'Dr. Rahul Singh', 'Orthopedic', 'rahul.singh@healthconnect.com', '+91 98765 43214', 12, 'MBBS, MS (Ortho)', 700.0),
        ]

        cursor.executemany('''
            INSERT INTO doctors (username, password, full_name, specialization, email, phone, experience_years, qualification, consultation_fee)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_doctors)
        conn.commit()

    conn.close()
    print("Database initialized successfully!")

# Database helper functions

def create_user(username, password, email=None, phone=None, full_name=None, age=None, gender=None):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, phone, full_name, age, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, email, phone, full_name, age, gender))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_doctor_by_username(username):
    """Get doctor by username"""
    conn = get_db_connection()
    doctor = conn.execute('SELECT * FROM doctors WHERE username = ?', (username,)).fetchone()
    conn.close()
    return doctor

def get_all_doctors():
    """Get all available doctors"""
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors WHERE available = 1 ORDER BY full_name').fetchall()
    conn.close()
    return doctors

def get_doctor_by_id(doctor_id):
    """Get doctor by ID"""
    conn = get_db_connection()
    doctor = conn.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,)).fetchone()
    conn.close()
    return doctor

def create_consultation(user_id, doctor_id, fullname, age, gender, city, service_type, problem):
    """Create a new consultation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consultations (user_id, doctor_id, fullname, age, gender, city, service_type, problem)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, doctor_id, fullname, age, gender, city, service_type, problem))
    conn.commit()
    consultation_id = cursor.lastrowid
    conn.close()
    return consultation_id

def get_doctor_consultations(doctor_id):
    """Get all consultations for a specific doctor"""
    conn = get_db_connection()
    consultations = conn.execute('''
        SELECT c.*, u.username, u.email, u.phone
        FROM consultations c
        LEFT JOIN users u ON c.user_id = u.id
        WHERE c.doctor_id = ?
        ORDER BY c.created_at DESC
    ''', (doctor_id,)).fetchall()
    conn.close()
    return consultations

def get_user_consultations(user_id):
    """Get all consultations for a specific user"""
    conn = get_db_connection()
    consultations = conn.execute('''
        SELECT c.*, d.full_name as doctor_name, d.specialization
        FROM consultations c
        LEFT JOIN doctors d ON c.doctor_id = d.id
        WHERE c.user_id = ?
        ORDER BY c.created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return consultations

def update_consultation(consultation_id, status=None, prescription=None, notes=None):
    """Update consultation details"""
    conn = get_db_connection()
    cursor = conn.cursor()

    updates = []
    params = []

    if status:
        updates.append('status = ?')
        params.append(status)
    if prescription:
        updates.append('prescription = ?')
        params.append(prescription)
    if notes:
        updates.append('notes = ?')
        params.append(notes)

    if updates:
        params.append(consultation_id)
        query = f"UPDATE consultations SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()

    conn.close()

def create_appointment(user_id, doctor_id, appointment_date, appointment_time, reason):
    """Create a new appointment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (user_id, doctor_id, appointment_date, appointment_time, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, doctor_id, appointment_date, appointment_time, reason))
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()
    return appointment_id

def get_doctor_appointments(doctor_id):
    """Get all appointments for a specific doctor"""
    conn = get_db_connection()
    appointments = conn.execute('''
        SELECT a.*, u.username, u.full_name as patient_name, u.email, u.phone
        FROM appointments a
        LEFT JOIN users u ON a.user_id = u.id
        WHERE a.doctor_id = ?
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    ''', (doctor_id,)).fetchall()
    conn.close()
    return appointments

def get_user_appointments(user_id):
    """Get all appointments for a specific user"""
    conn = get_db_connection()
    appointments = conn.execute('''
        SELECT a.*, d.full_name as doctor_name, d.specialization, d.consultation_fee
        FROM appointments a
        LEFT JOIN doctors d ON a.doctor_id = d.id
        WHERE a.user_id = ?
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return appointments

def create_medicine_order(user_id, fullname, phone, zipcode, town, landmark, prescription_file):
    """Create a new medicine order"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicine_orders (user_id, fullname, phone, zipcode, town, landmark, prescription_file)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, fullname, phone, zipcode, town, landmark, prescription_file))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return order_id

def get_user_orders(user_id):
    """Get all medicine orders for a specific user"""
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT * FROM medicine_orders
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return orders

def create_contact_message(name, email, message):
    """Create a new contact message"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contact_messages (name, email, message)
        VALUES (?, ?, ?)
    ''', (name, email, message))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id

if __name__ == '__main__':
    init_db()
