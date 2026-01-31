from app import app
from models import db, User, Note
from faker import Faker

fake = Faker()

def seed():
    with app.app_context():
        print('Deleting existing notes...')
        Note.query.delete()

        print('Deleting existing users...')
        User.query.delete()

        print('Creating users...')
        users = []

        # Create a known test user
        test_user = User(username='testuser')
        test_user.password_hash = 'password123'
        users.append(test_user)

        # Create another test user
        other_user = User(username='otheruser')
        other_user.password_hash = 'password123'
        users.append(other_user)

        # Create some random users
        for _ in range(3):
            user = User(username=fake.user_name())
            user.password_hash = 'password'
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        print(f'Seeded {len(users)} users')

        # Create notes for test_user
        print('Creating notes for testuser...')
        notes = []
        for i in range(15):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=test_user.id
            )
            notes.append(note)

        # Create notes for other_user (to test isolation)
        print('Creating notes for otheruser...')
        for i in range(5):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=other_user.id
            )
            notes.append(note)

        db.session.add_all(notes)
        db.session.commit()

        print(f'Seeded {len(notes)} notes')
        print('Test user: username="testuser", password="password123"')
        print('Other user: username="otheruser", password="password123"')

if __name__ == '__main__':
    seed()
