# Hospital Management System — DBMS Mini Project Report

**Student Name:** [Your Name]  
**Department / Year:** [Your Department and Year]  
**College:** [Your College]  
**Subject:** Database Management Systems  
**Project Title:** Hospital Management System

## 1. Introduction
The Hospital Management System is a web-based application designed to organize patient records, doctor information, and appointments. It uses a relational database to reduce duplicate data and make records easier to maintain.

## 2. Problem Statement
Maintaining patient, doctor, and appointment information manually can cause duplication, inconsistent records, and slow retrieval. This project demonstrates how a database-backed application can organize this information.

## 3. Objectives
- Store and retrieve patient and doctor details.
- Book appointments and update appointment status.
- Demonstrate CRUD operations and relational integrity.
- Use joins, aggregate queries, and a database view.
- Build a simple web interface with Flask and MySQL.

## 4. ER Diagram
Use this relationship summary to draw the ER diagram in draw.io or on paper:

`PATIENTS (1) ---- (M) APPOINTMENTS (M) ---- (1) DOCTORS`

`appointments.patient_id` references `patients.patient_id`; `appointments.doctor_id` references `doctors.doctor_id`.

## 5. Database Schema
- **patients:** patient_id (PK), full_name, age, gender, phone, email, address, created_at
- **doctors:** doctor_id (PK), full_name, department, phone, email, created_at
- **appointments:** appointment_id (PK), patient_id (FK), doctor_id (FK), appointment_date, reason, status, created_at
- **appointment_report:** SQL view joining appointment, patient, and doctor data

## 6. Technologies Used
Python, Flask, MySQL, mysql-connector-python, HTML, CSS, Git, GitHub.

## 7. SQL Queries and Features Implemented
- CREATE TABLE with primary and foreign keys
- NOT NULL, UNIQUE, CHECK, ENUM constraints
- INSERT, SELECT, UPDATE, DELETE
- INNER JOIN and LEFT JOIN
- COUNT and GROUP BY
- `appointment_report` view
- Foreign-key cascading on patient/doctor deletion

## 8. Screenshots
Add screenshots of:
1. Dashboard
2. Patient list and add-patient form
3. Doctor list and add-doctor form
4. Appointment booking and status update
5. Reports page
6. MySQL tables in Workbench

Save screenshots in `screenshots/` and embed them here, for example:
`![Dashboard](screenshots/dashboard.png)`

## 9. Conclusion
The project demonstrates how a relational database can manage patient, doctor, and appointment information. It applies relational design, constraints, CRUD operations, joins, and a view through a Flask web application.

## 10. Future Scope
- Login with role-based access for administrator, doctor, and receptionist
- Billing and pharmacy modules
- Appointment reminders
- Search, edit forms, and exportable reports

**Note:** This is an educational demonstration, not a production hospital system. Do not use real patient data.
