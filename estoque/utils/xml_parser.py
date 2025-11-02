"""
Utilitário para parsing de XML de Nota Fiscal Eletrônica (NF-e)
Extrai informações dos produtos contidos no XML
"""
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from decimal import Decimal


def parse_nfe_xml(xml_file) -> List[Dict]:
    """
    Faz o parsing de um arquivo XML de NF-e e retorna uma lista de produtos encontrados.
    
    Args:
        xml_file: Arquivo XML carregado
        
    Returns:
        Lista de dicionários com informações dos produtos:
        [{
            'codigo': str,
            'nome': str,
            'ncm': str,
            'ean': str,
            'quantidade': Decimal,
            'valor_unitario': Decimal,
            'unidade': str
        }, ...]
    """
    produtos = []
    
    try:
        # Parse do XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Namespaces comuns em NF-e
        namespaces = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe',
            'default': 'http://www.portalfiscal.inf.br/nfe'
        }
        
        # Tenta encontrar os itens da nota fiscal
        # Versão 3.10 e 4.00 do schema
        itens = root.findall('.//{http://www.portalfiscal.inf.br/nfe}det')
        if not itens:
            # Tenta sem namespace
            itens = root.findall('.//det')
        
        for item in itens:
            try:
                # Informações do produto
                prod = item.find('.//prod')
                if prod is None:
                    # Tenta sem namespace
                    prod = item.find('prod')
                
                if prod is None:
                    continue
                
                # Extrai informações
                nome = prod.find('xProd')
                if nome is not None:
                    nome = nome.text or ''
                else:
                    nome = ''
                
                codigo = prod.find('cProd')
                if codigo is not None:
                    codigo = codigo.text or ''
                else:
                    codigo = nome[:20]  # Usa parte do nome como código
                
                ncm = prod.find('NCM')
                if ncm is not None:
                    ncm = ncm.text or ''
                else:
                    ncm = ''
                
                ean = prod.find('cEAN')
                if ean is not None:
                    ean = ean.text or ''
                else:
                    # Tenta código de barras
                    ean = prod.find('cBarra')
                    if ean is not None:
                        ean = ean.text or ''
                    else:
                        ean = ''
                
                quantidade = prod.find('qCom')
                if quantidade is not None and quantidade.text:
                    quantidade = Decimal(quantidade.text)
                else:
                    quantidade = Decimal('1.00')
                
                valor_unitario = prod.find('vUnCom')
                if valor_unitario is not None and valor_unitario.text:
                    valor_unitario = Decimal(valor_unitario.text)
                else:
                    # Tenta calcular pela quantidade total
                    valor_total = prod.find('vProd')
                    if valor_total is not None and valor_total.text:
                        valor_total = Decimal(valor_total.text)
                        valor_unitario = valor_total / quantidade
                    else:
                        valor_unitario = Decimal('0.00')
                
                unidade = prod.find('uCom')
                if unidade is not None:
                    unidade = unidade.text or 'UN'
                else:
                    unidade = 'UN'
                
                # Normaliza unidade para os valores esperados
                unidade_map = {
                    'UN': 'UN',
                    'UNID': 'UN',
                    'CX': 'CX',
                    'CAIXA': 'CX',
                    'KG': 'KG',
                    'QUILO': 'KG',
                    'LT': 'LT',
                    'LITRO': 'LT',
                    'MT': 'MT',
                    'METRO': 'MT',
                    'PC': 'PC',
                    'PEÇA': 'PC',
                }
                unidade = unidade_map.get(unidade.upper(), 'UN')
                
                produtos.append({
                    'codigo': codigo.strip(),
                    'nome': nome.strip(),
                    'ncm': ncm.strip(),
                    'ean': ean.strip(),
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'unidade': unidade,
                })
                
            except Exception as e:
                # Continua processando outros itens mesmo se um der erro
                print(f"Erro ao processar item: {e}")
                continue
        
        return produtos
        
    except ET.ParseError as e:
        raise ValueError(f"Erro ao fazer parse do XML: {e}")
    except Exception as e:
        raise ValueError(f"Erro ao processar arquivo XML: {e}")


def encontrar_produto_por_codigo(codigo: str, ncm: str = '', ean: str = ''):
    """
    Tenta encontrar um produto no banco de dados usando código, NCM ou EAN.
    """
    from estoque.models import Product
    
    # Tenta por código
    produto = Product.objects.filter(codigo=codigo).first()
    if produto:
        return produto
    
    # Tenta por EAN
    if ean:
        produto = Product.objects.filter(ean=ean).first()
        if produto:
            return produto
    
    # Tenta por NCM
    if ncm:
        produto = Product.objects.filter(ncm=ncm).first()
        if produto:
            return produto
    
    return None

