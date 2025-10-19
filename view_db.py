import sqlite3
from datetime import datetime

def view_database():
    """View all data in the HealthConnect database"""
    conn = sqlite3.connect('healthconnect.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 80)
    print("HEALTHCONNECT DATABASE VIEWER")
    print("=" * 80)

    # View Users (Patients)
    print("\n\n[PATIENTS (USERS)]")
    print("-" * 80)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"ID: {user['id']} | Username: {user['username']} | Name: {user['full_name']} | Email: {user['email']}")
    else:
        print("No patients registered yet.")

    # View Doctors
    print("\n\n[DOCTORS]")
    print("-" * 80)
    cursor.execute('SELECT * FROM doctors')
    doctors = cursor.fetchall()
    if doctors:
        for doctor in doctors:
            print(f"ID: {doctor['id']} | Username: {doctor['username']} | Name: {doctor['full_name']}")
            print(f"   Specialization: {doctor['specialization']} | Experience: {doctor['experience_years']} years")
            print(f"   Fee: Rs.{doctor['consultation_fee']} | Available: {'Yes' if doctor['available'] else 'No'}")
            print()
    else:
        print("No doctors found.")

    # View Consultations
    print("\n\n[CONSULTATIONS]")
    print("-" * 80)
    cursor.execute('''
        SELECT c.*, d.full_name as doctor_name, u.username as patient_username
        FROM consultations c
        LEFT JOIN doctors d ON c.doctor_id = d.id
        LEFT JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
    ''')
    consultations = cursor.fetchall()
    if consultations:
        for consult in consultations:
            print(f"Consultation ID: {consult['id']} | Status: {consult['status']}")
            print(f"   Patient: {consult['fullname']} ({consult['patient_username']}) | Age: {consult['age']} | Gender: {consult['gender']}")
            print(f"   Doctor: {consult['doctor_name']}")
            print(f"   Problem: {consult['problem'][:100]}...")
            print(f"   Service: {consult['service_type']} | Date: {consult['created_at'][:10]}")
            if consult['prescription']:
                print(f"   Prescription: {consult['prescription'][:100]}...")
            print()
    else:
        print("No consultations yet.")

    # View Appointments
    print("\n\n[APPOINTMENTS]")
    print("-" * 80)
    cursor.execute('''
        SELECT a.*, d.full_name as doctor_name, u.username as patient_username, u.full_name as patient_name
        FROM appointments a
        LEFT JOIN doctors d ON a.doctor_id = d.id
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.appointment_date DESC
    ''')
    appointments = cursor.fetchall()
    if appointments:
        for appt in appointments:
            print(f"Appointment ID: {appt['id']} | Status: {appt['status']}")
            print(f"   Patient: {appt['patient_name'] or appt['patient_username']}")
            print(f"   Doctor: {appt['doctor_name']}")
            print(f"   Date: {appt['appointment_date']} at {appt['appointment_time']}")
            print(f"   Reason: {appt['reason']}")
            print()
    else:
        print("No appointments scheduled.")

    # View Medicine Orders
    print("\n\n[MEDICINE ORDERS]")
    print("-" * 80)
    cursor.execute('''
        SELECT m.*, u.username as patient_username
        FROM medicine_orders m
        LEFT JOIN users u ON m.user_id = u.id
        ORDER BY m.created_at DESC
    ''')
    orders = cursor.fetchall()
    if orders:
        for order in orders:
            print(f"Order ID: {order['id']} | Status: {order['status']}")
            print(f"   Patient: {order['fullname']} ({order['patient_username']})")
            print(f"   Phone: {order['phone']}")
            print(f"   Address: {order['town']}, {order['landmark']}, {order['zipcode']}")
            print(f"   Prescription File: {order['prescription_file']}")
            print(f"   Date: {order['created_at'][:10]}")
            print()
    else:
        print("No medicine orders yet.")

    # View Contact Messages
    print("\n\n[CONTACT MESSAGES]")
    print("-" * 80)
    cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
    messages = cursor.fetchall()
    if messages:
        for msg in messages:
            print(f"Message ID: {msg['id']} | Status: {msg['status']}")
            print(f"   From: {msg['name']} ({msg['email']})")
            print(f"   Message: {msg['message'][:100]}...")
            print(f"   Date: {msg['created_at'][:10]}")
            print()
    else:
        print("No contact messages yet.")

    # Statistics
    print("\n\n[DATABASE STATISTICS]")
    print("-" * 80)
    cursor.execute('SELECT COUNT(*) as count FROM users')
    print(f"Total Patients: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM doctors')
    print(f"Total Doctors: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM consultations')
    print(f"Total Consultations: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM appointments')
    print(f"Total Appointments: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM medicine_orders')
    print(f"Total Medicine Orders: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM contact_messages')
    print(f"Total Contact Messages: {cursor.fetchone()['count']}")

    print("\n" + "=" * 80)
    conn.close()

if __name__ == '__main__':
    view_database()
