# HealthConnect

A Flask-based web application for online healthcare services with SQLite database, providing doctor consultation, appointment booking, and medicine delivery.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Demo Credentials](#demo-credentials)
- [API Routes](#api-routes)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Future Enhancements](#future-enhancements)

## Overview

HealthConnect is a comprehensive healthcare web platform that connects patients with doctors online. The platform features:
- Patient and Doctor login systems with separate dashboards
- Online doctor consultation and prescription requests
- Appointment booking with doctors
- Medicine ordering with prescription upload
- Complete patient history tracking
- Doctor-patient data management

## Features

### Patient Features

#### User Authentication
- **Registration**: Create patient account with personal details
- **Login**: Secure login with session management
- **User Dashboard**: Centralized dashboard for all patient activities

#### Doctor Services
- **Browse Doctors**: View all available doctors with:
  - Specialization
  - Experience
  - Qualifications
  - Consultation fees
- **Book Appointments**: Schedule appointments with preferred doctors
- **Request Prescriptions**: Submit health problems for online prescription
- **View History**: Track all consultations, appointments, and orders

#### Medicine Ordering
- **Prescription Upload**: Upload doctor's prescription (image/PDF)
- **Delivery Details**: Multiple address support
- **Order Tracking**: View order status and history

### Doctor Features

#### Doctor Authentication
- **Doctor Login**: Separate login portal for doctors
- **Doctor Dashboard**: Professional dashboard for patient management

#### Patient Management
- **View Consultations**: Access all patient consultation requests with:
  - Patient demographics (name, age, gender, location)
  - Problem description
  - Service type (prescription/appointment)
  - Status tracking (pending/in-progress/completed)
- **Update Consultations**:
  - Change consultation status
  - Provide prescriptions
  - Add doctor's notes
- **Appointment Management**: View all scheduled appointments with patient details

#### Data Access
- **Patient Information**: Complete patient contact and health details
- **Consultation History**: Full access to all consultation records
- **Appointment Schedule**: View upcoming and past appointments

### Additional Features
- **Responsive Design**: Mobile-friendly interface
- **Flash Notifications**: Real-time user feedback
- **File Upload Security**: Secure prescription file handling
- **Session Management**: Secure user sessions

## Project Structure

```
healthconnect/
│
├── app.py                      # Main Flask application with routes
├── database.py                 # Database models and helper functions
├── healthconnect.db            # SQLite database (auto-generated)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── venv/                       # Virtual environment (auto-generated)
├── uploads/                    # Uploaded prescription files (auto-generated)
│
├── static/                     # Static assets
│   ├── css/                    # Stylesheets
│   │   ├── home.css
│   │   ├── doctor.css
│   │   ├── order.css
│   │   ├── contact.css
│   │   └── login.css
│   └── js/                     # JavaScript files
│       ├── home.js
│       ├── doctor.js
│       ├── order.js
│       └── script.js
│
└── templates/                  # HTML templates
    ├── home.html               # Landing page
    ├── login.html              # Patient login page
    ├── register.html           # Patient registration page
    ├── doctor_login.html       # Doctor login page
    ├── user_dashboard.html     # Patient dashboard
    ├── doctor_dashboard.html   # Doctor dashboard
    ├── book_appointment.html   # Appointment booking form
    ├── request_prescription.html # Prescription request form
    ├── doctor.html             # Doctor consultation page
    ├── order.html              # Medicine ordering page
    ├── about.html              # About page
    └── contact.html            # Contact page
```

## Technologies Used

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLite3 (Lightweight relational database)
- **Templating**: Jinja2 (Flask templating engine)
- **Session Management**: Flask sessions with secret key
- **File Upload**: Werkzeug 3.0.1
- **Frontend**: HTML5, CSS3, JavaScript

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory**
   ```bash
   cd D:\genAI\healthconnect
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database**
   ```bash
   python database.py
   ```

   This will create:
   - SQLite database (`healthconnect.db`)
   - All required tables
   - Sample doctor accounts

## Running the Application

### Start the Flask Server

```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Run the application
python app.py
```

The application will start on: `http://127.0.0.1:5000/`

### Stopping the Application

Press `Ctrl + C` in the terminal.

## Usage Guide

### For Patients

1. **Register an Account**
   - Go to `/register`
   - Enter username, password, and optional details (email, phone, full name)
   - Click "Register"

2. **Login**
   - Go to `/login`
   - Enter your credentials
   - Redirected to User Dashboard

3. **Browse Doctors**
   - View all available doctors on dashboard
   - See specialization, experience, fees, and qualifications

4. **Book an Appointment**
   - Click "Book Appointment" on any doctor card
   - Select date and time
   - Describe reason for appointment
   - Submit booking

5. **Request a Prescription**
   - Click "Get Prescription" on any doctor card
   - Fill in age, gender, location
   - Describe your health problem
   - Submit request

6. **Order Medicine**
   - Go to `/order`
   - Upload prescription file
   - Enter delivery details
   - Place order

7. **View History**
   - Dashboard tabs show:
     - All consultations with status
     - Upcoming/past appointments
     - Medicine orders

### For Doctors

1. **Login**
   - Go to `/doctor-login`
   - Enter doctor credentials
   - Redirected to Doctor Dashboard

2. **View Patient Consultations**
   - See all consultation requests
   - View patient details and problems
   - Filter by status

3. **Update Consultations**
   - Click "Update" on any consultation
   - Change status (pending/in-progress/completed)
   - Add prescription details
   - Add doctor's notes
   - Submit update

4. **Manage Appointments**
   - View all scheduled appointments
   - See patient contact information
   - Check appointment dates and times

## Demo Credentials

### Patient Account
Create a new account at `/register` or use:
- **Username**: test_patient
- **Password**: password123

### Doctor Accounts
Five sample doctors are pre-loaded:

1. **Dr. Ravi Kumar** (General Physician)
   - Username: `dr_ravi`
   - Password: `doctor123`

2. **Dr. Meera Sharma** (Pediatrician)
   - Username: `dr_meera`
   - Password: `doctor123`

3. **Dr. Arjun Reddy** (Cardiologist)
   - Username: `dr_arjun`
   - Password: `doctor123`

4. **Dr. Priya Nair** (Dermatologist)
   - Username: `dr_priya`
   - Password: `doctor123`

5. **Dr. Rahul Singh** (Orthopedic)
   - Username: `dr_rahul`
   - Password: `doctor123`

### Admin Access
- **Username**: `admin`
- **Password**: `1234`

## API Routes

### Public Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` or `/home` | Home page |
| GET, POST | `/login` | Patient login |
| GET, POST | `/register` | Patient registration |
| GET, POST | `/doctor-login` | Doctor login |
| GET, POST | `/doctor` | Doctor consultation (old) |
| GET, POST | `/order` | Medicine ordering |
| GET | `/about` | About page |
| GET, POST | `/contact` | Contact form |

### Protected Patient Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/user-dashboard` | Patient dashboard |
| GET, POST | `/book-appointment/<doctor_id>` | Book appointment |
| GET, POST | `/request-prescription/<doctor_id>` | Request prescription |

### Protected Doctor Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/doctor-dashboard` | Doctor dashboard |
| POST | `/update-consultation/<consultation_id>` | Update consultation |

### Common Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/logout` | Logout (all users) |

## Database Schema

### Tables

1. **users** - Patient accounts
   - id, username, password, email, phone, full_name, age, gender, created_at

2. **doctors** - Doctor accounts
   - id, username, password, full_name, specialization, email, phone, experience_years, qualification, consultation_fee, available, created_at

3. **consultations** - Consultation requests
   - id, user_id, doctor_id, fullname, age, gender, city, service_type, problem, status, prescription, notes, created_at

4. **appointments** - Scheduled appointments
   - id, user_id, doctor_id, appointment_date, appointment_time, reason, status, notes, created_at

5. **medicine_orders** - Medicine orders
   - id, user_id, fullname, phone, zipcode, town, landmark, prescription_file, status, created_at

6. **contact_messages** - Contact form submissions
   - id, name, email, message, status, created_at

### Database Helper Functions

Located in `database.py`:
- `init_db()` - Initialize database and tables
- `create_user()` - Create new patient
- `get_user_by_username()` - Retrieve patient
- `get_doctor_by_username()` - Retrieve doctor
- `get_all_doctors()` - List all doctors
- `create_consultation()` - Create consultation
- `create_appointment()` - Create appointment
- `create_medicine_order()` - Create order
- `update_consultation()` - Update consultation status/prescription
- And more...

## Configuration

### App Configuration (app.py)

```python
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
```

### Security Recommendations

For production deployment:

1. **Change Secret Key**
   ```python
   import secrets
   app.secret_key = secrets.token_hex(32)
   ```

2. **Hash Passwords**
   - Install: `pip install bcrypt`
   - Use bcrypt to hash passwords before storing

3. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-key
   export DATABASE_URL=sqlite:///healthconnect.db
   ```

4. **HTTPS**
   - Use SSL certificates in production
   - Enforce HTTPS for all routes

5. **Input Validation**
   - Validate all form inputs
   - Sanitize user data
   - Use Flask-WTF for CSRF protection

6. **File Upload Security**
   - Validate file types
   - Scan for malware
   - Limit file sizes

## Future Enhancements

### High Priority
- [ ] Password hashing with bcrypt
- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Video consultation integration
- [ ] Payment gateway for consultation fees
- [ ] SMS notifications for appointments
- [ ] Email notifications for prescriptions

### Medium Priority
- [ ] Admin dashboard for system management
- [ ] Doctor availability calendar
- [ ] Real-time chat between patients and doctors
- [ ] Prescription image preview
- [ ] Medicine catalog and search
- [ ] Rating and review system for doctors
- [ ] Appointment reminders
- [ ] Medical records upload

### Low Priority
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Integration with pharmacy APIs
- [ ] Health insurance claims
- [ ] Telemedicine prescriptions
- [ ] AI-powered symptom checker
- [ ] Patient health analytics

## Testing

To test the application:

1. **Initialize database with sample data**
   ```bash
   python database.py
   ```

2. **Test patient flow**
   - Register a new patient
   - Login and view dashboard
   - Browse doctors
   - Book an appointment
   - Request a prescription

3. **Test doctor flow**
   - Login as a doctor (use demo credentials)
   - View patient consultations
   - Update consultation with prescription
   - View appointments

4. **Test medicine ordering**
   - Login as patient
   - Upload prescription
   - Enter delivery details
   - Submit order

## Troubleshooting

### Common Issues

1. **Database not found**
   - Run `python database.py` to initialize

2. **Module not found error**
   - Activate virtual environment
   - Run `pip install -r requirements.txt`

3. **Port already in use**
   - Change port: `app.run(debug=True, port=5001)`

4. **File upload fails**
   - Check `uploads/` folder exists
   - Verify file size < 16MB

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

## Support

For support or queries:
- Email: support@healthconnect.com
- Open an issue in the repository

---

**Built with Flask and SQLite**

**Last Updated**: October 2025
