from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Index
    path('', views.index, name='index'),
    
    # Categorias
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/criar/', views.categoria_criar, name='categoria_criar'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/deletar/', views.categoria_deletar, name='categoria_deletar'),
    
    # Fornecedores
    path('fornecedores/', views.fornecedor_lista, name='fornecedor_lista'),
    path('fornecedores/criar/', views.fornecedor_criar, name='fornecedor_criar'),
    path('fornecedores/<int:pk>/editar/', views.fornecedor_editar, name='fornecedor_editar'),
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_deletar, name='fornecedor_deletar'),
    
    # Produtos
    path('produtos/', views.produto_lista, name='produto_lista'),
    path('produtos/novo/', views.produto_criar, name='produto_criar'),
    path('produtos/<int:pk>/editar/', views.produto_editar, name='produto_editar'),
    
    # Entradas
    path('entrada/manual/', views.entrada_manual, name='entrada_manual'),
    path('entrada/xml/', views.entrada_xml, name='entrada_xml'),
    path('entrada/xml/confirmar/', views.entrada_xml_confirmar, name='entrada_xml_confirmar'),
    
    # Saídas
    path('saida/', views.saida_criar, name='saida_criar'),
    
    # Relatórios
    path('relatorios/', views.relatorio_index, name='relatorio_index'),
    
    # Pedidos WhatsApp
    path('pedidos/whatsapp/', views.pedido_whatsapp, name='pedido_whatsapp'),
    
    # API
    path('api/produto/<int:produto_id>/estoque/', views.api_produto_estoque, name='api_produto_estoque'),
    path('api/sku/verificar/', views.api_verificar_sku, name='api_verificar_sku'),
]

