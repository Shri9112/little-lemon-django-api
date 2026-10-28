from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Booking, MenuItem

User = get_user_model()

class LittleLemonAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="SafePass123!")
        self.token = Token.objects.create(user=self.user)

    def test_homepage_serves_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Little Lemon")

    def test_menu_list_is_public(self):
        MenuItem.objects.create(title="Lemon Cake", price="5.50", inventory=10)
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Lemon Cake")

    def test_menu_create_requires_authentication(self):
        response = self.client.post("/api/menu/", {
            "title": "Pasta", "price": "12.50", "inventory": 5
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_menu_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post("/api/menu/", {
            "title": "Pasta", "price": "12.50", "inventory": 5
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_returns_token(self):
        response = self.client.post("/api/registration/", {
            "username": "newuser", "email": "new@example.com", "password": "StrongPass456!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_booking_requires_authentication(self):
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post("/api/bookings/", {
            "name": "Shri", "no_of_guests": 2,
            "booking_date": (timezone.now() + timedelta(days=1)).isoformat()
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
