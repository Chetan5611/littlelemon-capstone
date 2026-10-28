from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer


class MenuModelTest(TestCase):
    def test_str(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")


class MenuSerializerTest(TestCase):
    def test_serializer_output(self):
        item = Menu.objects.create(title="Greek Salad", price=12.50, inventory=10)
        data = MenuSerializer(item).data
        self.assertEqual(data["title"], "Greek Salad")
        self.assertEqual(Decimal(data["price"]), Decimal("12.50"))
        self.assertEqual(data["inventory"], 10)


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("chef", password="lemonpass123")
        self.token = Token.objects.create(user=self.user)
        Menu.objects.create(title="IceCream", price=80, inventory=100)
        Menu.objects.create(title="Pasta", price=150, inventory=50)

    def test_list_menu_items(self):
        response = self.client.get("/restaurant/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_single_menu_item(self):
        item = Menu.objects.first()
        response = self.client.get(f"/restaurant/menu/{item.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "IceCream")

    def test_create_requires_auth(self):
        payload = {"title": "Bruschetta", "price": "9.00", "inventory": 20}
        self.assertEqual(
            self.client.post("/restaurant/menu/", payload, format="json").status_code,
            401,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post("/restaurant/menu/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 3)

    def test_update_and_delete(self):
        item = Menu.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.put(
            f"/restaurant/menu/{item.pk}",
            {"title": "Gelato", "price": "85.00", "inventory": 90},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.title, "Gelato")
        response = self.client.delete(f"/restaurant/menu/{item.pk}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Menu.objects.count(), 1)


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("guest", password="lemonpass123")
        self.token = Token.objects.create(user=self.user)
        self.payload = {
            "name": "Chetan",
            "no_of_guests": 4,
            "booking_date": "2026-11-05T19:30:00Z",
        }

    def test_booking_requires_auth(self):
        response = self.client.get("/restaurant/booking/tables/")
        self.assertEqual(response.status_code, 401)

    def test_booking_crud(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        created = self.client.post(
            "/restaurant/booking/tables/", self.payload, format="json"
        )
        self.assertEqual(created.status_code, 201)
        pk = created.json()["id"]

        self.assertEqual(
            len(self.client.get("/restaurant/booking/tables/").json()), 1
        )

        updated = self.client.put(
            f"/restaurant/booking/tables/{pk}/",
            {**self.payload, "no_of_guests": 6},
            format="json",
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(Booking.objects.get(pk=pk).no_of_guests, 6)

        deleted = self.client.delete(f"/restaurant/booking/tables/{pk}/")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

    def test_rejects_zero_guests(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/restaurant/booking/tables/",
            {**self.payload, "no_of_guests": 0},
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class AuthTest(TestCase):
    def test_register_and_get_token(self):
        client = APIClient()
        reg = client.post(
            "/auth/users/",
            {"username": "newuser", "password": "S3cure-Lemon-Pass"},
            format="json",
        )
        self.assertEqual(reg.status_code, 201)
        login = client.post(
            "/auth/token/login/",
            {"username": "newuser", "password": "S3cure-Lemon-Pass"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token", login.json())


class IndexPageTest(TestCase):
    def test_static_html_served(self):
        response = self.client.get("/restaurant/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")
