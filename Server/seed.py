from app import app
from models import db, User
from faker import Faker

fake = Faker()

def seed():
    with app.app_context():
        print('Deleting existing users...')
        User.query.delete()

        print('Creating users...')
        users = []

        # Create a known test user
        test_user = User(username='testuser')
        test_user.password_hash = 'password123'
        users.append(test_user)

        # Create some random users
        for _ in range(5):
            user = User(username=fake.user_name())
            user.password_hash = 'password'
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        print(f'Seeded {len(users)} users')
        print('Test user: username="testuser", password="password123"')

if __name__ == '__main__':
    seed()
