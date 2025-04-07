from app import create_app, db
from app.models import User
import time

app = create_app()

with app.app_context():
    try:
        # Check if the first user already exists
        user1 = User.query.filter_by(email='razia@gmail.com').first()
        if not user1:
            user1 = User(username='razia', email='razia@gmail.com', role='user')
            user1.set_password('2405')  # Set the password for user1
            db.session.add(user1)
            print("User 'razia' has been added!")
        else:
            print("User 'razia' already exists!")

        # Check if the second user already exists
        user2 = User.query.filter_by(email='abdul@gmail.com').first()
        if not user2:
            user2 = User(username='abdul', email='abdul@gmail.com', role='user')
            user2.set_password('1610')  # Set the password for user2
            db.session.add(user2)
            print("User 'abdul' has been added!")
        else:
            print("User 'abdul' already exists!")

        # Commit the changes to the database
        db.session.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        db.session.rollback()  # Rollback the session to avoid conflicts

    # List all users
    users = User.query.all()
    if users:
        print("Users in the database:")
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}, Role: {user.role}")
    else:
        print("No users found in the database.")