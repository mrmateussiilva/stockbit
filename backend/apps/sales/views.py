from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, 
    OrderItemSerializer, 
    OrderCreateSerializer,
    OrderSummarySerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar pedidos"""
    
    queryset = Order.objects.select_related('client', 'user').prefetch_related('order_items')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'client', 'user']
    search_fields = ['order_number', 'client__name', 'notes']
    ordering_fields = ['created_at', 'total', 'order_number']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado"""
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """Filtra pedidos baseado em parâmetros de query"""
        queryset = super().get_queryset()
        
        # Filtro por data
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Filtro por status de pagamento
        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        return queryset
    
    def perform_create(self, serializer):
        """Cria um pedido associando ao usuário atual se não especificado"""
        if 'user' not in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marca um pedido como concluído"""
        order = self.get_object()
        
        if order.status == 'completed':
            return Response(
                {'error': 'Pedido já está concluído'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se há estoque suficiente
        for item in order.order_items.all():
            if item.product.quantity < item.quantity:
                return Response(
                    {'error': f'Estoque insuficiente para {item.product.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        order.mark_as_completed()
        return Response({
            'message': 'Pedido concluído com sucesso',
            'order': OrderSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancela um pedido"""
        order = self.get_object()
        
        if order.status in ['completed', 'cancelled']:
            return Response(
                {'error': 'Não é possível cancelar este pedido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        return Response({
            'message': 'Pedido cancelado com sucesso',
            'order': OrderSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Marca um pedido como pago"""
        order = self.get_object()
        order.payment_status = 'paid'
        order.save()
        
        return Response({
            'message': 'Pagamento registrado com sucesso',
            'order': OrderSerializer(order).data
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Retorna resumo de vendas"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Calcula estatísticas
        total_orders = queryset.count()
        completed_orders = queryset.filter(status='completed').count()
        pending_orders = queryset.filter(status='pending').count()
        
        # Receita total de pedidos completos
        revenue = queryset.filter(status='completed').aggregate(
            total=Sum('total')
        )['total'] or Decimal('0.00')
        
        # Total de itens vendidos
        items_sold = OrderItem.objects.filter(
            order__status='completed'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        # Valor médio do pedido
        avg_order_value = revenue / completed_orders if completed_orders > 0 else Decimal('0.00')
        
        summary = {
            'total_orders': total_orders,
            'total_revenue': revenue,
            'total_items_sold': items_sold,
            'average_order_value': avg_order_value,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
        }
        
        serializer = OrderSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retorna pedidos recentes"""
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar itens de pedido"""
    
    queryset = OrderItem.objects.select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order', 'product']
    search_fields = ['product__name', 'notes']
    ordering_fields = ['created_at', 'total', 'quantity']
    ordering = ['-created_at']

