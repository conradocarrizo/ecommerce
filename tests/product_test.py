from tests.base_case import BaseTestCase
from rest_framework import status
from app.models.product import Product


class ProductTestClass(BaseTestCase):
    base_url = "/api/product/"
    instance_url = "/api/product/{}/"

    def setUp(self) -> None:
        super().setUp()
        self.product = Product.objects.create(
            name="Product A",
            price=100,
            stock=100,
        )

    def test_product_list_no_auth(self):
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_product_list(self):
        response = self.client.get(self.base_url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_get(self):
        response = self.client.get(self.instance_url.format(
            self.product.id), **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update(self):
        data_to_update = {
            "id": self.product.id,
            "name": "Product B",
            "price": 100,
            "stock": 100,
        }
        response = self.client.put(self.instance_url.format(
            self.product.id),
            data=data_to_update, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Product B")

    def test_product_partial_update(self):
        data_to_update = {
            "name": "Product B",
        }
        response = self.client.patch(self.instance_url.format(
            self.product.id),
            data=data_to_update, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Product B")

    def test_product_delete(self):
        response = self.client.delete(self.instance_url.format(
            self.product.id), **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        product = Product.objects.filter(id=self.product.id).first()
        self.assertIsNone(product)

    def test_product_create(self):
        data_to_create = {
            "name": "Product B",
            "price": 100,
            "stock": 100,
        }

        response = self.client.post(
            self.base_url, data_to_create, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.filter(name="Product B").first()
        self.assertIsNotNone(product)

    def test_product_create_invalid_stock(self):
        data_to_create = {
            "name": "Product B",
            "price": 100,
            "stock": -100,
        }

        response = self.client.post(
            self.base_url, data_to_create, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        product = Product.objects.filter(name="Product B").first()
        self.assertIsNone(product)
