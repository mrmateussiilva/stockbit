from rest_framework import serializers
from .models import StockMovement
from apps.products.serializers import ProductListSerializer
from apps.users.serializers import UserSerializer


class StockMovementSerializer(serializers.ModelSerializer):
    """Serializer para o modelo StockMovement"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    movement_type_display = serializers.CharField(
        source='get_movement_type_display', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'movement_type',
            'movement_type_display', 'quantity', 'reason', 'notes', 'user',
            'user_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        """Cria uma nova movimentação de estoque"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class StockMovementListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de movimentações"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    movement_type_display = serializers.CharField(
        source='get_movement_type_display', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'product_name', 'product_sku', 'movement_type_display',
            'quantity', 'reason', 'user_name', 'created_at'
        ]


class StockSummarySerializer(serializers.Serializer):
    """Serializer para resumo do estoque"""
    total_products = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    low_stock_count = serializers.IntegerField()
    out_of_stock_count = serializers.IntegerField()
    recent_movements = StockMovementListSerializer(many=True)
