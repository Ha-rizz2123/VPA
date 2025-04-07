'''
from app import create_app
from flask import redirect  # Import redirect from Flask

app = create_app()

@app.route("/")
def index():
    # Redirect to the login page by default
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
'''
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import subprocess
import os
import sqlite3  # Database integration
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf  # CSRF Protection
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'jarvis.db')

app = Flask(__name__, template_folder='app/templates')  # Ensure correct template folder path
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use env variable for security
csrf = CSRFProtect(app)  # Enable CSRF protection

# Form classes for WTForms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Make csrf_token function available in all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=lambda: generate_csrf())

# Session timeout settings
app.permanent_session_lifetime = timedelta(minutes=30)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None

# Initialize database with users and logs tables
def init_db():
    conn = get_db_connection()
    if conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT,
                            email TEXT,
                            role TEXT DEFAULT 'user')''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            action TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        
        # Ensure there is at least one admin
        admin = conn.execute("SELECT * FROM users WHERE role = 'admin'").fetchone()
        if not admin:
            conn.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                         ('admin', generate_password_hash('admin123'), 'admin@example.com', 'admin'))
            conn.commit()
        conn.close()

init_db()

# Helper function to log actions
def log_action(username, action):
    conn = get_db_connection()
    if conn:
        conn.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
        conn.commit()
        conn.close()

# Helper function to check login status
def is_logged_in():
    return 'user' in session

@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    session.modified = True  # Reset session timeout
    return redirect(url_for('admin_dashboard' if session.get('role') == 'admin' else 'dashboard'))

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if not is_logged_in() or session.get('role') != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    conn = get_db_connection()
    if conn:
        users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
        logs = conn.execute("SELECT * FROM logs ORDER BY timestamp DESC").fetchall()
        conn.close()
        return render_template('admin_dashboard.html', username=session['user'], users=users, logs=logs, role=session['role'], current_user=session['user'])
    return "Database error", 500

# User Dashboard Route
@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    session.modified = True
    return render_template('dashboard.html', username=session['user'], role=session['role'])

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conn = get_db_connection()
        if conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            conn.close()
            if user and check_password_hash(user['password'], password):
                session['user'] = user['username']
                session['role'] = user['role']
                session.permanent = True
                log_action(username, "Logged in")
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard' if session['role'] == 'admin' else 'dashboard'))
        flash('Invalid credentials, try again.', 'danger')
    return render_template('login.html', form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)  # Hash password before storing
        conn = get_db_connection()
        if conn:
            existing_user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

            if existing_user:
                flash('Username already taken, choose another one.', 'danger')
                return redirect(url_for('register'))

            conn.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                        (username, email, hashed_password, 'user'))
            conn.commit()
            conn.close()
            log_action('System', f"New user registered: {username}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    if is_logged_in():
        log_action(session['user'], "Logged out")
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Promote User Route
@app.route('/promote_user/<int:user_id>', methods=['POST'])
def promote_user(user_id):
    if not is_logged_in() or session.get('role') != 'admin':
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        conn.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        log_action(session['user'], f"Promoted user {user_id} to admin")
        flash('User promoted to admin successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Demote User Route
@app.route('/demote_user/<int:user_id>', methods=['POST'])
def demote_user(user_id):
    if not is_logged_in() or session.get('role') != 'admin':
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        conn.execute("UPDATE users SET role = 'user' WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        log_action(session['user'], f"Demoted user {user_id} to user")
        flash('Admin demoted to user successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Delete User Route
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not is_logged_in() or session.get('role') != 'admin':
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        log_action(session['user'], f"Deleted user {user_id}")
        flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# API to trigger Jarvis
@app.route('/run_jarvis', methods=['POST'])
@csrf.exempt  # Exempt this route from CSRF protection
def run_jarvis():
    if not is_logged_in():
        return jsonify({'status': 'error', 'message': 'Unauthorized access'})
    try:
        # Path to the original jarvis.py in the 3rd review code folder
        jarvis_path = 'C:/Users/Amjith/Desktop/virtual_pa/3rd reviewcode/jarvis.py'

        # Check if the file exists
        if not os.path.exists(jarvis_path):
            return jsonify({
                'status': 'error',
                'message': 'Jarvis file not found',
                'output': [f"Error: Could not find {jarvis_path}"]
            })

        # Check if Jarvis is already running by looking for a Python process with jarvis.py in the command line
        import psutil
        jarvis_running = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'jarvis.py' in ' '.join(cmdline):
                    jarvis_running = True
                    pid = proc.info['pid']
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if jarvis_running:
            log_action(session['user'], "Jarvis already running")
            return jsonify({
                'status': 'success',
                'message': 'Jarvis is already running',
                'output': [
                    'Jarvis is already running in another window.',
                    'You can interact with it using voice commands.',
                    f'Process ID: {pid}'
                ]
            })

        # Launch the original jarvis.py script in a separate process
        # Use pythonw.exe instead of python.exe to reduce overhead
        # Use subprocess.Popen to start the process without waiting for it to complete
        # Use shell=True to open it in a new window
        # Use creationflags to hide the console window
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.Popen(
            f'pythonw "{jarvis_path}"',
            shell=True,
            creationflags=CREATE_NO_WINDOW
        )

        # Log the action
        log_action(session['user'], "Started Jarvis")

        # Return success message immediately
        return jsonify({
            'status': 'success',
            'message': 'Jarvis started successfully',
            'output': [
                'Jarvis is now running...',
                'The Jarvis application has been launched in a separate window.',
                'You can interact with it using voice commands.',
                f'Process ID: {process.pid}'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'output': [f"Error: {str(e)}"]
        })

# Handle 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
