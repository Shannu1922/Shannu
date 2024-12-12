from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

# Initialize the Flask application
app = Flask(__name__)


# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Surya%402002@localhost/payroll'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1922'  # Change this to a strong secret key

# Initialize the database connection
db = SQLAlchemy(app)

# Models

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))  # 'Admin' or 'Employee'

class LeaveRequest(db.Model):
    leave_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    leave_type = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pending')
    employee = db.relationship('Employee', backref='leave_requests')

class Payroll(db.Model):
    payroll_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    basic_salary = db.Column(db.Float)
    bonuses = db.Column(db.Float)
    deductions = db.Column(db.Float)
    net_salary = db.Column(db.Float)
    employee = db.relationship('Employee', backref='payrolls')

# Routes

@app.route('/')
def home():
    return render_template('login.html')  # Redirect to login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if login is for Admin
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['user_id'] = admin.admin_id  # Set session for admin
            session['role'] = 'Admin'  # Set role for admin
            return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

        # Check if login is for Employee
        employee = Employee.query.filter_by(email=username, phone=password).first()
        if employee:
            session['user_id'] = employee.id  # Set session for employee
            session['role'] = 'Employee'  # Set role for employee
            return redirect(url_for('employee_dashboard'))  # Redirect to the employee dashboard
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template('admin_dashboard.html')

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'user_id' not in session or session['role'] != 'Employee':
        return redirect(url_for('login'))
    
    return render_template('employee_dashboard.html')

# Manage Leaves (Admin)
@app.route('/manage_leaves', methods=['GET', 'POST'])
def manage_leaves():
    if 'user_id' not in session or session['role'] != 'Admin':
        return redirect(url_for('login'))

    leave_requests = LeaveRequest.query.all()
    
    if request.method == 'POST':
        leave_id = request.form['leave_id']
        action = request.form['action']
        
        leave_request = LeaveRequest.query.get(leave_id)
        if action == 'approve':
            leave_request.status = 'Approved'
        elif action == 'reject':
            leave_request.status = 'Rejected'
        
        db.session.commit()
        flash('Leave request updated successfully!', 'success')
        return redirect(url_for('manage_leaves'))
    
    return render_template('manage_leaves.html', leave_requests=leave_requests)

# View Payroll (Employee)
@app.route('/payroll')
def payroll():
    if 'user_id' not in session or session['role'] != 'Employee':
        return redirect(url_for('login'))
    
    employee_id = session['user_id']
    payroll_data = Payroll.query.filter_by(employee_id=employee_id).all()
    
    return render_template('payroll.html', payroll_data=payroll_data)

# Manage Payroll (Admin)
@app.route('/manage_payroll', methods=['GET', 'POST'])
def manage_payroll():
    if 'user_id' not in session or session['role'] != 'Admin':
        return redirect(url_for('login'))
    
    payroll_data = Payroll.query.all()
    
    if request.method == 'POST':
        payroll_id = request.form['payroll_id']
        action = request.form['action']
        
        payroll = Payroll.query.get(payroll_id)
        
        if action == 'edit':
            # Logic for editing payroll (could add a form for updates)
            pass
        elif action == 'delete':
            db.session.delete(payroll)
            db.session.commit()
            flash('Payroll record deleted successfully!', 'success')
        
        return redirect(url_for('manage_payroll'))
    
    return render_template('manage_payroll.html', payroll_data=payroll_data)

# Leave Request (Employee)
@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request():
    if 'user_id' not in session or session['role'] != 'Employee':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        leave_request = LeaveRequest(employee_id=session['user_id'], leave_type=leave_type, 
                                     start_date=start_date, end_date=end_date)
        db.session.add(leave_request)
        db.session.commit()
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('leave_request'))
    
    return render_template('leave_request.html')

# View Employees (Admin)
@app.route('/view_employees')
def view_employees():
    if 'user_id' not in session or session['role'] != 'Admin':
        return redirect(url_for('login'))
    
    employees = Employee.query.all()
    return render_template('view_employees.html', employees=employees)

from flask import send_file, redirect, url_for, session, flash
import os

# Route to handle the download of a payslip
@app.route('/download_payslip/<int:payroll_id>')
def download_payslip(payroll_id):
    # Ensure the user is logged in by checking session
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    # Fetch the payroll record by ID
    payroll = Payroll.query.get(payroll_id)
    
    if not payroll:
        flash('Payroll record not found', 'danger')
        return redirect(url_for('manage_payroll'))  # Redirect back to manage payroll if not found

    # Check if the logged-in user has access to this payroll (for example, if it's their own payroll)
    if session['role'] == 'Employee' and payroll.employee_id != session['user_id']:
        flash('You are not authorized to download this payslip.', 'danger')
        return redirect(url_for('employee_dashboard'))  # Redirect to dashboard if unauthorized

    # Assuming you have a folder with generated payslips or generating a file
    payslip_path = f"payslips/{payroll_id}_payslip.pdf"  # Adjust the file path accordingly

    if not os.path.exists(payslip_path):
        flash('Payslip file not found', 'danger')
        return redirect(url_for('payroll'))  # Adjust this as necessary

    # Send the file for download
    return send_file(payslip_path, as_attachment=True, download_name=f"payslip_{payroll_id}.pdf")

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
