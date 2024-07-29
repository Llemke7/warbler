import unittest
from app import app
from models import db, User, Message

class MessageModelTestCase(unittest.TestCase):
    """Test model for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
        app.config['SQLALCHEMY_ECHO'] = False
        db.create_all()

        user = User.signup(username="testuser",
                           email="test@test.com",
                           password="password",
                           image_url=None)
        db.session.commit()
        self.user = User.query.get(user.id)

    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        msg = Message(
            text="Hello world",
            user_id=self.user.id
        )

        db.session.add(msg)
        db.session.commit()

        # Message should have user associated with it
        self.assertEqual(msg.user.id, self.user.id)
        self.assertEqual(msg.text, "Hello world")

    

if __name__ == '__main__':
    unittest.main()
