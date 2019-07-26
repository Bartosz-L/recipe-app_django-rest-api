from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    # test the publicly available tags API

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        # test that login is required for retrieveing tags
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    # test the authorized user tags API

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpassword',
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        # test retrieving tags
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        # test that tags returned are for the authenticated user
        # and not for the other user
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'test2password2',
        )

        Tag.objects.create(user=user2, name='Thai')
        tag = Tag.objects.create(user=self.user, name='Chinese')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        # test creating a nwe tag
        payload = {
            'name': 'Test Tag',
        }

        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        # test creating a nwe tag with invalid payload
        payload = {
            'name': ''
        }

        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)