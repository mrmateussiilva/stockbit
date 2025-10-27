#!/usr/bin/env python
"""
Script para criar usuário admin no Django
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_api.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin_user():
    username = 'finderbit'
    email = 'admin@finderbit.com.br'
    password = 'finderbit3010'
    
    if User.objects.filter(username=username).exists():
        print(f'✅ Usuário "{username}" já existe!')
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Usuário admin criado com sucesso!')
        print(f'   Username: {username}')
        print(f'   Password: {password}')
        print(f'   Email: {email}')

if __name__ == '__main__':
    create_admin_user()

