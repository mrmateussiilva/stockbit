from django import forms
from .models import Product, Category, Supplier, StockMovement


class ProductForm(forms.ModelForm):
    """Formulário para cadastro/edição de produtos"""
    class Meta:
        model = Product
        fields = ['codigo', 'nome', 'categoria', 'unidade', 'quantidade_estoque', 
                  'custo_unitario', 'ncm', 'ean']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Deixe em branco para gerar automaticamente (PROD-0001)'
            }),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'unidade': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ncm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000000',
                'maxlength': '8'
            }),
            'ean': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '7891234567890',
                'maxlength': '13'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo código opcional
        self.fields['codigo'].required = False
        self.fields['codigo'].help_text = 'Deixe em branco para gerar automaticamente'


class CategoryForm(forms.ModelForm):
    """Formulário para cadastro/edição de categorias"""
    class Meta:
        model = Category
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    """Formulário para cadastro/edição de fornecedores"""
    class Meta:
        model = Supplier
        fields = ['nome', 'cnpj', 'telefone', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do fornecedor'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'maxlength': '18'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000 ou (00) 0000-0000',
                'maxlength': '15'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo do fornecedor'
            }),
        }
    
    def clean_cnpj(self):
        """Valida CNPJ"""
        cnpj = self.cleaned_data.get('cnpj')
        
        if cnpj:
            # Remove formatação
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            
            # Verifica se tem 14 dígitos
            if len(cnpj_limpo) != 14:
                raise forms.ValidationError('CNPJ deve ter 14 dígitos.')
            
            # Validação do algoritmo de CNPJ
            if not self._validar_cnpj(cnpj_limpo):
                raise forms.ValidationError('CNPJ inválido. Verifique os dígitos.')
            
            # Retorna formatado
            return cnpj
        
        return cnpj
    
    def clean_telefone(self):
        """Valida telefone"""
        telefone = self.cleaned_data.get('telefone')
        
        if telefone:
            # Remove formatação
            telefone_limpo = ''.join(filter(str.isdigit, telefone))
            
            # Verifica se tem 10 ou 11 dígitos (fixo ou celular)
            if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
                raise forms.ValidationError('Telefone inválido. Deve ter 10 ou 11 dígitos.')
        
        return telefone
    
    def clean_email(self):
        """Valida email"""
        email = self.cleaned_data.get('email')
        
        if email:
            # Validação básica do Django já faz, mas podemos adicionar validação customizada
            if '@' not in email or '.' not in email.split('@')[1]:
                raise forms.ValidationError('Email inválido.')
        
        return email
    
    @staticmethod
    def _validar_cnpj(cnpj):
        """Valida CNPJ usando algoritmo oficial"""
        # Elimina CNPJs conhecidos inválidos
        if len(set(cnpj)) == 1:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(posicoes):
            soma = sum(int(cnpj[i]) * posicoes[i] for i in range(len(posicoes)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Primeiro dígito verificador
        posicoes1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digito1 = calcular_digito(posicoes1)
        
        if int(cnpj[12]) != digito1:
            return False
        
        # Segundo dígito verificador
        posicoes2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digito2 = calcular_digito(posicoes2)
        
        if int(cnpj[13]) != digito2:
            return False
        
        return True


class EntradaManualForm(forms.ModelForm):
    """Formulário para entrada manual de produtos"""
    class Meta:
        model = StockMovement
        fields = ['produto', 'quantidade', 'custo_unitario', 'fornecedor', 'observacao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Product.objects.all().order_by('nome')
        self.fields['fornecedor'].required = False
        self.fields['observacao'].required = False

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.tipo = 'ENTRADA'
        if user:
            instance.usuario = user
        if commit:
            instance.save()
        return instance


class SaidaForm(forms.ModelForm):
    """Formulário para saída de produtos"""
    class Meta:
        model = StockMovement
        fields = ['produto', 'quantidade', 'observacao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Product.objects.filter(
            quantidade_estoque__gt=0
        ).order_by('nome')
        self.fields['observacao'].required = False

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        produto = self.cleaned_data.get('produto')
        
        if produto and quantidade:
            if quantidade > produto.quantidade_estoque:
                raise forms.ValidationError(
                    f'Quantidade solicitada ({quantidade}) excede o estoque disponível '
                    f'({produto.quantidade_estoque} {produto.unidade})'
                )
        return quantidade

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.tipo = 'SAIDA'
        if user:
            instance.usuario = user
        if commit:
            instance.save()
        return instance


class XMLUploadForm(forms.Form):
    """Formulário para upload de XML de NF-e"""
    arquivo_xml = forms.FileField(
        label='Arquivo XML da NF-e',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xml',
            'style': 'cursor: pointer;',
            'id': 'id_arquivo_xml'
        })
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Supplier.objects.all().order_by('nome'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Fornecedor'
    )
    
    def clean_arquivo_xml(self):
        """Valida se o arquivo é um XML válido"""
        arquivo = self.cleaned_data.get('arquivo_xml')
        
        if not arquivo:
            raise forms.ValidationError('Por favor, selecione um arquivo XML.')
        
        # Verifica extensão
        if not arquivo.name.lower().endswith('.xml'):
            raise forms.ValidationError('O arquivo deve ter extensão .xml')
        
        # Verifica tamanho (máximo 10MB)
        if arquivo.size > 10 * 1024 * 1024:
            raise forms.ValidationError('O arquivo é muito grande. Tamanho máximo: 10MB')
        
        # Tenta fazer um parse básico para verificar se é XML válido
        try:
            import xml.etree.ElementTree as ET
            
            # Salva posição atual
            pos_atual = arquivo.tell() if hasattr(arquivo, 'tell') else 0
            
            # Tenta ler e parsear
            if hasattr(arquivo, 'seek'):
                arquivo.seek(0)
            
            try:
                tree = ET.parse(arquivo)
                root = tree.getroot()
                # Verifica se parece ser uma NF-e
                if 'nfe' not in root.tag.lower() and 'nfe' not in str(root.tag).lower():
                    # Não é crítico, apenas avisa
                    pass
            except ET.ParseError:
                # Tenta ler como string
                if hasattr(arquivo, 'seek'):
                    arquivo.seek(0)
                content = arquivo.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
                ET.fromstring(content)
            
            # Restaura posição
            if hasattr(arquivo, 'seek'):
                arquivo.seek(pos_atual)
                
        except Exception as e:
            raise forms.ValidationError(f'O arquivo não parece ser um XML válido: {str(e)}')
        
        return arquivo

