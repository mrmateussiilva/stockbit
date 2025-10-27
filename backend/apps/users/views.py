from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    """View customizada para login com JWT"""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    """Registro de novos usuários"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Perfil do usuário logado"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Atualizar perfil do usuário"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout do usuário"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def forgot_password(request):
    """Solicitar recuperação de senha"""
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email é obrigatório'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        # Em produção, enviaria email com token aqui
        # Por enquanto, apenas retorna mensagem de sucesso
        return Response({
            'message': 'Email de recuperação enviado com sucesso',
            'note': 'Em produção, um email seria enviado com instruções'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # Por segurança, retorna mensagem genérica
        return Response({
            'message': 'Se o email existir, você receberá instruções'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def reset_password(request):
    """Resetar senha com token"""
    email = request.data.get('email')
    new_password = request.data.get('new_password')
    token = request.data.get('token')  # Em produção, validaria o token
    
    if not email or not new_password:
        return Response(
            {'error': 'Email e nova senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Senha alterada com sucesso'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuário não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Trocar senha (usuário logado)"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {'error': 'Senha antiga e nova senha são obrigatórias'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    
    if not user.check_password(old_password):
        return Response(
            {'error': 'Senha antiga incorreta'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    return Response({
        'message': 'Senha alterada com sucesso'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def verify_email(request):
    """Verificar email"""
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response(
            {'error': 'Email e código são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        # Em produção, validaria o código
        user.is_active = True
        user.save()
        
        return Response({
            'message': 'Email verificado com sucesso'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuário não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

