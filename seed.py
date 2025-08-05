from models.user import db, User
from app import app

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='Elliott').first():
        user = User(
            username='Elliott',
            email='elliott@chicagoassociation.com',
            name='Elliott Graziano',
            is_admin=True,
        )
        user.set_password('7064')
        db.session.add(user)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")
