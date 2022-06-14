from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestCase(APITestCase):
    @property
    def bearer_token(self):
        user = User.objects.create_user(
            username="username", email='email@email.com', password='some_password'
        )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
