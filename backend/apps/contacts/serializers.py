from rest_framework import serializers
from .models import Client, Supplier


class ClientSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Client"""
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'type', 'cpf_cnpj', 'email', 'phone', 'cellphone',
            'address', 'city', 'state', 'zip_code', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_cpf_cnpj(self, value):
        """Validação personalizada para CPF/CNPJ"""
        if not value:
            return value
        
        # Remove formatação para validação
        clean_value = value.replace('.', '').replace('-', '').replace('/', '')
        
        if len(clean_value) == 11:  # CPF
            if not self._validate_cpf(clean_value):
                raise serializers.ValidationError('CPF inválido')
        elif len(clean_value) == 14:  # CNPJ
            if not self._validate_cnpj(clean_value):
                raise serializers.ValidationError('CNPJ inválido')
        else:
            raise serializers.ValidationError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos')
        
        return value
    
    def _validate_cpf(self, cpf):
        """Validação de CPF"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Cálculo do primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Cálculo do segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cpf[9]) == digit1 and int(cpf[10]) == digit2
    
    def _validate_cnpj(self, cnpj):
        """Validação de CNPJ"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Cálculo do primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Cálculo do segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Supplier"""
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'type', 'cpf_cnpj', 'email', 'phone', 'cellphone',
            'address', 'city', 'state', 'zip_code', 'contact_person',
            'payment_terms', 'delivery_time', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_cpf_cnpj(self, value):
        """Validação personalizada para CPF/CNPJ"""
        if not value:
            return value
        
        # Remove formatação para validação
        clean_value = value.replace('.', '').replace('-', '').replace('/', '')
        
        if len(clean_value) == 11:  # CPF
            if not self._validate_cpf(clean_value):
                raise serializers.ValidationError('CPF inválido')
        elif len(clean_value) == 14:  # CNPJ
            if not self._validate_cnpj(clean_value):
                raise serializers.ValidationError('CNPJ inválido')
        else:
            raise serializers.ValidationError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos')
        
        return value
    
    def _validate_cpf(self, cpf):
        """Validação de CPF"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Cálculo do primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Cálculo do segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cpf[9]) == digit1 and int(cpf[10]) == digit2
    
    def _validate_cnpj(self, cnpj):
        """Validação de CNPJ"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Cálculo do primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Cálculo do segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2

