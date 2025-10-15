# 🚀 Variáveis de Ambiente para Railway

## ✅ Configuração Correta das Variáveis

### 📋 Copie e cole estas variáveis EXATAS no Railway:

```
API_KEY=yGFJh4FzhOzzVxXLUUMKVu8R9
API_KEY_SECRET=gMedEvioYsIdtZEwb6FEML26gx28IvjPwddTNhD7Dk1CFC6D5f
ACCESS_TOKEN=1520208237672472577-CGVJwlhaDKhQEbX78U81B3UxtwYJ5a
ACCESS_TOKEN_SECRET=3eWYhSBIO68ujHfbbUkIUQudRxoORjCci4BxlcoXRoFOq
BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAFmX4gEAAAAAAtV26F1B8P5Qu%2FFn6ZdUh8Ruf1M%3Dv03UdfeeNfkpwV18c49dl5YH1i0rzItlU5wkMKQQcShWyfjRXD
BOT_USERNAME=drtrafeg0
MAX_COMMENTS_PER_CYCLE=2
COMMENT_INTERVAL_SEC=120
# (Opcional) IDs de posts próprios para monitorar comentários sem chamar API
# Use IDs dos tweets raiz (conversation_id). Separe por vírgula.
# Exemplo: MONITORED_POST_IDS=1869723456789012345,1869123456789012345
MONITORED_POST_IDS=
```

### 🔧 Como Configurar no Railway:

1. **Acesse seu projeto no Railway**
2. **Vá para a aba "Variables"**
3. **Delete todas as variáveis antigas/incorretas**
4. **Adicione uma por uma as variáveis acima**
5. **Clique em "Deploy" para aplicar**

### ⚠️ IMPORTANTE:
- **NÃO adicione aspas** nas variáveis do Railway
- **Copie exatamente** como mostrado acima
- **Verifique se não há espaços extras**
- **O BEARER_TOKEN tem caracteres especiais (%2F) - copie exato**

### 🧪 Teste após Deploy:
- Acesse: `https://agente-twitter.up.railway.app/`
- Deve retornar: `{"status":"healthy","bot_running":true}`
- Status endpoint: `https://agente-twitter.up.railway.app/status`

### 📝 Variáveis Opcionais:
```
DATABASE_URL=postgresql://neondb_owner:npg_NEjkh7WQaBl4@ep-winter-tooth-adj61kyi-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```
(Só adicione se for usar banco de dados)

---
**✅ Com essas variáveis corretas, o bot deve funcionar perfeitamente no Railway!**