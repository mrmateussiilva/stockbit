from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductSerializer
from apps.contacts.serializers import ClientSerializer
from apps.users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer para itens de pedido"""
    
    product_detail = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_detail',
            'quantity', 'unit_price', 'discount', 'total',
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total']
    
    def validate(self, data):
        """Valida os dados do item"""
        if data['quantity'] <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero")
        if data['unit_price'] <= 0:
            raise serializers.ValidationError("O preço unitário deve ser maior que zero")
        return data


class OrderSerializer(serializers.ModelSerializer):
    """Serializer para pedidos"""
    
    order_items = OrderItemSerializer(many=True, read_only=True)
    client_detail = ClientSerializer(source='client', read_only=True)
    user_detail = serializers.SerializerMethodField()
    item_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'client', 'client_detail', 'user', 'user_detail',
            'status', 'payment_status', 'order_items', 'item_count',
            'subtotal', 'discount', 'tax', 'total',
            'created_at', 'updated_at', 'completed_at', 'delivery_date', 'due_date',
            'notes', 'shipping_address'
        ]
        read_only_fields = ['id', 'order_number', 'subtotal', 'total', 'created_at', 'updated_at', 'completed_at']
    
    def get_user_detail(self, obj):
        """Retorna informações do usuário"""
        if obj.user:
            return {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'email': obj.user.email
            }
        return None


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de pedidos com itens"""
    
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'client', 'user', 'status', 'payment_status',
            'discount', 'notes', 'shipping_address',
            'order_items', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """Cria um pedido com seus itens"""
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        for item_data in order_items_data:
            # Define o preço unitário se não fornecido
            if 'unit_price' not in item_data or not item_data['unit_price']:
                item_data['unit_price'] = item_data['product'].price
            
            OrderItem.objects.create(order=order, **item_data)
        
        # Recalcula os totais
        order.calculate_totals()
        
        return order
    
    def update(self, instance, validated_data):
        """Atualiza um pedido e seus itens"""
        order_items_data = validated_data.pop('order_items', None)
        
        # Atualiza campos do pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza itens se fornecidos
        if order_items_data is not None:
            # Remove itens antigos
            instance.order_items.all().delete()
            
            # Cria novos itens
            for item_data in order_items_data:
                if 'unit_price' not in item_data or not item_data['unit_price']:
                    item_data['unit_price'] = item_data['product'].price
                
                OrderItem.objects.create(order=instance, **item_data)
            
            # Recalcula totais
            instance.calculate_totals()
        
        return instance


class OrderSummarySerializer(serializers.Serializer):
    """Serializer para resumo de vendas"""
    
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_items_sold = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()

