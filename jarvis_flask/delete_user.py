from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Delete all users
    users = User.query.all()
    for user in users:
        db.session.delete(user)
        print(f"Deleted user: {user.username}, Email: {user.email}")
    
    db.session.commit()
    print("All users have been deleted!")