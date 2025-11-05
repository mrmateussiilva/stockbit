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
        xml_file: Arquivo XML carregado (pode ser objeto de arquivo do Django ou caminho)
        
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
        # Tenta ler o arquivo de diferentes formas
        # Se for um arquivo do Django, pode precisar ser lido como texto
        try:
            # Tenta fazer parse direto
            if hasattr(xml_file, 'seek'):
                xml_file.seek(0)  # Garante que está no início
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except (AttributeError, TypeError, OSError):
            # Se não funcionar, tenta ler como texto
            if hasattr(xml_file, 'seek'):
                xml_file.seek(0)
            xml_content = xml_file.read()
            if isinstance(xml_content, bytes):
                # Tenta diferentes codificações
                try:
                    xml_content = xml_content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        xml_content = xml_content.decode('latin-1')
                    except UnicodeDecodeError:
                        xml_content = xml_content.decode('utf-8', errors='ignore')
            root = ET.fromstring(xml_content)
        
        # Detecta namespace automaticamente
        # Extrai namespace do root se existir
        ns = {}
        if root.tag.startswith('{'):
            ns['nfe'] = root.tag[1:root.tag.index('}')]
        else:
            # Tenta namespaces comuns
            ns['nfe'] = 'http://www.portalfiscal.inf.br/nfe'
        
        # Namespaces comuns em NF-e (versões diferentes)
        namespaces_tentativas = [
            'http://www.portalfiscal.inf.br/nfe',
            'http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4',
            '',  # Sem namespace
        ]
        
        # Tenta encontrar os itens da nota fiscal
        # Versão 3.10 e 4.00 do schema
        itens = []
        for ns_url in namespaces_tentativas:
            if ns_url:
                itens = root.findall(f'.//{{{ns_url}}}det')
            else:
                itens = root.findall('.//det')
            
            if itens:
                break
        
        # Se ainda não encontrou, tenta buscar de forma mais genérica
        if not itens:
            # Busca qualquer elemento 'det' em qualquer nível
            for elem in root.iter():
                if elem.tag.endswith('}det') or elem.tag == 'det':
                    itens.append(elem)
                    break
            # Se ainda não encontrou, tenta buscar todos os elementos 'det'
            if not itens:
                itens = [elem for elem in root.iter() if 'det' in elem.tag.lower()]
        
        for item in itens:
            try:
                # Informações do produto - tenta diferentes formas de encontrar
                prod = None
                
                # Tenta com diferentes namespaces
                for ns_url in namespaces_tentativas:
                    if ns_url:
                        prod = item.find(f'.//{{{ns_url}}}prod')
                    else:
                        prod = item.find('.//prod')
                    
                    if prod is None:
                        # Tenta sem o ponto no início
                        if ns_url:
                            prod = item.find(f'{{{ns_url}}}prod')
                        else:
                            prod = item.find('prod')
                    
                    if prod is not None:
                        break
                
                # Se ainda não encontrou, busca em todos os filhos
                if prod is None:
                    for child in item.iter():
                        if child.tag.endswith('}prod') or child.tag == 'prod':
                            prod = child
                            break
                
                if prod is None:
                    continue
                
                # Função auxiliar para buscar elementos com diferentes namespaces
                def find_element(parent, tag_name):
                    """Busca elemento tentando diferentes namespaces"""
                    for ns_url in namespaces_tentativas:
                        if ns_url:
                            elem = parent.find(f'{{{ns_url}}}{tag_name}')
                        else:
                            elem = parent.find(tag_name)
                        if elem is not None:
                            return elem
                    # Busca em todos os filhos
                    for child in parent.iter():
                        if child.tag.endswith(f'}}{tag_name}') or child.tag == tag_name:
                            return child
                    return None
                
                # Extrai informações
                nome_elem = find_element(prod, 'xProd')
                nome = nome_elem.text.strip() if nome_elem is not None and nome_elem.text else ''
                
                if not nome:
                    continue  # Produto sem nome não é válido
                
                codigo_elem = find_element(prod, 'cProd')
                codigo = codigo_elem.text.strip() if codigo_elem is not None and codigo_elem.text else ''
                if not codigo:
                    codigo = nome[:20] if len(nome) > 20 else nome  # Usa parte do nome como código
                
                ncm_elem = find_element(prod, 'NCM')
                ncm = ncm_elem.text.strip() if ncm_elem is not None and ncm_elem.text else ''
                
                ean_elem = find_element(prod, 'cEAN')
                ean = ean_elem.text.strip() if ean_elem is not None and ean_elem.text else ''
                if not ean:
                    # Tenta código de barras
                    ean_elem = find_element(prod, 'cBarra')
                    ean = ean_elem.text.strip() if ean_elem is not None and ean_elem.text else ''
                
                quantidade_elem = find_element(prod, 'qCom')
                if quantidade_elem is not None and quantidade_elem.text:
                    try:
                        quantidade = Decimal(quantidade_elem.text.strip())
                    except:
                        quantidade = Decimal('1.00')
                else:
                    quantidade = Decimal('1.00')
                
                valor_unitario_elem = find_element(prod, 'vUnCom')
                if valor_unitario_elem is not None and valor_unitario_elem.text:
                    try:
                        valor_unitario = Decimal(valor_unitario_elem.text.strip())
                    except:
                        valor_unitario = Decimal('0.00')
                else:
                    # Tenta calcular pela quantidade total
                    valor_total_elem = find_element(prod, 'vProd')
                    if valor_total_elem is not None and valor_total_elem.text:
                        try:
                            valor_total = Decimal(valor_total_elem.text.strip())
                            valor_unitario = valor_total / quantidade if quantidade > 0 else Decimal('0.00')
                        except:
                            valor_unitario = Decimal('0.00')
                    else:
                        valor_unitario = Decimal('0.00')
                
                unidade_elem = find_element(prod, 'uCom')
                unidade = unidade_elem.text.strip() if unidade_elem is not None and unidade_elem.text else 'UN'
                
                # Normaliza unidade para os valores esperados
                unidade_map = {
                    'UN': 'UN',
                    'UNID': 'UN',
                    'UNIDADE': 'UN',
                    'CX': 'CX',
                    'CAIXA': 'CX',
                    'KG': 'KG',
                    'QUILO': 'KG',
                    'QUILOGRAM': 'KG',
                    'LT': 'LT',
                    'LITRO': 'LT',
                    'MT': 'MT',
                    'METRO': 'MT',
                    'PC': 'PC',
                    'PEÇA': 'PC',
                }
                unidade_normalizada = unidade_map.get(unidade.upper() if unidade else 'UN', 'UN')
                
                produtos.append({
                    'codigo': codigo.strip() if codigo else f'PROD-{len(produtos) + 1}',
                    'nome': nome.strip(),
                    'ncm': ncm.strip() if ncm else '',
                    'ean': ean.strip() if ean else '',
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'unidade': unidade_normalizada,
                })
                
            except Exception as e:
                # Continua processando outros itens mesmo se um der erro
                print(f"Erro ao processar item: {e}")
                continue
        
        return produtos
        
    except ET.ParseError as e:
        raise ValueError(f"Erro ao fazer parse do XML. Verifique se o arquivo é um XML válido de NF-e: {str(e)}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Erro ao decodificar o arquivo XML. Certifique-se de que o arquivo está em UTF-8: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erro ao processar arquivo XML: {str(e)}")


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

