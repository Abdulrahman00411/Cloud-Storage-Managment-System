Cloud Storage Management System Documentation
This documentation provides an overview of the Cloud Storage Management System, detailing the configuration, database schema, Flask application logic, and SQL operations as provided in the submitted files: .hintrc, Quries.sql, app.py, and some_operation.txt.
Table of Contents

System Overview
Configuration File (.hintrc)
Database Schema (Quries.sql)
Flask Application (app.py)
SQL Operations (some_operation.txt)
Setup Instructions
Usage
Notes and Limitations


System Overview
The Cloud Storage Management System is a web-based application built using Flask, MySQL, and HTML templates. It allows users to:

Register and log in with role-based access (Admin or User).
Upload, view, and delete files in a cloud storage system.
Share files with specific access levels (View, Edit, Download).
Manage user roles and accounts (Admin only).
Maintain file versions and folder structures.

The system uses a MySQL database to store user information, files, folders, file-sharing details, and file versions. The Flask application provides a user interface and handles backend logic, while SQL scripts initialize the database and populate it with sample data.

Configuration File (.hintrc)
The .hintrc file configures linting rules for the project, likely for accessibility and code quality checks using a tool like hint (a static code analysis tool).
