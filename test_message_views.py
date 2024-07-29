"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import unittest
from app import app, CURR_USER_KEY
from models import db, User, Message

class MessageViewsTestCase(unittest.TestCase):
    """Test views for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
        app.config['SQLALCHEMY_ECHO'] = False
        db.create_all()

        self.user = User.signup(username="testuser",
                                email="test@test.com",
                                password="password",
                                image_url=None)
        db.session.commit()

        self.msg = Message(text="Hello world", user_id=self.user.id)
        db.session.add(self.msg)
        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_add_message(self):
        """Can user add a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.post("/messages/new", data={"text": "Hello world"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello world", str(resp.data))

    def test_delete_message(self):
        """Can user delete a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.post(f"/messages/{self.msg.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Hello world", str(resp.data))

    # Additional tests...

if __name__ == '__main__':
    unittest.main()
