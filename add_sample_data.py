import database as db
from datetime import datetime, timedelta
import random

def add_sample_data():
    """Add sample patients, consultations, appointments, and orders for testing"""

    print("=" * 80)
    print("ADDING SAMPLE DATA TO HEALTHCONNECT DATABASE")
    print("=" * 80)

    # Sample Patients
    sample_patients = [
        ('john_doe', 'patient123', 'john.doe@email.com', '+91 98765 11111', 'John Doe', 28, 'Male'),
        ('sarah_smith', 'patient123', 'sarah.smith@email.com', '+91 98765 22222', 'Sarah Smith', 35, 'Female'),
        ('raj_kumar', 'patient123', 'raj.kumar@email.com', '+91 98765 33333', 'Raj Kumar', 42, 'Male'),
        ('priya_patel', 'patient123', 'priya.patel@email.com', '+91 98765 44444', 'Priya Patel', 29, 'Female'),
        ('mike_jones', 'patient123', 'mike.jones@email.com', '+91 98765 55555', 'Mike Jones', 51, 'Male'),
        ('anjali_sharma', 'patient123', 'anjali.sharma@email.com', '+91 98765 66666', 'Anjali Sharma', 33, 'Female'),
        ('david_lee', 'patient123', 'david.lee@email.com', '+91 98765 77777', 'David Lee', 45, 'Male'),
        ('neha_verma', 'patient123', 'neha.verma@email.com', '+91 98765 88888', 'Neha Verma', 26, 'Female'),
        ('amit_singh', 'patient123', 'amit.singh@email.com', '+91 98765 99999', 'Amit Singh', 38, 'Male'),
        ('lisa_brown', 'patient123', 'lisa.brown@email.com', '+91 98765 00000', 'Lisa Brown', 31, 'Female'),
    ]

    print("\n[1/5] Creating Sample Patients...")
    print("-" * 80)

    patient_ids = []
    for username, password, email, phone, full_name, age, gender in sample_patients:
        # Check if user already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            print(f"   [OK] Patient already exists: {username}")
            patient_ids.append(existing_user['id'])
        else:
            user_id = db.create_user(username, password, email, phone, full_name, age, gender)
            if user_id:
                patient_ids.append(user_id)
                print(f"   [OK] Created patient: {username} | {full_name}")

    print(f"\n   Total Patients: {len(patient_ids)}")

    # Get all doctors
    doctors = db.get_all_doctors()
    doctor_ids = [doc['id'] for doc in doctors]

    # Sample Consultations
    print("\n[2/5] Creating Sample Consultations...")
    print("-" * 80)

    consultation_problems = [
        "Experiencing persistent headaches for the past week. Pain is moderate and occurs mostly in the morning.",
        "Having fever (101°F) and body aches for 3 days. Also feeling very weak and tired.",
        "Skin rash appeared on arms and legs. It's itchy and red. Started 2 days ago.",
        "Chest pain and difficulty breathing during physical activity. Need immediate consultation.",
        "Chronic knee pain that gets worse when climbing stairs. Pain level 6/10.",
        "Digestive issues - bloating and stomach pain after meals for the past month.",
        "High blood pressure readings (150/95). Need prescription renewal.",
        "Anxiety and sleep problems. Difficulty falling asleep at night.",
        "Back pain in lower back region. Pain radiates to left leg.",
        "Allergic reactions - sneezing, runny nose, and watery eyes since yesterday.",
        "Child has fever and cough for 2 days. Temperature 100.5°F.",
        "Need prescription for diabetes medication refill.",
        "Joint pain in hands and wrists. Stiffness in the morning.",
        "Migraine episodes 3-4 times per week. Need stronger medication.",
        "Persistent cough with phlegm for 10 days. No fever.",
    ]

    consultation_count = 0
    for i in range(min(15, len(patient_ids))):
        user_id = patient_ids[i % len(patient_ids)]
        doctor_id = doctor_ids[i % len(doctor_ids)]

        user = db.get_user_by_username(sample_patients[i % len(sample_patients)][0])

        problem = consultation_problems[i % len(consultation_problems)]
        service_type = random.choice(['Prescription', 'Appointment', 'Prescription'])

        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata']
        city = random.choice(cities)

        # Create consultation
        consult_id = db.create_consultation(
            user_id, doctor_id,
            user['full_name'], user['age'], user['gender'],
            city, service_type, problem
        )

        # Randomly update some consultations with prescriptions
        if i < 8:  # First 8 consultations have prescriptions
            status = random.choice(['completed', 'in-progress'])
            prescriptions = [
                "Tab. Paracetamol 500mg - 1 tablet twice daily for 5 days. Rest and drink plenty of fluids.",
                "Tab. Amoxicillin 500mg - 1 tablet three times daily for 7 days. Take after meals.",
                "Skin Ointment - Apply twice daily on affected area. Avoid scratching. Continue for 10 days.",
                "Tab. Aspirin 75mg - 1 tablet once daily. Monitor blood pressure. Follow up in 2 weeks.",
                "Tab. Ibuprofen 400mg - 1 tablet when needed for pain. Don't exceed 3 tablets per day.",
                "Antacid Syrup - 2 teaspoons after meals. Avoid spicy food. Tab. Pantoprazole 40mg before breakfast.",
                "Tab. Amlodipine 5mg - 1 tablet once daily in the morning. Continue current medication.",
                "Tab. Alprazolam 0.5mg - 1 tablet at bedtime. Avoid caffeine after 4 PM.",
            ]
            notes = [
                "Patient shows good response to treatment. Continue medication as prescribed.",
                "Advised lifestyle changes including diet and exercise. Schedule follow-up in 2 weeks.",
                "Condition is improving. Complete the full course of antibiotics.",
                "Monitor symptoms closely. Return immediately if condition worsens.",
                "Physical therapy recommended along with medication.",
                "Blood tests advised. Reports to be reviewed in next consultation.",
                "Chronic condition - requires long-term management and regular monitoring.",
                "Emergency consultation completed. Stable now. Follow up required.",
            ]

            db.update_consultation(
                consult_id,
                status=status,
                prescription=prescriptions[i % len(prescriptions)],
                notes=notes[i % len(notes)]
            )

        consultation_count += 1

    print(f"   [OK] Created {consultation_count} consultations (8 with prescriptions)")

    # Sample Appointments
    print("\n[3/5] Creating Sample Appointments...")
    print("-" * 80)

    appointment_reasons = [
        "Regular health checkup and blood pressure monitoring",
        "Follow-up consultation for ongoing treatment",
        "Vaccination appointment for child",
        "Diabetes management and insulin adjustment",
        "Skin condition follow-up examination",
        "Cardiac health assessment and ECG",
        "Orthopedic consultation for knee pain",
        "Dental cleaning and checkup",
        "Eye examination and vision test",
        "Annual physical examination",
    ]

    appointment_count = 0
    base_date = datetime.now()

    for i in range(min(12, len(patient_ids))):
        user_id = patient_ids[i % len(patient_ids)]
        doctor_id = doctor_ids[i % len(doctor_ids)]

        # Mix of past and future appointments
        days_offset = random.choice([-10, -7, -3, -1, 1, 3, 5, 7, 10, 14, 21])
        appointment_date = (base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')

        times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        appointment_time = random.choice(times)

        reason = appointment_reasons[i % len(appointment_reasons)]

        appt_id = db.create_appointment(user_id, doctor_id, appointment_date, appointment_time, reason)
        appointment_count += 1

    print(f"   [OK] Created {appointment_count} appointments (past and upcoming)")

    # Sample Medicine Orders
    print("\n[4/5] Creating Sample Medicine Orders...")
    print("-" * 80)

    addresses = [
        ('Mumbai', 'Near Central Mall', '400001'),
        ('Delhi', 'Opposite Metro Station', '110001'),
        ('Bangalore', 'Behind City Hospital', '560001'),
        ('Hyderabad', 'Near Jubilee Hills', '500033'),
        ('Chennai', 'T Nagar Main Road', '600017'),
        ('Pune', 'Koregaon Park Area', '411001'),
        ('Kolkata', 'Salt Lake Sector 5', '700091'),
    ]

    order_count = 0
    for i in range(min(8, len(patient_ids))):
        user_id = patient_ids[i % len(patient_ids)]
        user = db.get_user_by_username(sample_patients[i % len(sample_patients)][0])

        town, landmark, zipcode = addresses[i % len(addresses)]

        prescription_file = f"prescription_{i+1}.pdf"

        order_id = db.create_medicine_order(
            user_id, user['full_name'], user['phone'],
            zipcode, town, landmark, prescription_file
        )
        order_count += 1

    print(f"   [OK] Created {order_count} medicine orders")

    # Sample Contact Messages
    print("\n[5/5] Creating Sample Contact Messages...")
    print("-" * 80)

    contact_messages = [
        ('Ramesh Gupta', 'ramesh.g@email.com', 'I would like to know about your home visit services. Do you provide doctors for home consultations?'),
        ('Sneha Reddy', 'sneha.reddy@email.com', 'How can I get my medical records from your system? I need them for insurance claims.'),
        ('Karthik Iyer', 'karthik.iyer@email.com', 'Is there an option for video consultation? I am currently traveling and need to consult a doctor.'),
        ('Meera Shah', 'meera.shah@email.com', 'What are your operating hours? Can I book an emergency appointment during night time?'),
        ('Vijay Kumar', 'vijay.k@email.com', 'Do you accept health insurance? Which insurance providers do you work with?'),
    ]

    message_count = 0
    for name, email, message in contact_messages:
        msg_id = db.create_contact_message(name, email, message)
        message_count += 1

    print(f"   [OK] Created {message_count} contact messages")

    # Print Summary
    print("\n" + "=" * 80)
    print("SAMPLE DATA ADDED SUCCESSFULLY!")
    print("=" * 80)

    conn = db.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_patients = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM doctors')
    total_doctors = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM consultations')
    total_consultations = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM appointments')
    total_appointments = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM medicine_orders')
    total_orders = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM contact_messages')
    total_messages = cursor.fetchone()['count']

    conn.close()

    print(f"\nDatabase Statistics:")
    print(f"  - Patients: {total_patients}")
    print(f"  - Doctors: {total_doctors}")
    print(f"  - Consultations: {total_consultations}")
    print(f"  - Appointments: {total_appointments}")
    print(f"  - Medicine Orders: {total_orders}")
    print(f"  - Contact Messages: {total_messages}")

    print("\n" + "=" * 80)
    print("LOGIN CREDENTIALS")
    print("=" * 80)

    print("\n[PATIENT ACCOUNTS] - Password: patient123")
    print("-" * 80)
    for username, _, email, phone, full_name, age, gender in sample_patients:
        print(f"Username: {username:20} | Name: {full_name:20} | Age: {age}")

    print("\n[DOCTOR ACCOUNTS] - Password: doctor123")
    print("-" * 80)
    doctors = db.get_all_doctors()
    for doc in doctors:
        print(f"Username: {doc['username']:20} | Name: {doc['full_name']:25} | Specialization: {doc['specialization']}")

    print("\n" + "=" * 80)
    print("You can now login with any of the above credentials!")
    print("=" * 80)

if __name__ == '__main__':
    add_sample_data()
