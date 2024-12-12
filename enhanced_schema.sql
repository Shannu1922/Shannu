DROP DATABASE payroll;
CREATE DATABASE payroll;
USE payroll;

CREATE TABLE admin(
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create Employee Table
CREATE TABLE IF NOT EXISTS Employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15) NOT NULL UNIQUE,
    position VARCHAR(50)
);

-- Create LeaveRequest Table
CREATE TABLE IF NOT EXISTS leave_request (
    leave_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES Employee(id)
);

-- Create Payroll Table
CREATE TABLE IF NOT EXISTS Payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    basic_salary DECIMAL(10, 2),
    bonuses DECIMAL(10, 2),
    deductions DECIMAL(10, 2),
    net_salary DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employee(id)
);

-- Create Department Table
CREATE TABLE IF NOT EXISTS Department (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    location VARCHAR(100)
);

-- Create Employee_Department Table to establish relationship between Employee and Department
CREATE TABLE IF NOT EXISTS Employee_Department (
    employee_id INT,
    department_id INT,
    PRIMARY KEY (employee_id, department_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Create Attendance Table
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    check_in DATETIME,
    check_out DATETIME,
    date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employee(id)
);

-- Create Project Table
CREATE TABLE IF NOT EXISTS Project (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2)
);

-- Create Employee_Project Table to establish relationship between Employee and Project
CREATE TABLE IF NOT EXISTS Employee_Project (
    employee_id INT,
    project_id INT,
    role VARCHAR(100),
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
);



-- Insert Sample Data into Employee Table
INSERT INTO Employee (first_name, last_name, email, phone, position)
VALUES
('John', 'Doe', 'john.doe@example.com','9542616615', 'Admin'),
('Jane', 'Smith', 'jane.smith@example.com','9134750360', 'Employee'),
('Alice', 'Johnson', 'alice.johnson@example.com','9131234567', 'Employee'),
('Bob', 'Brown', 'bob.brown@example.com','9139876543', 'Employee');

-- Insert Sample Data into LeaveRequest Table
INSERT INTO leave_request (employee_id, leave_type, start_date, end_date, status)
VALUES
(1, 'Sick Leave', '2024-12-01', '2024-12-05', 'Approved'),
(2, 'Vacation', '2024-12-10', '2024-12-15', 'Pending'),
(3, 'Personal Leave', '2024-12-20', '2024-12-22', 'Rejected'),
(4, 'Sick Leave', '2024-12-05', '2024-12-07', 'Pending');

-- Insert Sample Data into Payroll Table
INSERT INTO Payroll (employee_id, basic_salary, bonuses, deductions, net_salary)
VALUES
(1, 5000.00, 500.00, 200.00, 5300.00),
(2, 4000.00, 300.00, 150.00, 4150.00),
(3, 3500.00, 250.00, 100.00, 3650.00),
(4, 4500.00, 400.00, 250.00, 4650.00);

-- Insert Sample Data into Department Table
INSERT INTO Department (name, location)
VALUES
('HR', 'New York'),
('Engineering', 'San Francisco'),
('Sales', 'Chicago'),
('Marketing', 'Los Angeles');

-- Insert Sample Data into Employee_Department Table
INSERT INTO Employee_Department (employee_id, department_id)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

-- Insert Sample Data into Attendance Table
INSERT INTO Attendance (employee_id, check_in, check_out, date)
VALUES
(1, '2024-12-01 08:00:00', '2024-12-01 17:00:00', '2024-12-01'),
(2, '2024-12-01 09:00:00', '2024-12-01 18:00:00', '2024-12-01'),
(3, '2024-12-01 08:30:00', '2024-12-01 17:30:00', '2024-12-01'),
(4, '2024-12-01 08:15:00', '2024-12-01 17:15:00', '2024-12-01');

-- Insert Sample Data into Project Table
INSERT INTO Project (name, start_date, end_date, budget)
VALUES
('Project A', '2024-01-01', '2024-06-30', 100000.00),
('Project B', '2024-02-01', '2024-07-31', 200000.00),
('Project C', '2024-03-01', '2024-08-31', 150000.00);

-- Insert Sample Data into Employee_Project Table
INSERT INTO Employee_Project (employee_id, project_id, role)
VALUES
(1, 1, 'Project Manager'),
(2, 2, 'Developer'),
(3, 3, 'Designer'),
(4, 1, 'Tester');

INSERT INTO admin( username,password)
VALUES
('Shannu','Shannu1922');


SELECT * FROM Employee;
SELECT * FROM leave_request;
SELECT * FROM Payroll;
SELECT * FROM Department;
SELECT * FROM Employee_Department;
SELECT * FROM Attendance;
SELECT * FROM Project;
SELECT * FROM Employee_Project;
SELECT * FROM admin;