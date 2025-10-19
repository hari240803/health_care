from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
from functools import wraps
import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize database
db.init_db()

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for doctor login required
def doctor_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            flash('Please login as a doctor to access this page.', 'error')
            return redirect(url_for('doctor_login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Doctor consultation page (old version - simplified)
@app.route('/doctor', methods=['GET', 'POST'])
@login_required
def doctor():
    doctors = db.get_all_doctors()

    if request.method == 'POST':
        # Get logged in user id
        user_id = session.get('user_id')

        # Get form data
        fullname = request.form.get('fullname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        city = request.form.get('city')
        doctor_name = request.form.get('doctor')
        service = request.form.get('service')
        problem = request.form.get('problem')

        # Find doctor ID by name
        doctor_id = None
        for doc in doctors:
            if doc['full_name'] in doctor_name:
                doctor_id = doc['id']
                break

        # Create consultation
        consultation_id = db.create_consultation(
            user_id, doctor_id, fullname, age, gender, city, service, problem
        )

        flash('Consultation request submitted successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('doctor.html', doctors=doctors)

# Order Medicine page
@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    if request.method == 'POST':
        user_id = session.get('user_id')

        # Handle file upload
        prescription_file = request.files.get('prescription')
        filename = None

        if prescription_file and prescription_file.filename:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prescription_file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            prescription_file.save(filepath)

        # Get form data
        fullname = request.form.get('fullname')
        phone = request.form.get('phone')
        zipcode = request.form.get('zipcode')
        town = request.form.get('town')
        landmark = request.form.get('landmark')

        # Create order
        db.create_medicine_order(user_id, fullname, phone, zipcode, town, landmark, filename)

        flash('Order placed successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('order.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        db.create_contact_message(name, email, message)

        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# User Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check against database users
        user = db.get_user_by_username(username)

        if user and user['password'] == password:
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_type'] = 'patient'
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('user_dashboard'))
        elif username == 'admin' and password == '1234':
            session['logged_in'] = True
            session['username'] = username
            session['user_type'] = 'admin'
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
            return render_template('login.html')

    return render_template('login.html')

# User Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Check if user already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            flash('Username already exists! Please choose a different one.', 'error')
            return render_template('register.html')

        # Create new user with all fields
        user_id = db.create_user(username, password, email, phone, full_name, age, gender)

        if user_id:
            flash('Registration successful! Please login with your credentials.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed! Please try again.', 'error')

    return render_template('register.html')

# Doctor Register page
@app.route('/doctor-register', methods=['GET', 'POST'])
def doctor_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        specialization = request.form.get('specialization')
        qualification = request.form.get('qualification', '')
        experience_years_str = request.form.get('experience_years', '0')
        consultation_fee_str = request.form.get('consultation_fee', '500')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Validate and convert numeric fields with defaults
        try:
            experience_years = int(experience_years_str) if experience_years_str else 0
            consultation_fee = float(consultation_fee_str) if consultation_fee_str else 500.0
        except (ValueError, TypeError):
            flash('Invalid experience years or consultation fee. Please enter valid numbers.', 'error')
            return render_template('doctor_register.html')

        # Check if doctor already exists
        existing_doctor = db.get_doctor_by_username(username)
        if existing_doctor:
            flash('Username already exists! Please choose a different one.', 'error')
            return render_template('doctor_register.html')

        # Create new doctor
        doctor_id = db.create_doctor(
            username, password, full_name, specialization,
            email, phone, experience_years, qualification, consultation_fee
        )

        if doctor_id:
            flash('Doctor registration successful! Please login with your credentials.', 'success')
            return redirect(url_for('doctor_login'))
        else:
            flash('Registration failed! Please try again.', 'error')

    return render_template('doctor_register.html')

# Doctor Login page
@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check against database doctors
        doctor = db.get_doctor_by_username(username)

        if doctor and doctor['password'] == password:
            session['logged_in'] = True
            session['doctor_id'] = doctor['id']
            session['username'] = doctor['username']
            session['doctor_name'] = doctor['full_name']
            session['user_type'] = 'doctor'
            flash(f'Welcome Dr. {doctor["full_name"]}!', 'success')
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
            return render_template('doctor_login.html')

    return render_template('doctor_login.html')

# Doctor Dashboard
@app.route('/doctor-dashboard')
@doctor_login_required
def doctor_dashboard():
    doctor_id = session.get('doctor_id')

    # Get doctor's consultations
    consultations = db.get_doctor_consultations(doctor_id)

    # Get doctor's appointments
    appointments = db.get_doctor_appointments(doctor_id)

    return render_template('doctor_dashboard.html',
                         consultations=consultations,
                         appointments=appointments,
                         doctor_name=session.get('doctor_name'))

# Update consultation (for doctors)
@app.route('/update-consultation/<int:consultation_id>', methods=['POST'])
@doctor_login_required
def update_consultation(consultation_id):
    status = request.form.get('status')
    prescription = request.form.get('prescription')
    notes = request.form.get('notes')

    db.update_consultation(consultation_id, status, prescription, notes)

    flash('Consultation updated successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))

# User Dashboard
@app.route('/user-dashboard')
@login_required
def user_dashboard():
    user_id = session.get('user_id')

    # Get all doctors
    doctors = db.get_all_doctors()

    # Get user's consultations
    consultations = db.get_user_consultations(user_id)

    # Get user's appointments
    appointments = db.get_user_appointments(user_id)

    # Get user's orders
    orders = db.get_user_orders(user_id)

    return render_template('user_dashboard.html',
                         doctors=doctors,
                         consultations=consultations,
                         appointments=appointments,
                         orders=orders,
                         username=session.get('username'))

# Book Appointment
@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    doctor = db.get_doctor_by_id(doctor_id)

    if request.method == 'POST':
        user_id = session.get('user_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason')

        appointment_id = db.create_appointment(user_id, doctor_id, appointment_date, appointment_time, reason)

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('book_appointment.html', doctor=doctor)

# Request Prescription
@app.route('/request-prescription/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def request_prescription(doctor_id):
    doctor = db.get_doctor_by_id(doctor_id)
    user_id = session.get('user_id')
    user = db.get_user_by_username(session.get('username'))

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        city = request.form.get('city')
        problem = request.form.get('problem')

        fullname = user['full_name'] if user['full_name'] else session.get('username')

        consultation_id = db.create_consultation(
            user_id, doctor_id, fullname, age, gender, city, 'Prescription', problem
        )

        flash('Prescription request submitted successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('request_prescription.html', doctor=doctor, user=user)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
