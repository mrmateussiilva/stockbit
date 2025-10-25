from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet
from apps.products.export_views import export_movements_excel

router = DefaultRouter()
router.register(r'movements', StockMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export/movements/', export_movements_excel, name='export_movements_excel'),
]

