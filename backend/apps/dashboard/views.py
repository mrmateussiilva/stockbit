from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta
from apps.products.models import Product, Category
from apps.stock.models import StockMovement
from apps.users.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats(request):
    """Estatísticas gerais do dashboard"""
    
    # Estatísticas de produtos
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    
    # Valor total do estoque
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    
    # Estatísticas de movimentações (últimos 30 dias)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_movements = StockMovement.objects.filter(created_at__gte=thirty_days_ago)
    
    movements_in = recent_movements.filter(movement_type='in').aggregate(
        total=Sum('quantity')
    )['total'] or 0
    
    movements_out = recent_movements.filter(movement_type='out').aggregate(
        total=Sum('quantity')
    )['total'] or 0
    
    # Produtos mais movimentados
    top_moved_products = Product.objects.annotate(
        movement_count=Count('stock_movements')
    ).order_by('-movement_count')[:5]
    
    # Categorias com mais produtos
    top_categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:5]
    
    return Response({
        'products': {
            'total': total_products,
            'active': active_products,
            'low_stock': low_stock_products,
            'out_of_stock': out_of_stock_products,
        },
        'stock_value': float(total_stock_value),
        'movements': {
            'in_last_30_days': movements_in,
            'out_last_30_days': movements_out,
        },
        'top_moved_products': [
            {
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'movement_count': product.movement_count
            }
            for product in top_moved_products
        ],
        'top_categories': [
            {
                'id': category.id,
                'name': category.name,
                'product_count': category.product_count
            }
            for category in top_categories
        ],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def charts_data(request):
    """Dados para gráficos do dashboard"""
    
    # Movimentações por dia (últimos 30 dias)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_movements = StockMovement.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'DATE(created_at)'}
    ).values('day', 'movement_type').annotate(
        quantity=Sum('quantity')
    ).order_by('day')
    
    # Produtos por categoria
    products_by_category = Category.objects.annotate(
        product_count=Count('products'),
        total_value=Sum(F('products__price') * F('products__quantity'))
    ).values('name', 'product_count', 'total_value')
    
    # Estoque baixo por categoria
    low_stock_by_category = Category.objects.annotate(
        low_stock_count=Count('products', filter=Q(products__quantity__lte=F('products__min_quantity')))
    ).values('name', 'low_stock_count')
    
    return Response({
        'daily_movements': list(daily_movements),
        'products_by_category': list(products_by_category),
        'low_stock_by_category': list(low_stock_by_category),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activity(request):
    """Atividade recente do sistema"""
    
    # Movimentações recentes
    recent_movements = StockMovement.objects.select_related(
        'product', 'user'
    ).order_by('-created_at')[:10]
    
    # Produtos criados recentemente
    recent_products = Product.objects.select_related('category').order_by('-created_at')[:5]
    
    return Response({
        'recent_movements': [
            {
                'id': movement.id,
                'product_name': movement.product.name,
                'product_sku': movement.product.sku,
                'movement_type': movement.get_movement_type_display(),
                'quantity': movement.quantity,
                'user_name': movement.user.full_name,
                'created_at': movement.created_at,
            }
            for movement in recent_movements
        ],
        'recent_products': [
            {
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'category_name': product.category.name,
                'price': float(product.price),
                'quantity': product.quantity,
                'created_at': product.created_at,
            }
            for product in recent_products
        ],
    })


