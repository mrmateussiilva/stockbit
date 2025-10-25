from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuários"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para JWT com email"""
    
    def validate(self, attrs):
        # Permite login com email ou username
        username = attrs.get('username')
        password = attrs.get('password')
        
        print(f"DEBUG: Tentativa de login com username: {username}")
        
        if not username or not password:
            raise serializers.ValidationError('Username e senha são obrigatórios.')
        
        # Tenta encontrar o usuário por email ou username
        user_obj = None
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
            print(f"DEBUG: Usuário encontrado por email: {username}")
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(username=username)
                print(f"DEBUG: Usuário encontrado por username: {username}")
            except User.DoesNotExist:
                print(f"DEBUG: Usuário não encontrado: {username}")
                raise serializers.ValidationError('Credenciais inválidas.')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            print(f"DEBUG: Falha na autenticação para: {username}")
            raise serializers.ValidationError('Credenciais inválidas.')
        
        if not user.is_active:
            print(f"DEBUG: Usuário inativo: {username}")
            raise serializers.ValidationError('Usuário inativo.')
        
        print(f"DEBUG: Login bem-sucedido para: {username}")
        refresh = self.get_token(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }

