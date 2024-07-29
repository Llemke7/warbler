"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import unittest
from app import app
from models import db, User, Message, Likes

class UserModelTestCase(unittest.TestCase):
    """Test model for Users."""

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

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        
        u1 = User.signup(username="testuser1",
                         email="test1@test.com",
                         password="password",
                         image_url=None)
        u2 = User.signup(username="testuser2",
                         email="test2@test.com",
                         password="password",
                         image_url=None)
        db.session.commit()
        
        u1.following.append(u2)
        db.session.commit()
        
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        
        u1 = User.signup(username="testuser1",
                         email="test1@test.com",
                         password="password",
                         image_url=None)
        u2 = User.signup(username="testuser2",
                         email="test2@test.com",
                         password="password",
                         image_url=None)
        db.session.commit()
        
        u1.followers.append(u2)
        db.session.commit()
        
        self.assertTrue(u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(u1))

    

if __name__ == '__main__':
    unittest.main()
