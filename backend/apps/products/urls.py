from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet
from .export_views import export_products_excel, export_movements_excel, export_inventory_report_excel

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export/products/', export_products_excel, name='export_products_excel'),
    path('export/movements/', export_movements_excel,
         name='export_movements_excel'),
    path('export/inventory-report/', export_inventory_report_excel,
         name='export_inventory_report_excel'),
]
