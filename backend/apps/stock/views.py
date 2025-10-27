from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from .models import StockMovement
from .serializers import StockMovementSerializer, StockMovementListSerializer, StockSummarySerializer
from apps.products.models import Product


class StockMovementViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar movimentações de estoque"""
    queryset = StockMovement.objects.select_related('product', 'user').all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movement_type', 'product', 'user']
    search_fields = ['product__name', 'product__sku', 'reason', 'notes']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return StockMovementListSerializer
        return StockMovementSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumo do estoque"""
        # Estatísticas gerais
        total_products = Product.objects.count()
        total_value = Product.objects.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0

        low_stock_count = Product.objects.filter(
            quantity__lte=F('min_quantity')
        ).count()

        out_of_stock_count = Product.objects.filter(quantity=0).count()

        # Movimentações recentes (últimos 7 dias)
        recent_movements = self.get_queryset().filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        )[:10]

        summary_data = {
            'total_products': total_products,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'recent_movements': recent_movements,
        }

        serializer = StockSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estatísticas das movimentações"""
        # Movimentações por tipo
        movements_by_type = self.get_queryset().values('movement_type').annotate(
            count=Count('id'),
            total_quantity=Sum('quantity')
        )

        # Movimentações por dia (últimos 30 dias)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_movements = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).extra(
            select={'day': 'DATE(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')

        return Response({
            'movements_by_type': list(movements_by_type),
            'daily_movements': list(daily_movements),
        })
