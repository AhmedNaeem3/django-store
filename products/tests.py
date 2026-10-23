from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from products.models import Category, Product


class UserRegistrationTests(APITestCase):

    def test_user_registration(self):
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPass123!",
        }

        response = self.client.post("/api/register/", payload, format="json")

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username="testuser")

        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("TestPass123!"))

    def test_registration_with_short_password(self):
        payload = {
            "username": "shortpassuser",
            "email": "short@example.com",
            "password": "abc",
        }

        response = self.client.post("/api/register/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username="shortpassuser").exists())


class ProductPermissionTests(APITestCase):

    def test_anonymous_user_cannot_create_product(self):
        response = self.client.post("/api/products/", {}, format="json")

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_reaches_product_validation(self):
        user = User.objects.create_user(
            username="api_test_user", password="TestPass123!"
        )

        self.client.force_authenticate(user=user)

        response = self.client.post("/api/products/", {}, format="json")

        self.assertEqual(response.status_code, 400)

    def test_valid_jwt_can_access_protected_write(self):
        user = User.objects.create_user(
            username="jwt_test_user", password="TestPass123!"
        )

        response = self.client.post(
            "/api/token/",
            {"username": "jwt_test_user", "password": "TestPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post("/api/products/", {}, format="json")

        self.assertEqual(response.status_code, 400)

    def test_invalid_jwt_cannot_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token")

        response = self.client.post("/api/products/", {}, format="json")

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_product(self):
        user = User.objects.create_user(
            username="product_test_user", password="TestPass123!"
        )

        self.client.force_authenticate(user=user)

        category = Category.objects.create(name="Electronics")

        payload = {
            "name": "New T Product",
            "price": "25.99",
            "stock": 10,
            "status": "active",
            "category_name": "Electronics",
            "tags": [],
            "detail": {"warranty_months": 12, "weight_kg": 0.5},
        }

        response = self.client.post("/api/products/", payload, format="json")

        print(response.status_code)
        print(response.data)

        self.assertEqual(response.status_code, 201)

        product = Product.objects.get(name="New T Product")

        self.assertEqual(product.category.name, "Electronics")
        self.assertEqual(product.tags.count(), 0)
        self.assertEqual(product.detail.warranty_months, 12)
        self.assertEqual(float(product.detail.weight_kg), 0.5)
