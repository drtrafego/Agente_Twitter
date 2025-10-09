# 🚨 Railway Deploy Debug Guide

## 📋 Checklist para Verificar Deploy Quebrado

### 1. 🔍 Verificar Status do Deploy
1. Acesse o [Railway Dashboard](https://railway.app/dashboard)
2. Vá para o seu projeto "Agente Twitter"
3. Verifique se o último deploy foi bem-sucedido
4. Procure por erros nos logs de build

### 2. 📊 Verificar Logs
```bash
# No Railway Dashboard:
1. Clique na aba "Deployments"
2. Clique no último deployment
3. Verifique os logs de build e runtime
4. Procure por erros em vermelho
```

### 3. 🔧 Verificar Variáveis de Ambiente
Confirme se estas variáveis estão configuradas no Railway:

```
API_KEY=sua_api_key_aqui
API_KEY_SECRET=sua_api_secret_aqui
ACCESS_TOKEN=seu_access_token_aqui
ACCESS_TOKEN_SECRET=seu_access_token_secret_aqui
BEARER_TOKEN=seu_bearer_token_aqui
BOT_USERNAME=drtrafeg0
CLIENT_ID=seu_client_id_aqui
CLIENT_SECRET=seu_client_secret_aqui
DATABASE_URL=postgresql://neondb_owner:npg_NEjkh7WQaBl4@ep-winter-tooth-adj61kyi-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 4. 🌐 Obter URL Correta
1. No Railway Dashboard, vá para a aba "Settings"
2. Procure por "Domains" ou "Public URL"
3. Copie a URL gerada (algo como: `https://seu-app-production-xxxx.up.railway.app`)

### 5. 🧪 Testar URL
Depois de obter a URL correta, teste:
```bash
curl https://sua-url-railway.up.railway.app/
```

## 🔧 Possíveis Problemas e Soluções

### ❌ Build Failed
- **Causa**: Erro no requirements.txt ou código
- **Solução**: Verificar logs de build, corrigir erros

### ❌ Runtime Error
- **Causa**: Variáveis de ambiente incorretas
- **Solução**: Verificar e corrigir variáveis no Railway

### ❌ Port Binding Error
- **Causa**: App não está usando a variável $PORT
- **Solução**: Já corrigido no código atual

### ❌ Timeout na Inicialização
- **Causa**: Bot demora para inicializar
- **Solução**: Já implementado com waitress

## 📞 Próximos Passos

1. **Verifique o Railway Dashboard** e me informe:
   - Status do último deploy (sucesso/falha)
   - URL pública do seu app
   - Mensagens de erro nos logs

2. **Teste a URL** que você encontrar:
   ```bash
   curl https://sua-url-railway.up.railway.app/
   ```

3. **Compartilhe os resultados** para que eu possa ajudar com a correção específica.

## 🆘 Se Tudo Falhar

Se o deploy continuar quebrado, podemos:
1. Fazer um redeploy manual
2. Verificar se o Railway está com problemas
3. Migrar para outra plataforma (Render, Heroku, etc.)

---
*Última atualização: 2025-10-08*