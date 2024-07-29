import unittest
from app import app, CURR_USER_KEY
from models import db, User, Message

class UserViewsTestCase(unittest.TestCase):
    """Test views for Users."""

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

    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_homepage(self):
        """Test if homepage displays correct information."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome, testuser", str(resp.data))

    

if __name__ == '__main__':
    unittest.main()
