from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    if not User.query.filter_by(username='hariz').first():
        admin = User(username='hariz', email='hariz@gmail.com', role='admin')
        admin.set_password('3103')  # Replace with a secure password
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")



