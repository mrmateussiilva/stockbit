# ✅ Checklist de Deploy para Produção

Use este checklist antes e após o deploy para garantir que tudo está funcionando corretamente.

## 📋 Antes do Deploy

### Configuração Inicial
- [ ] Ler e entender o arquivo `DEPLOY.md`
- [ ] Servidor com Docker e Docker Compose instalados
- [ ] Portas 80, 8000 e 5432 disponíveis no servidor
- [ ] Domínio ou IP configurado e apontado para o servidor

### Arquivos de Configuração
- [ ] Criado arquivo `.env` baseado em `env.production.example`
- [ ] `SECRET_KEY` alterado para uma chave forte e única
- [ ] `DEBUG=False` configurado
- [ ] `ALLOWED_HOSTS` configurado com seus domínios
- [ ] `DB_PASSWORD` alterado para senha forte
- [ ] `CORS_ALLOWED_ORIGINS` configurado corretamente
- [ ] `VITE_API_URL` configurado corretamente

### Configurações de Segurança
- [ ] SSL/HTTPS configurado (opcional mas recomendado)
- [ ] `SECURE_SSL_REDIRECT=True` se usar HTTPS
- [ ] `CSRF_COOKIE_SECURE=True` se usar HTTPS
- [ ] `SESSION_COOKIE_SECURE=True` se usar HTTPS

## 🚀 Durante o Deploy

### Build e Inicialização
- [ ] Executado `./prod.sh build` ou `docker-compose -f docker-compose.prod.yml build`
- [ ] Executado `./prod.sh start` ou `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Verificado logs com `./prod.sh logs`
- [ ] Confirmado que todos os serviços estão rodando com `./prod.sh ps`

### Configuração do Banco de Dados
- [ ] Executado `./prod.sh migrate` para aplicar migrações
- [ ] Criado superusuário com `./prod.sh createsuperuser`
- [ ] Testado login no painel admin

## ✅ Após o Deploy

### Verificações de Funcionamento
- [ ] Frontend acessível e carregando corretamente
- [ ] Backend API respondendo (testar endpoint `/api/`)
- [ ] Login funcionando corretamente
- [ ] Todas as páginas principais funcionando
- [ ] CRUD de produtos funcionando
- [ ] CRUD de estoque funcionando
- [ ] Relatórios/dashboard funcionando
- [ ] Exportação de dados funcionando (se aplicável)

### Verificações de Segurança
- [ ] DEBUG=False em produção
- [ ] Arquivo `.env` não está no repositório git
- [ ] Senha do banco de dados forte
- [ ] Senhas de usuários fortes
- [ ] CORS configurado corretamente

### Verificações de Performance
- [ ] Assets estáticos carregando corretamente
- [ ] Compressão gzip ativa
- [ ] Cache funcionando corretamente
- [ ] Tempo de resposta adequado

### Monitoramento
- [ ] Logs não mostram erros críticos
- [ ] Uso de recursos do servidor adequado
- [ ] Backup automático configurado (opcional)

## 🔄 Manutenção Contínua

### Diário
- [ ] Verificar logs para erros
- [ ] Monitorar uso de recursos

### Semanal
- [ ] Verificar backups
- [ ] Revisar logs
- [ ] Verificar atualizações de segurança

### Mensal
- [ ] Fazer backup completo do banco de dados
- [ ] Revisar e atualizar dependências
- [ ] Testar restauração de backup
- [ ] Revisar logs de acesso

## 🚨 Procedimentos de Emergência

### Se algo der errado
1. Ver logs: `./prod.sh logs`
2. Verificar status: `./prod.sh ps`
3. Verificar recursos: `docker stats`
4. Backup antes de qualquer alteração: `./prod.sh backup`
5. Comunicar a equipe

### Rollback
```bash
# Parar serviços
./prod.sh stop

# Restaurar backup
cat backup.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U stockbit_user stockbit_db

# Reiniciar
./prod.sh start
```

## 📞 Contatos de Suporte

- Documentação: `DEPLOY.md`
- Logs do sistema: `./prod.sh logs`
- Status: `./prod.sh ps`

---

**Data do último deploy:** ___________
**Responsável:** ___________
**Observações:** ___________

