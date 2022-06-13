from django.db import router
from .views import OrderViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
