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
