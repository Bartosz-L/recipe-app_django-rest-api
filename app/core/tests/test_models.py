from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    # test creating a new user with an email is successful
    def test_create_user_with_email_successful(self):
        email = 'test@test.com'
        password = 'TestP@ssword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # test the email for a new user is normalized
    def test_new_user_email_normalized(self):
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    # test creating user with no email raises error
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
