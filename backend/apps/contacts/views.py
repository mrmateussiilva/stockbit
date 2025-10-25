from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Client, Supplier
from .serializers import ClientSerializer, SupplierSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar clientes"""
    
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'city', 'state']
    search_fields = ['name', 'cpf_cnpj', 'email', 'phone', 'cellphone']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filtra clientes ativos por padrão"""
        queryset = Client.objects.all()
        
        # Se não especificado, mostra apenas ativos
        if self.request.query_params.get('show_inactive') != 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retorna estatísticas dos clientes"""
        total = Client.objects.count()
        active = Client.objects.filter(is_active=True).count()
        inactive = total - active
        individuals = Client.objects.filter(type='individual').count()
        companies = Client.objects.filter(type='company').count()
        
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive,
            'individuals': individuals,
            'companies': companies,
        })
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Alterna o status ativo/inativo do cliente"""
        client = self.get_object()
        client.is_active = not client.is_active
        client.save()
        
        status_text = 'ativado' if client.is_active else 'desativado'
        return Response({
            'message': f'Cliente {status_text} com sucesso',
            'is_active': client.is_active
        })


class SupplierViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar fornecedores"""
    
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'city', 'state']
    search_fields = ['name', 'cpf_cnpj', 'email', 'phone', 'cellphone', 'contact_person']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filtra fornecedores ativos por padrão"""
        queryset = Supplier.objects.all()
        
        # Se não especificado, mostra apenas ativos
        if self.request.query_params.get('show_inactive') != 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retorna estatísticas dos fornecedores"""
        total = Supplier.objects.count()
        active = Supplier.objects.filter(is_active=True).count()
        inactive = total - active
        individuals = Supplier.objects.filter(type='individual').count()
        companies = Supplier.objects.filter(type='company').count()
        
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive,
            'individuals': individuals,
            'companies': companies,
        })
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Alterna o status ativo/inativo do fornecedor"""
        supplier = self.get_object()
        supplier.is_active = not supplier.is_active
        supplier.save()
        
        status_text = 'ativado' if supplier.is_active else 'desativado'
        return Response({
            'message': f'Fornecedor {status_text} com sucesso',
            'is_active': supplier.is_active
        })