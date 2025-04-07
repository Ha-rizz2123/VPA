from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from app.models import db, User
from functools import wraps
from app.forms import LoginForm, RegisterForm  # Import your registration form

main = Blueprint('main', __name__)

# -------------------------
# AUTHENTICATION ROUTES
# -------------------------

@main.route('/')
def index():
    return redirect(url_for('main.login'))  # Redirect to the login page

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect admins to admin dashboard and users to user dashboard
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')  # Flash error message

    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()  # Create an instance of the registration form
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please use a different email.", "danger")
            return render_template('register.html', form=form)  # Render the form with the error message

        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose a different one.", "danger")
            return render_template('register.html', form=form)  # Render the form with the error message

        # Create a new user
        new_user = User(username=username, email=email, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# -------------------------
# USER DASHBOARD
# -------------------------
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------------------------
# ADMIN PANEL ROUTES
# -------------------------
def admin_required(f):
    """Decorator to restrict access to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"Current user: {current_user.username}, Role: {current_user.role}")  # Debugging
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('main.login'))
        if current_user.role != 'admin':
            flash("Access Denied! Admins only.", "danger")
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    # Query all users from the database
    users = User.query.all()  # Ensure this fetches all users
    return render_template('admin_dashboard.html', users=users)

@main.route('/admin/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('main.dashboard'))

    user = User.query.get(user_id)
    if user and user.role != 'admin':
        user.role = 'admin'
        db.session.commit()
        flash(f"{user.username} has been promoted to Admin!", "success")
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/demote/<int:user_id>', methods=['POST'])
@login_required
def demote_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('main.dashboard'))

    user = User.query.get(user_id)
    if user and user.role == 'admin':
        user.role = 'user'
        db.session.commit()
        flash(f"{user.username} has been demoted to User!", "warning")
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('main.dashboard'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"{user.username} has been deleted!", "danger")
    return redirect(url_for('main.admin_dashboard'))
