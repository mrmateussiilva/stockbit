from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Product, Category, Supplier, StockMovement, WhatsAppOrder
from .forms import (
    ProductForm, CategoryForm, SupplierForm,
    EntradaManualForm, SaidaForm, XMLUploadForm
)
from .utils.xml_parser import parse_nfe_xml, encontrar_produto_por_codigo, baixar_xml_de_url
from .utils.export_xlsx import exportar_produtos_para_xlsx, exportar_relatorio_para_xlsx


def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('estoque:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('estoque:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'estoque/login.html', {'form': form})


def logout_view(request):
    """View de logout"""
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('estoque:login')


@login_required
def index(request):
    """Página inicial com dashboard"""
    from django.core.cache import cache
    
    # Cache de estatísticas por 5 minutos
    cache_key = 'dashboard_stats'
    stats = cache.get(cache_key)
    
    if stats is None:
        # Otimização: usa select_related e prefetch_related
        total_produtos = Product.objects.count()
        total_categorias = Category.objects.count()
        
        # Produtos com estoque baixo (critico <= 5 ou abaixo do mínimo configurado)
        produtos_baixo_estoque = Product.objects.filter(
            Q(quantidade_estoque__lte=5) |
            Q(quantidade_estoque__lte=F('estoque_minimo'), estoque_minimo__gt=0)
        ).count()
        
        # Produtos com estoque abaixo do mínimo configurado
        produtos_abaixo_minimo = Product.objects.filter(
            quantidade_estoque__lte=F('estoque_minimo'),
            estoque_minimo__gt=0
        ).count()
        
        # Calcula valor total do estoque (otimizado)
        valor_total_estoque = Product.objects.aggregate(
            total=Sum(F('quantidade_estoque') * F('custo_unitario'))
        )['total'] or Decimal('0.00')
        
        stats = {
            'total_produtos': total_produtos,
            'total_categorias': total_categorias,
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'produtos_abaixo_minimo': produtos_abaixo_minimo,
            'valor_total_estoque': valor_total_estoque,
        }
        cache.set(cache_key, stats, 300)  # Cache por 5 minutos
    
    # Movimentações recentes (sempre atualizado, sem cache)
    movimentacoes_recentes = StockMovement.objects.select_related(
        'produto', 'usuario'
    ).only(
        'tipo', 'quantidade', 'created_at', 'produto__nome', 'produto__unidade', 'usuario__username'
    ).order_by('-created_at')[:10]
    
    # Produtos com menor estoque (otimizado) - considera mínimo configurado ou <= 5
    produtos_criticos = Product.objects.select_related('categoria').filter(
        Q(quantidade_estoque__lte=5) |
        Q(quantidade_estoque__lte=F('estoque_minimo'), estoque_minimo__gt=0)
    ).only(
        'nome', 'quantidade_estoque', 'estoque_minimo', 'unidade', 'categoria__nome'
    ).order_by('quantidade_estoque')[:10]
    
    # Dados para gráfico de movimentações (últimos 7 dias)
    from datetime import timedelta
    from django.utils import timezone
    
    hoje = timezone.now().date()
    sete_dias_atras = hoje - timedelta(days=7)
    
    # Prepara dados para o gráfico (últimos 7 dias)
    dias_labels = []
    entradas_data = []
    saidas_data = []
    
    for dia in range(7):
        data_dia = sete_dias_atras + timedelta(days=dia)
        dias_labels.append(data_dia.strftime('%d/%m'))
        
        # Busca movimentações por dia específico
        mov_entradas = StockMovement.objects.filter(
            created_at__date=data_dia,
            tipo='ENTRADA'
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        
        mov_saidas = StockMovement.objects.filter(
            created_at__date=data_dia,
            tipo='SAIDA'
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        
        entradas_data.append(float(mov_entradas))
        saidas_data.append(float(mov_saidas))
    
    context = {
        **stats,
        'movimentacoes_recentes': movimentacoes_recentes,
        'produtos_criticos': produtos_criticos,
        'grafico_labels': mark_safe(json.dumps(dias_labels)),
        'grafico_entradas': mark_safe(json.dumps(entradas_data)),
        'grafico_saidas': mark_safe(json.dumps(saidas_data)),
    }
    
    return render(request, 'estoque/index.html', context)


# ============ CATEGORIAS ============

@login_required
def categoria_lista(request):
    """Lista de categorias"""
    categorias = Category.objects.all().order_by('nome')
    return render(request, 'estoque/categorias/lista.html', {
        'categorias': categorias,
    })


@login_required
def categoria_criar(request):
    """Criar nova categoria"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('estoque:categoria_lista')
    else:
        form = CategoryForm()
    
    return render(request, 'estoque/categorias/form.html', {
        'form': form,
        'titulo': 'Nova Categoria'
    })


@login_required
def categoria_editar(request, pk):
    """Editar categoria existente"""
    categoria = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" atualizada com sucesso!')
            return redirect('estoque:categoria_lista')
    else:
        form = CategoryForm(instance=categoria)
    
    return render(request, 'estoque/categorias/form.html', {
        'form': form,
        'titulo': 'Editar Categoria',
        'categoria': categoria
    })


@login_required
def categoria_deletar(request, pk):
    """Deletar categoria"""
    categoria = get_object_or_404(Category, pk=pk)
    
    # Verifica se há produtos usando esta categoria
    produtos_count = Product.objects.filter(categoria=categoria).count()
    
    if produtos_count > 0:
        messages.error(
            request,
            f'Não é possível deletar a categoria "{categoria.nome}" pois existem {produtos_count} produto(s) vinculado(s) a ela.'
        )
        return redirect('estoque:categoria_lista')
    
    if request.method == 'POST':
        nome_categoria = categoria.nome
        categoria.delete()
        messages.success(request, f'Categoria "{nome_categoria}" deletada com sucesso!')
        return redirect('estoque:categoria_lista')
    
    return render(request, 'estoque/categorias/confirmar_delete.html', {
        'categoria': categoria
    })


# ============ FORNECEDORES ============

@login_required
def fornecedor_lista(request):
    """Lista de fornecedores"""
    fornecedores = Supplier.objects.all().order_by('nome')
    return render(request, 'estoque/fornecedores/lista.html', {
        'fornecedores': fornecedores,
    })


@login_required
def fornecedor_criar(request):
    """Criar novo fornecedor"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" criado com sucesso!')
            return redirect('estoque:fornecedor_lista')
    else:
        form = SupplierForm()
    
    return render(request, 'estoque/fornecedores/form.html', {
        'form': form,
        'titulo': 'Novo Fornecedor'
    })


@login_required
def fornecedor_editar(request, pk):
    """Editar fornecedor existente"""
    fornecedor = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" atualizado com sucesso!')
            return redirect('estoque:fornecedor_lista')
    else:
        form = SupplierForm(instance=fornecedor)
    
    return render(request, 'estoque/fornecedores/form.html', {
        'form': form,
        'titulo': 'Editar Fornecedor',
        'fornecedor': fornecedor
    })


@login_required
def fornecedor_deletar(request, pk):
    """Deletar fornecedor"""
    fornecedor = get_object_or_404(Supplier, pk=pk)
    
    # Verifica se há movimentações usando este fornecedor
    movimentacoes_count = StockMovement.objects.filter(fornecedor=fornecedor).count()
    
    if movimentacoes_count > 0:
        messages.error(
            request,
            f'Não é possível deletar o fornecedor "{fornecedor.nome}" pois existem {movimentacoes_count} movimentação(ões) vinculada(s) a ele.'
        )
        return redirect('estoque:fornecedor_lista')
    
    if request.method == 'POST':
        nome_fornecedor = fornecedor.nome
        fornecedor.delete()
        messages.success(request, f'Fornecedor "{nome_fornecedor}" deletado com sucesso!')
        return redirect('estoque:fornecedor_lista')
    
    return render(request, 'estoque/fornecedores/confirmar_delete.html', {
        'fornecedor': fornecedor
    })


# ============ PRODUTOS ============

@login_required
def produto_lista(request):
    """Lista de produtos com filtros e paginação"""
    from django.core.paginator import Paginator
    
    # Query otimizada com select_related
    produtos = Product.objects.select_related('categoria').only(
        'codigo', 'nome', 'categoria__nome', 'unidade', 
        'quantidade_estoque', 'custo_unitario', 'ncm'
    )
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    busca = request.GET.get('busca')
    ordenar = request.GET.get('ordenar', 'nome')
    
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(codigo__icontains=busca) |
            Q(ncm__icontains=busca)
        )
    
    # Ordenação
    ordenacoes_validas = {
        'nome': 'nome',
        '-nome': '-nome',
        'codigo': 'codigo',
        '-codigo': '-codigo',
        'quantidade': 'quantidade_estoque',
        '-quantidade': '-quantidade_estoque',
        'custo': 'custo_unitario',
        '-custo': '-custo_unitario',
    }
    
    ordenacao = ordenacoes_validas.get(ordenar, 'nome')
    produtos = produtos.order_by(ordenacao)
    
    categorias = Category.objects.only('id', 'nome').order_by('nome')
    
    # Exportação XLSX
    if request.GET.get('exportar') == 'xlsx':
        return exportar_produtos_para_xlsx(produtos)
    
    # Paginação (20 itens por página)
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'produtos': page_obj,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'busca': busca,
        'ordenar': ordenar,
    }
    
    return render(request, 'estoque/produtos/lista.html', context)


@login_required
def produto_criar(request):
    """Criar novo produto"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" criado com sucesso!')
            return redirect('estoque:produto_lista')
    else:
        form = ProductForm()
    
    return render(request, 'estoque/produtos/form.html', {'form': form, 'titulo': 'Novo Produto'})


@login_required
def produto_editar(request, pk):
    """Editar produto existente"""
    produto = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('estoque:produto_detalhar', pk=produto.pk)
    else:
        form = ProductForm(instance=produto)
    
    return render(request, 'estoque/produtos/form.html', {
        'form': form,
        'produto': produto,
        'titulo': f'Editar {produto.nome}'
    })


@login_required
def produto_detalhar(request, pk):
    """Visualização detalhada de produto"""
    produto = get_object_or_404(Product.objects.select_related('categoria'), pk=pk)
    
    # Últimas movimentações (10 mais recentes)
    movimentacoes_recentes = produto.movimentacoes.select_related('usuario', 'fornecedor').order_by('-created_at')[:10]
    
    # Estatísticas do produto
    total_entradas = produto.movimentacoes.filter(tipo='ENTRADA').aggregate(
        total=Sum('quantidade')
    )['total'] or Decimal('0.00')
    
    total_saidas = produto.movimentacoes.filter(tipo='SAIDA').aggregate(
        total=Sum('quantidade')
    )['total'] or Decimal('0.00')
    
    # Dados para gráfico de evolução do estoque (últimos 30 dias)
    from datetime import timedelta
    hoje = timezone.now().date()
    trinta_dias_atras = hoje - timedelta(days=30)
    
    # Agrupa movimentações por dia para o gráfico
    movimentacoes_grafico = produto.movimentacoes.filter(
        created_at__date__gte=trinta_dias_atras
    ).order_by('created_at')
    
    # Calcula estoque ao longo do tempo
    estoque_historico = []
    estoque_atual = Decimal('0.00')
    labels = []
    dados = []
    
    # Calcula estoque dia a dia
    dias_unicos = set()
    for mov in movimentacoes_grafico:
        dias_unicos.add(mov.created_at.date())
    
    dias_unicos = sorted(dias_unicos)
    
    for dia in dias_unicos:
        movs_dia = movimentacoes_grafico.filter(created_at__date=dia)
        estoque_dia = estoque_atual
        for mov in movs_dia:
            if mov.tipo == 'ENTRADA':
                estoque_dia += mov.quantidade
            else:
                estoque_dia -= mov.quantidade
        
        labels.append(dia.strftime('%d/%m'))
        dados.append(float(estoque_dia))
        estoque_atual = estoque_dia
    
    context = {
        'produto': produto,
        'movimentacoes_recentes': movimentacoes_recentes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'grafico_labels': mark_safe(json.dumps(labels)),
        'grafico_dados': mark_safe(json.dumps(dados)),
    }
    
    return render(request, 'estoque/produtos/detalhar.html', context)


@login_required
def produto_historico(request, pk):
    """Histórico completo de movimentações do produto"""
    produto = get_object_or_404(Product, pk=pk)
    
    # Filtros
    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')
    tipo_filter = request.GET.get('tipo')
    
    movimentacoes = produto.movimentacoes.select_related('usuario', 'fornecedor').all()
    
    # Aplica filtros
    if data_inicio_str:
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            movimentacoes = movimentacoes.filter(created_at__gte=data_inicio)
        except:
            pass
    
    if data_fim_str:
        try:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
            movimentacoes = movimentacoes.filter(created_at__lte=data_fim)
        except:
            pass
    
    if tipo_filter and tipo_filter in ['ENTRADA', 'SAIDA']:
        movimentacoes = movimentacoes.filter(tipo=tipo_filter)
    
    # Ordena por data mais recente
    movimentacoes = movimentacoes.order_by('-created_at')
    
    # Adiciona valor total calculado para cada movimentação
    movimentacoes_com_total = []
    for mov in movimentacoes:
        valor_total = mov.quantidade * mov.custo_unitario
        mov.valor_total = valor_total
        movimentacoes_com_total.append(mov)
    
    # Paginação
    from django.core.paginator import Paginator
    paginator = Paginator(movimentacoes_com_total, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'produto': produto,
        'movimentacoes': page_obj,
        'data_inicio': data_inicio_str,
        'data_fim': data_fim_str,
        'tipo_filter': tipo_filter,
    }
    
    return render(request, 'estoque/produtos/historico.html', context)


@login_required
def produto_deletar(request, pk):
    """Deletar produto"""
    produto = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        nome_produto = produto.nome
        movimentacoes_count = produto.movimentacoes.count()
        
        # Deleta o produto (as movimentações serão deletadas automaticamente via CASCADE)
        produto.delete()
        
        if movimentacoes_count > 0:
            messages.success(
                request, 
                f'Produto "{nome_produto}" deletado com sucesso! '
                f'({movimentacoes_count} movimentação(ões) também foram removida(s))'
            )
        else:
            messages.success(request, f'Produto "{nome_produto}" deletado com sucesso!')
        
        return redirect('estoque:produto_lista')
    
    return render(request, 'estoque/produtos/confirmar_delete.html', {
        'produto': produto
    })


# ============ ENTRADAS ============

@login_required
def entrada_manual(request):
    """Entrada manual de produtos"""
    if request.method == 'POST':
        form = EntradaManualForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False, user=request.user)
            movimentacao.save()
            messages.success(
                request,
                f'Entrada de {movimentacao.quantidade} {movimentacao.produto.unidade} '
                f'de "{movimentacao.produto.nome}" registrada com sucesso!'
            )
            return redirect('estoque:entrada_manual')
    else:
        form = EntradaManualForm()
    
    return render(request, 'estoque/entradas/manual.html', {'form': form})


@login_required
def entrada_xml(request):
    """Entrada de produtos via XML de NF-e"""
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tipo_entrada = form.cleaned_data.get('tipo_entrada')
            fornecedor = form.cleaned_data.get('fornecedor')
            arquivo_xml = None
            
            try:
                # Processa de acordo com o tipo de entrada
                if tipo_entrada == 'arquivo':
                    arquivo_xml = request.FILES['arquivo_xml']
                elif tipo_entrada == 'url':
                    url_xml = form.cleaned_data.get('url_xml')
                    # Baixa o XML da URL
                    arquivo_xml = baixar_xml_de_url(url_xml)
                
                # Faz o parsing do XML
                produtos_xml = parse_nfe_xml(arquivo_xml)
                
                if not produtos_xml:
                    messages.warning(request, 'Nenhum produto encontrado no XML.')
                    return redirect('estoque:entrada_xml')
                
                # Prepara dados para exibição e criação
                produtos_processados = []
                produtos_nao_encontrados = []
                
                for produto_xml in produtos_xml:
                    # Calcula valor total do item
                    produto_xml['valor_total'] = produto_xml['quantidade'] * produto_xml['valor_unitario']
                    
                    # Tenta encontrar produto existente
                    produto_db = encontrar_produto_por_codigo(
                        produto_xml['codigo'],
                        produto_xml['ncm'],
                        produto_xml['ean']
                    )
                    
                    if produto_db:
                        produto_xml['produto_db'] = produto_db
                        produto_xml['novo'] = False
                        produtos_processados.append(produto_xml)
                    else:
                        produtos_nao_encontrados.append(produto_xml)
                
                # Converte Decimal para float antes de salvar na sessão (JSON não serializa Decimal)
                produtos_xml_serializaveis = []
                for produto in produtos_xml:
                    produto_serial = produto.copy()
                    produto_serial['quantidade'] = float(produto['quantidade'])
                    produto_serial['valor_unitario'] = float(produto['valor_unitario'])
                    produto_serial['valor_total'] = float(produto.get('valor_total', produto['quantidade'] * produto['valor_unitario']))
                    # Remove objetos que não podem ser serializados
                    produto_serial.pop('produto_db', None)
                    produtos_xml_serializaveis.append(produto_serial)
                
                # Salva na sessão para processamento posterior
                request.session['produtos_xml'] = produtos_xml_serializaveis
                request.session['fornecedor_id'] = fornecedor.id if fornecedor else None
                
                # Calcula totais para exibição
                total_produtos = len(produtos_xml)
                total_encontrados = len(produtos_processados)
                total_novos = len(produtos_nao_encontrados)
                valor_total = Decimal('0.00')
                
                for produto in produtos_xml:
                    valor_total += produto['quantidade'] * produto['valor_unitario']
                
                context = {
                    'produtos_processados': produtos_processados,
                    'produtos_nao_encontrados': produtos_nao_encontrados,
                    'form': form,
                    'total_produtos': total_produtos,
                    'total_encontrados': total_encontrados,
                    'total_novos': total_novos,
                    'valor_total': valor_total,
                }
                
                return render(request, 'estoque/entradas/xml_preview.html', context)
                
            except ValueError as e:
                messages.error(request, f'Erro ao processar XML: {str(e)}')
            except ET.ParseError as e:
                messages.error(request, f'Erro ao fazer parse do XML: {str(e)}')
            except Exception as e:
                import traceback
                messages.error(request, f'Erro inesperado ao processar XML: {str(e)}')
                # Log do erro completo para debug
                print(f"Erro completo ao processar XML: {traceback.format_exc()}")
    else:
        form = XMLUploadForm()
    
    return render(request, 'estoque/entradas/xml.html', {'form': form})


@login_required
def entrada_xml_confirmar(request):
    """Confirma e processa entrada de produtos via XML"""
    if request.method == 'POST':
        produtos_xml = request.session.get('produtos_xml', [])
        fornecedor_id = request.session.get('fornecedor_id')
        
        # Verifica se há produtos na sessão
        if not produtos_xml:
            messages.error(request, 'Nenhum produto encontrado na sessão. Por favor, faça o upload do XML novamente.')
            return redirect('estoque:entrada_xml')
        
        # Converte de volta para Decimal (vem da sessão como float)
        produtos_xml_desserializados = []
        for produto in produtos_xml:
            produto_dec = produto.copy()
            produto_dec['quantidade'] = Decimal(str(produto['quantidade']))
            produto_dec['valor_unitario'] = Decimal(str(produto['valor_unitario']))
            produto_dec['valor_total'] = Decimal(str(produto.get('valor_total', produto['quantidade'] * produto['valor_unitario'])))
            produtos_xml_desserializados.append(produto_dec)
        
        produtos_xml = produtos_xml_desserializados
        
        # Busca fornecedor se fornecido
        fornecedor = None
        if fornecedor_id:
            try:
                fornecedor = Supplier.objects.get(pk=fornecedor_id)
            except Supplier.DoesNotExist:
                messages.warning(request, f'Fornecedor selecionado não foi encontrado. Continuando sem fornecedor.')
        
        produtos_criados = []
        movimentacoes_criadas = 0
        
        for produto_xml in produtos_xml:
            # Verifica se deve criar novo produto
            criar_novo = request.POST.get(f'criar_{produto_xml["codigo"]}') == 'on'
            
            # Busca ou cria produto
            produto_db = encontrar_produto_por_codigo(
                produto_xml['codigo'],
                produto_xml['ncm'],
                produto_xml['ean']
            )
            
            if not produto_db:
                if criar_novo:
                    # Cria novo produto
                    categoria_padrao = Category.objects.first()
                    if not categoria_padrao:
                        messages.error(request, 'É necessário criar pelo menos uma categoria primeiro!')
                        return redirect('estoque:entrada_xml')
                    
                    produto_db = Product.objects.create(
                        codigo=produto_xml['codigo'],
                        nome=produto_xml['nome'],
                        categoria=categoria_padrao,
                        unidade=produto_xml['unidade'],
                        ncm=produto_xml['ncm'] or '',
                        ean=produto_xml['ean'] or '',
                        quantidade_estoque=0,
                        custo_unitario=produto_xml['valor_unitario']
                    )
                    produtos_criados.append(produto_db.nome)
                else:
                    continue
            
            # Cria movimentação de entrada
            StockMovement.objects.create(
                tipo='ENTRADA',
                produto=produto_db,
                quantidade=produto_xml['quantidade'],
                custo_unitario=produto_xml['valor_unitario'],
                fornecedor=fornecedor,
                usuario=request.user,
                observacao='Entrada via XML de NF-e'
            )
            movimentacoes_criadas += 1
        
        # Limpa sessão
        request.session.pop('produtos_xml', None)
        request.session.pop('fornecedor_id', None)
        
        messages.success(
            request,
            f'{movimentacoes_criadas} entrada(s) registrada(s) com sucesso! '
            f'{len(produtos_criados)} novo(s) produto(s) criado(s).'
        )
        
        return redirect('estoque:entrada_xml')
    
    return redirect('estoque:entrada_xml')


# ============ SAÍDAS ============

@login_required
def saida_criar(request):
    """Criar saída de produtos"""
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False, user=request.user)
            movimentacao.save()
            messages.success(
                request,
                f'Saída de {movimentacao.quantidade} {movimentacao.produto.unidade} '
                f'de "{movimentacao.produto.nome}" registrada com sucesso!'
            )
            return redirect('estoque:saida_criar')
    else:
        form = SaidaForm()
    
    return render(request, 'estoque/saidas/form.html', {'form': form})


# ============ RELATÓRIOS ============

@login_required
def relatorio_index(request):
    """Página principal de relatórios"""
    # Período padrão: últimos 30 dias
    data_fim = timezone.now()
    data_inicio = data_fim - timedelta(days=30)
    
    # Filtros
    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')
    
    if data_inicio_str:
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        except:
            pass
    
    if data_fim_str:
        try:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
        except:
            pass
    
    # Movimentações no período
    movimentacoes = StockMovement.objects.filter(
        created_at__gte=data_inicio,
        created_at__lte=data_fim
    ).select_related('produto', 'usuario').order_by('-created_at')
    
    # Resumo
    entradas_total = movimentacoes.filter(tipo='ENTRADA').aggregate(
        total=Sum('quantidade')
    )['total'] or Decimal('0.00')
    
    saidas_total = movimentacoes.filter(tipo='SAIDA').aggregate(
        total=Sum('quantidade')
    )['total'] or Decimal('0.00')
    
    # Dados para gráfico (saídas por mês)
    movimentacoes_saidas = movimentacoes.filter(tipo='SAIDA')
    dados_grafico = {}
    
    for mov in movimentacoes_saidas:
        mes_ano = mov.created_at.strftime('%Y-%m')
        if mes_ano not in dados_grafico:
            dados_grafico[mes_ano] = {}
        
        produto_nome = mov.produto.nome
        if produto_nome not in dados_grafico[mes_ano]:
            dados_grafico[mes_ano][produto_nome] = Decimal('0.00')
        
        dados_grafico[mes_ano][produto_nome] += mov.quantidade
    
    # Prepara dados para Chart.js
    meses = sorted(dados_grafico.keys())
    produtos_unicos = set()
    for mes_data in dados_grafico.values():
        produtos_unicos.update(mes_data.keys())
    produtos_unicos = sorted(produtos_unicos)
    
    datasets = []
    cores = ['#36A2EB', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF']
    
    for idx, produto in enumerate(produtos_unicos[:10]):  # Limita a 10 produtos
        dados = [float(dados_grafico.get(mes, {}).get(produto, 0)) for mes in meses]
        datasets.append({
            'label': produto[:30],  # Limita tamanho do nome
            'data': dados,
            'backgroundColor': cores[idx % len(cores)],
        })
    
    # Exportação
    if request.GET.get('exportar') == 'xlsx':
        resumo = {
            'entradas': entradas_total,
            'saidas': saidas_total,
            'saldo_final': entradas_total - saidas_total,
        }
        return exportar_relatorio_para_xlsx(movimentacoes, resumo)
    
    context = {
        'movimentacoes': movimentacoes[:100],  # Limita exibição
        'entradas_total': entradas_total,
        'saidas_total': saidas_total,
        'saldo_final': entradas_total - saidas_total,
        'data_inicio': data_inicio.date(),
        'data_fim': data_fim.date(),
        'meses': mark_safe(json.dumps(meses)),
        'datasets': mark_safe(json.dumps(datasets)),
    }
    
    return render(request, 'estoque/relatorios/index.html', context)


# ============ API para AJAX ============

@login_required
def api_produto_estoque(request, produto_id):
    """API para retornar estoque atual de um produto"""
    produto = get_object_or_404(Product, pk=produto_id)
    return JsonResponse({
        'quantidade': float(produto.quantidade_estoque),
        'unidade': produto.get_unidade_display(),
    })


@login_required
def api_verificar_sku(request):
    """API para verificar se SKU já existe (validação em tempo real)"""
    sku = request.GET.get('sku', '').strip()
    produto_id = request.GET.get('produto_id', None)
    
    if not sku:
        return JsonResponse({'disponivel': True, 'mensagem': ''})
    
    # Verifica se existe produto com esse SKU
    query = Product.objects.filter(codigo=sku)
    
    # Se estiver editando, exclui o próprio produto da verificação
    if produto_id:
        try:
            query = query.exclude(pk=int(produto_id))
        except (ValueError, TypeError):
            pass
    
    existe = query.exists()
    
    return JsonResponse({
        'disponivel': not existe,
        'mensagem': 'Este SKU já está em uso' if existe else 'SKU disponível',
        'existe': existe
    })


# ============ PEDIDOS WHATSAPP ============

@login_required
def pedido_whatsapp(request):
    """Geração de pedidos para WhatsApp"""
    # Mostra todos os produtos, não apenas os com estoque > 0
    # pois o objetivo é fazer pedidos para reposição de estoque
    produtos = Product.objects.select_related('categoria').all().order_by('categoria__nome', 'nome')
    
    if request.method == 'POST':
        # Coleta os produtos selecionados com quantidades
        produtos_selecionados = []
        total = Decimal('0.00')
        
        for produto in produtos:
            quantidade_key = f'qtd_{produto.pk}'
            quantidade = request.POST.get(quantidade_key)
            
            if quantidade and float(quantidade) > 0:
                qtd = Decimal(quantidade)
                # Permite pedir qualquer quantidade, mesmo maior que o estoque
                # pois o objetivo é fazer pedidos para reposição de estoque
                valor_item = qtd * produto.custo_unitario
                produtos_selecionados.append({
                    'produto': produto,
                    'quantidade': qtd,
                    'valor_total': valor_item
                })
                total += valor_item
        
        if produtos_selecionados:
            # Formata mensagem para WhatsApp
            mensagem = "📋 *PEDIDO DE ESTOQUE*\n\n"
            mensagem += f"Data: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            mensagem += "*PRODUTOS:*\n\n"
            
            categoria_atual = None
            for item in produtos_selecionados:
                produto = item['produto']
                
                # Agrupa por categoria
                if produto.categoria.nome != categoria_atual:
                    categoria_atual = produto.categoria.nome
                    mensagem += f"\n*{categoria_atual}*\n"
                
                mensagem += f"• {produto.nome} ({produto.codigo})\n"
                mensagem += f"  Qtd: {item['quantidade']} {produto.get_unidade_display()}\n"
                mensagem += f"  R$ {item['valor_total']:.2f}\n\n"
            
            mensagem += f"━━━━━━━━━━━━━━━━\n"
            mensagem += f"*TOTAL: R$ {total:.2f}*\n"
            
            # Codifica a mensagem para URL do WhatsApp
            import urllib.parse
            mensagem_encoded = urllib.parse.quote(mensagem)
            
            # URL do WhatsApp Web/App
            whatsapp_url = f"https://wa.me/?text={mensagem_encoded}"
            
            # Calcula total de itens
            total_itens = sum(item['quantidade'] for item in produtos_selecionados)
            
            # Salva o pedido no banco de dados
            WhatsAppOrder.objects.create(
                usuario=request.user,
                mensagem=mensagem,
                valor_total=total,
                total_itens=total_itens
            )
            
            # Busca os últimos 10 pedidos gerados
            ultimos_pedidos = WhatsAppOrder.objects.select_related('usuario').order_by('-created_at')[:10]
            
            return render(request, 'estoque/pedidos/whatsapp.html', {
                'produtos_selecionados': produtos_selecionados,
                'total': total,
                'whatsapp_url': whatsapp_url,
                'mensagem': mensagem,
                'ultimos_pedidos': ultimos_pedidos,
            })
        else:
            messages.warning(request, 'Selecione pelo menos um produto com quantidade.')
    
    # Agrupa produtos por categoria
    produtos_por_categoria = {}
    for produto in produtos:
        cat_nome = produto.categoria.nome if produto.categoria else 'Sem Categoria'
        if cat_nome not in produtos_por_categoria:
            produtos_por_categoria[cat_nome] = []
        produtos_por_categoria[cat_nome].append(produto)
    
    # Busca os últimos 10 pedidos gerados
    ultimos_pedidos = WhatsAppOrder.objects.select_related('usuario').order_by('-created_at')[:10]
    
    return render(request, 'estoque/pedidos/whatsapp.html', {
        'produtos_por_categoria': produtos_por_categoria,
        'ultimos_pedidos': ultimos_pedidos,
    })
