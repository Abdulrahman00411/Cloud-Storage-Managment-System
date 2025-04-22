from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import mysql.connector
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'pptx'}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1112Abdulawan",
            database="Cloud_Storages_Management"
        )
        logging.info("Database connection successful")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        return None

# Database functions (from original CSMS.py, with modifications)
def login_user(email, password):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role FROM Users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            logging.info(f"Login attempt for {email}: {'Success' if user else 'Failed'}")
            conn.close()
            return user
        except mysql.connector.Error as err:
            logging.error(f"Login error: {err}")
            conn.close()
            return None
    return None

def signup_user(username, email, password, role="user"):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                           (username, email, password, role))
            conn.commit()
            logging.info(f"User signup successful: {email}")
            conn.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Signup error: {err}")
            conn.close()
            return False
    return False

def upload_file(file_path, file_type, file_size, file_url, user_id, parent_folder_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Files (file_name, file_type, file_size, file_url, uploaded_by, parent_folder_id) "
                           "VALUES (%s, %s, %s, %s, %s, %s)",
                           (os.path.basename(file_path), file_type, file_size, file_url, user_id, parent_folder_id))
            conn.commit()
            logging.info(f"File uploaded: {os.path.basename(file_path)} by user_id {user_id}")
            conn.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"File upload error: {err}")
            conn.close()
            return False
    return False

def get_user_files(user_id, search_query=""):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT file_name, file_type, file_size, created_at, file_url FROM Files WHERE uploaded_by=%s"
            params = (user_id,)
            if search_query:
                query += " AND file_name LIKE %s"
                params = (user_id, f"%{search_query}%")
            cursor.execute(query, params)
            files = cursor.fetchall()
            logging.info(f"Fetched {len(files)} files for user_id {user_id} with query: {search_query}")
            conn.close()
            return files
        except mysql.connector.Error as err:
            logging.error(f"Get files error: {err}")
            conn.close()
            return []
    return []

def get_all_user_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id, username, email, role FROM Users")
            users = cursor.fetchall()
            user_data = []
            for user in users:
                user_id, username, email, role = user
                cursor.execute("SELECT file_name, file_type, file_size, created_at, file_url FROM Files WHERE uploaded_by=%s", (user_id,))
                files = cursor.fetchall()
                user_data.append({
                    "user_id": user_id,
                    "username": username,
                    "email": email,
                    "role": role,
                    "files": [{"file_name": f[0], "file_type": f[1], "file_size": f[2], "upload_date": f[3], "file_url": f[4]} for f in files]
                })
            logging.info(f"Fetched data for {len(user_data)} users")
            conn.close()
            return user_data
        except mysql.connector.Error as err:
            logging.error(f"Get all user data error: {err}")
            conn.close()
            return []
    return []

def delete_user(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Files WHERE uploaded_by=%s", (user_id,))
            cursor.execute("DELETE FROM Users WHERE user_id=%s", (user_id,))
            conn.commit()
            logging.info(f"User deleted: {user_id}")
            conn.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Delete user error: {err}")
            conn.close()
            return False
    return False

def delete_file(file_name, user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT file_url FROM Files WHERE file_name=%s AND uploaded_by=%s", (file_name, user_id))
            file_url = cursor.fetchone()
            if file_url:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(file_url[0]))
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Removed file from disk: {file_path}")
            cursor.execute("DELETE FROM Files WHERE file_name=%s AND uploaded_by=%s", (file_name, user_id))
            conn.commit()
            logging.info(f"File deleted: {file_name} by user_id {user_id}")
            conn.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Delete file error: {err}")
            conn.close()
            return False
    return False

def update_user_role(user_id, new_role):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Users SET role=%s WHERE user_id=%s", (new_role, user_id))
            conn.commit()
            logging.info(f"Role updated for user_id {user_id} to {new_role}")
            conn.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Update role error: {err}")
            conn.close()
            return False
    return False

# Utility to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'true'
        user = login_user(email, password)
        if user:
            user_id, username, role = user
            if is_admin and user_id not in [100, 102]:
                flash("Restricted admin access.", "error")
                return redirect(url_for('login'))
            session['user_id'] = user_id
            session['username'] = username
            session['role'] = role
            if user_id in [100, 102]:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        flash("Invalid email or password.", "error")
    return render_template('login.html', is_admin=request.args.get('is_admin', 'false') == 'true')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if signup_user(username, email, password):
            flash("User registered successfully! Please log in.", "success")
            return redirect(url_for('login'))
        flash("Registration failed. Email might already exist.", "error")
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))
    
    search_query = ""
    if request.method == 'POST' and 'search' in request.form:
        search_query = request.form.get('search_query', '')
    
    # Handle file upload
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            file_type = filename.rsplit('.', 1)[1].upper()
            file_url = f"/uploads/{filename}"  # URL for accessing file
            parent_folder_id = 10  # Root folder
            if upload_file(filename, file_type, file_size, file_url, session['user_id'], parent_folder_id):
                flash("File uploaded successfully!", "success")
            else:
                flash("File upload failed.", "error")
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            flash("Invalid file type.", "error")
        return redirect(url_for('dashboard'))

    files = get_user_files(session['user_id'], search_query)
    return render_template('dashboard.html', username=session['username'], files=files, search_query=search_query)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session or session['user_id'] not in [100, 102]:
        flash("Restricted admin access.", "error")
        return redirect(url_for('login', is_admin='true'))
    
    # Handle delete file
    if request.method == 'POST' and 'delete_file' in request.form:
        file_name = request.form['file_name']
        user_id = int(request.form['user_id'])
        if delete_file(file_name, user_id):
            flash("File deleted successfully.", "success")
        else:
            flash("Failed to delete file.", "error")
        return redirect(url_for('admin_dashboard'))
    
    # Handle toggle role
    if request.method == 'POST' and 'toggle_role' in request.form:
        user_id = int(request.form['user_id'])
        current_role = request.form['current_role']
        if user_id == session['user_id']:
            flash("Cannot change your own role.", "error")
        else:
            new_role = 'admin' if current_role == 'user' else 'user'
            if update_user_role(user_id, new_role):
                flash(f"Role changed to {new_role}.", "success")
            else:
                flash("Failed to change role.", "error")
        return redirect(url_for('admin_dashboard'))
    
    # Handle delete user
    if request.method == 'POST' and 'delete_user' in request.form:
        user_id = int(request.form['user_id'])
        if user_id == session['user_id']:
            flash("Cannot delete your own account.", "error")
        else:
            if delete_user(user_id):
                flash("User deleted successfully.", "success")
            else:
                flash("Failed to delete user.", "error")
        return redirect(url_for('admin_dashboard'))

    users = get_all_user_data()
    return render_template('admin_dashboard.html', users=users)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)