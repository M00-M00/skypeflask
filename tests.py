from datetime import datetime, timedelta
import unittest
from app import db, app
from app.models import User, Security

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="tester")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))

    def test_follow(self):
        u = User(username="tester")
        s = Security(ticker = "AAPL")
        db.session.add(u)
        db.session.add(s)
        db.session.commit()
        self.assertEqual(u.followed_tickers(), [])

        u.follow(s)
        self.assertEqual(u.followed_tickers(), [s.ticker])
        self.assertTrue(u.is_following(s))

        u.unfollow(s)
        self.assertEqual(u.followed_tickers(), [])
        self.assertFalse(u.is_following(s))

if __name__ =="__main__":
    unittest.main(verbosity=2)
