# HealthConnect - Login Credentials

This document contains all login credentials for testing the HealthConnect application.

---

## 🏥 DOCTOR ACCOUNTS

**Common Password for all doctors:** `doctor123`

| Username | Full Name | Specialization | Experience | Consultation Fee |
|----------|-----------|----------------|------------|------------------|
| `dr_ravi` | Dr. Ravi Kumar | General Physician | 10 years | Rs. 500 |
| `dr_meera` | Dr. Meera Sharma | Pediatrician | 8 years | Rs. 600 |
| `dr_arjun` | Dr. Arjun Reddy | Cardiologist | 15 years | Rs. 800 |
| `dr_priya` | Dr. Priya Nair | Dermatologist | 7 years | Rs. 550 |
| `dr_rahul` | Dr. Rahul Singh | Orthopedic | 12 years | Rs. 700 |

**Login URL:** `http://localhost:5000/doctor-login`

**Doctor Dashboard Features:**
- View all patient consultations
- Update consultations with prescriptions
- Add doctor's notes
- View scheduled appointments
- Access patient contact information

---

## 👤 PATIENT ACCOUNTS

**Common Password for all patients:** `patient123`

| Username | Full Name | Age | Gender | Email | Phone |
|----------|-----------|-----|--------|-------|-------|
| `john_doe` | John Doe | 28 | Male | john.doe@email.com | +91 98765 11111 |
| `sarah_smith` | Sarah Smith | 35 | Female | sarah.smith@email.com | +91 98765 22222 |
| `raj_kumar` | Raj Kumar | 42 | Male | raj.kumar@email.com | +91 98765 33333 |
| `priya_patel` | Priya Patel | 29 | Female | priya.patel@email.com | +91 98765 44444 |
| `mike_jones` | Mike Jones | 51 | Male | mike.jones@email.com | +91 98765 55555 |
| `anjali_sharma` | Anjali Sharma | 33 | Female | anjali.sharma@email.com | +91 98765 66666 |
| `david_lee` | David Lee | 45 | Male | david.lee@email.com | +91 98765 77777 |
| `neha_verma` | Neha Verma | 26 | Female | neha.verma@email.com | +91 98765 88888 |
| `amit_singh` | Amit Singh | 38 | Male | amit.singh@email.com | +91 98765 99999 |
| `lisa_brown` | Lisa Brown | 31 | Female | lisa.brown@email.com | +91 98765 00000 |

**Login URL:** `http://localhost:5000/login`

**Patient Dashboard Features:**
- Browse all available doctors
- Book appointments with doctors
- Request prescriptions
- View consultation history
- View appointment schedule
- Track medicine orders

---

## 🔐 ADMIN ACCOUNT

| Username | Password | Access Level |
|----------|----------|--------------|
| `admin` | `1234` | Administrator |

**Login URL:** `http://localhost:5000/login`

---

## 📊 Pre-loaded Data Summary

The database has been populated with realistic sample data:

### Consultations
- **10 consultations** created across different patients and doctors
- **8 consultations** have prescriptions and doctor's notes
- **2 consultations** are pending (awaiting doctor review)
- Mix of "Prescription" and "Appointment" service types

### Appointments
- **10 appointments** scheduled
- Mix of past and future appointments
- Different times and dates for testing

### Medicine Orders
- **8 medicine orders** placed
- Include delivery addresses across major Indian cities
- Sample prescription files attached

### Contact Messages
- **5 contact messages** from potential patients
- Various queries about services

---

## 🧪 Testing Scenarios

### Test as Patient (e.g., `john_doe` / `patient123`)

1. **Login:** `http://localhost:5000/login`
2. **Dashboard:** View your consultations, appointments, and orders
3. **Book Appointment:**
   - Click "Book Appointment" on any doctor card
   - Select date and time
   - Submit
4. **Request Prescription:**
   - Click "Get Prescription" on any doctor
   - Fill in your health problem
   - Submit
5. **Order Medicine:**
   - Go to "Order Medicine" from home page
   - Upload prescription
   - Enter delivery address

### Test as Doctor (e.g., `dr_ravi` / `doctor123`)

1. **Login:** `http://localhost:5000/doctor-login`
2. **Dashboard:** View patient consultations and appointments
3. **Update Consultation:**
   - Click "Update" on any pending consultation
   - Change status to "in-progress" or "completed"
   - Add prescription details
   - Add doctor's notes
   - Submit
4. **View Appointments:** Check scheduled appointments with patient details

---

## 🔄 Sample Data Details

### Example Patient with Full History: `john_doe`

**Personal Info:**
- Age: 28, Male
- Email: john.doe@email.com
- Phone: +91 98765 11111

**Medical History:**
- 1 Consultation (Completed)
  - Problem: Persistent headaches
  - Doctor: Dr. Arjun Reddy (Cardiologist)
  - Prescription: Paracetamol 500mg
- 1 Appointment (Upcoming)
  - Date: 2025-11-02 at 16:00
  - Doctor: Dr. Arjun Reddy
  - Reason: Regular health checkup
- 1 Medicine Order
  - Delivery: Mumbai, Near Central Mall
  - Prescription: prescription_1.pdf

### Example Doctor with Patients: `dr_ravi`

**Patients Assigned:**
- Mike Jones (Chronic knee pain - Completed)
- Lisa Brown (Allergic reactions - Pending)

**Specialization:** General Physician
**Experience:** 10 years
**Fee:** Rs. 500

---

## 📝 Quick Start Guide

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open browser:** `http://localhost:5000`

3. **Test patient login:**
   - Username: `john_doe`
   - Password: `patient123`

4. **Test doctor login:**
   - Username: `dr_ravi`
   - Password: `doctor123`

5. **View database:**
   ```bash
   python view_db.py
   ```

---

## 🔧 Add More Sample Data

To add more sample data or reset:

```bash
# Add sample data (can be run multiple times)
python add_sample_data.py

# Reset database completely
del healthconnect.db
python database.py
python add_sample_data.py
```

---

## ⚠️ Security Note

**Important:** These are **DEMO credentials** for development/testing only!

For production:
- Change all passwords
- Implement password hashing (bcrypt)
- Use strong, unique passwords
- Enable HTTPS
- Add two-factor authentication
- Remove or disable demo accounts

---

## 📞 Support

If credentials don't work:
1. Check if database exists: `dir healthconnect.db`
2. Reinitialize database: `python database.py`
3. Add sample data: `python add_sample_data.py`
4. View database: `python view_db.py`

---

**Last Updated:** October 2025

**Database Location:** `healthconnect.db`
**Total Users:** 10 Patients + 5 Doctors + 1 Admin
