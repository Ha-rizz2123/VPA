from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    admin_user = User.query.filter_by(email='hariz@gmail.com').first()
    if admin_user:
        print(f"Username: {admin_user.username}, Role: {admin_user.role}")
    else:
        print("Admin user not found.")