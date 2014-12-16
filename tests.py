"""Tests for User, Network, and Infection"""
import unittest

from user import User


class UserTests(unittest.TestCase):
    """Tests for User Class"""
    def test_auto_user_names(self):
        User.user_id = 0
        user0 = User()
        user1 = User()
        self.assertEqual(user0.name, "User0")
        self.assertEqual(user1.name, "User1")

    def test_add_student(self):
        user0 = User()
        user1 = User()
        user0.add_student(user1)
        self.assertEqual(user0.students[0], user1)
        self.assertEqual(user1.coaches[0], user0)

    def test_self_referential(self):
        user = User()
        user.add_student(user)
        self.assertEqual(user.students, [])


class NetworkTests(unittest.TestCase):
    """Tests for Network and Group Class"""
    def test_something(self):
        self.assertEqual(True, True)


class InfectionTests(unittest.TestCase):
    """Tests for Infection Class"""
    def test_something(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
