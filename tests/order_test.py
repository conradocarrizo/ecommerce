from datetime import datetime
from tests.base_case import BaseTestCase
from rest_framework import status
from app.models.product import Product
from app.models.order import Order
from app.models.order_detail import OrderDetail


class OrderTestClass(BaseTestCase):
    base_url = "/api/order/"
    instance_url = "/api/order/{}/"

    def setUp(self) -> None:
        super().setUp()
        self.product_a = Product.objects.create(
            name="Product A",
            price=100,
            stock=100,
        )
        self.product_b = Product.objects.create(
            name="Product B",
            price=200,
            stock=100,
        )
        self.product_c = Product.objects.create(
            name="Product C",
            price=300,
            stock=100,
        )

        self.order = Order.objects.create(
            date_time=datetime.now()
        )
        OrderDetail.objects.create(
            product=self.product_a,
            order=self.order,
            quantity=10,
        )

    def test_order_list_no_auth(self):
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_order_list(self):
        response = self.client.get(self.base_url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_get(self):
        response = self.client.get(self.instance_url.format(
            self.order.pk), **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_delete(self):
        quantity_to_restore = self.order.details.all().first().quantity
        stock = self.product_a.stock
        expected_stock = stock + quantity_to_restore

        response = self.client.delete(self.instance_url.format(
            self.order.pk), **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.product_a.refresh_from_db()
        self.assertEqual(self.product_a.stock, expected_stock)

    def test_order_create(self):

        excepted_stock_product_b = self.product_b.stock - 10
        excepted_stock_product_c = self.product_c.stock - 20
        print(self.product_b.id)
        data_to_create = {
            "date_time": datetime.now(),
            "details": [
                {
                    "quantity": 10,
                    "product": {
                        "id": self.product_b.id
                    }
                },
                {
                    "quantity": 20,
                    "product": {
                        "id": self.product_c.id
                    }
                }
            ]
        }
        response = self.client.post(
            self.base_url, data_to_create, **self.bearer_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product_b.refresh_from_db()
        self.product_c.refresh_from_db()

        self.assertEqual(self.product_b.stock, excepted_stock_product_b)
        self.assertEqual(self.product_c.stock, excepted_stock_product_c)

    def test_order_update(self):
        expected_stock_a = self.product_a.stock + 5
        expected_stock_b = self.product_b.stock - 5

        current_detail = self.order.details.first()

        data_to_update = {
            "id": self.order.id,
            "date_time": self.order.date_time,
            "details": [
                {
                    # editing a detail
                    "pk": current_detail.pk,
                    "quantity": current_detail.quantity - 5,
                    "product": {
                        "id": current_detail.product_id
                    }
                },
                {
                    # adding new detail
                    "quantity": 5,
                    "product": {
                        "id": self.product_b.id
                    }
                }
            ]
        }

        response = self.client.put(self.instance_url.format(
            self.order.pk), data=data_to_update, **self.bearer_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product_a.refresh_from_db()
        self.product_b.refresh_from_db()

        self.assertEqual(self.product_a.stock, expected_stock_a)
        self.assertEqual(self.product_b.stock, expected_stock_b)

    def test_order_partial_update(self):
        expected_stock_c = self.product_c.stock - 10
        data_to_update = {
            "id": self.order.id,
            "date_time": self.order.date_time,
            "details": [
                {
                    "quantity": 10,
                    "product": {
                        "id": self.product_c.id
                    }
                }
            ]
        }
        response = self.client.patch(self.instance_url.format(
            self.order.pk), data=data_to_update, **self.bearer_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product_c.refresh_from_db()
        self.assertEqual(self.product_c.stock, expected_stock_c)

    def test_order_partial_update_not_enought_stock(self):
        data_to_update = {
            "id": self.order.id,
            "date_time": self.order.date_time,
            "details": [
                {
                    "quantity": self.product_c.stock+1,
                    "product": {
                        "id": self.product_c.id
                    }
                }
            ]
        }
        response = self.client.patch(self.instance_url.format(
            self.order.pk), data=data_to_update, **self.bearer_token, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        dict_response = response.json()
        self.assertEqual(dict_response["error"],
                         'not enought stock of Product C')

    def test_order_partial_detail_with_negative_quantity(self):
        data_to_update = {
            "id": self.order.id,
            "date_time": self.order.date_time,
            "details": [
                {
                    "quantity": -100,
                    "product": {
                        "id": self.product_c.id
                    }
                }
            ]
        }
        response = self.client.patch(self.instance_url.format(
            self.order.pk), data=data_to_update, **self.bearer_token, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        dict_response = response.json()
        self.assertEqual(dict_response["error"],
                         'the quantity must be a greater than 0, -100 is not')
