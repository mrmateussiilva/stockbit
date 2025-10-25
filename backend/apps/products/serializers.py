from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para o modelo Category"""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Product"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'category', 'category_name',
            'price', 'quantity', 'min_quantity', 'is_active', 'stock_status',
            'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_sku(self, value):
        """Valida se o SKU é único"""
        if self.instance and self.instance.sku == value:
            return value
        
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Já existe um produto com este SKU.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de produtos"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category_name', 'price', 
            'quantity', 'stock_status', 'is_active'
        ]

