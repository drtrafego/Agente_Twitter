# Configuração Railway - Bot X API v2 Híbrido Oficial

## ✅ SOLUÇÃO DEFINITIVA BASEADA NA DOCUMENTAÇÃO OFICIAL

Este bot foi desenvolvido seguindo rigorosamente a documentação oficial do X API v2 e resolve todos os problemas de autenticação identificados.

## 🔧 Variáveis de Ambiente (Railway)

Configure estas variáveis exatamente como estão no arquivo `.env`:

```
API_KEY=yGFJh4FzhOzzVxXLUUMKVu8R9
API_KEY_SECRET=gMedEvioYsIdtZEwb6FEML26gx28IvjPwddTNhD7Dk1CFC6D5f
ACCESS_TOKEN=1520208237672472577-CGVJwlhaDKhQEbX78U81B3UxtwYJ5a
ACCESS_TOKEN_SECRET=3eWYhSBIO68ujHfbbUkIUQudRxoORjCci4BxlcoXRoFOq
BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAFmX4gEAAAAAAtV26F1B8P5Qu%2FFn6ZdUh8Ruf1M%3Dv03UdfeeNfkpwV18c49dl5YH1i0rzItlU5wkMKQQcShWyfjRXD
BOT_USERNAME=drtrafeg0
```

## 🚀 Método de Autenticação HÍBRIDO

**SOLUÇÃO DEFINITIVA**: O bot usa autenticação híbrida conforme documentação oficial:

- **OAuth 1.0a User Context**: Para endpoints que exigem contexto de usuário (`/2/users/me`, `/2/tweets`)
- **Bearer Token App-Only**: Para endpoints que permitem contexto de aplicação (`/2/tweets/search/recent`)

## 📊 Limitações do Free Tier (Documentação Oficial)

- **Posts**: 17 por 24 horas (por usuário E por app)
- **Leitura**: 500 posts por mês
- **Rate Limits**: Respeitados automaticamente pelo bot

## 🎯 Funcionalidades Confirmadas

✅ **Autenticação**: OAuth 1.0a + Bearer Token híbrido  
✅ **Busca de Menções**: Funciona com Bearer Token  
✅ **Criação de Tweets**: Funciona com OAuth 1.0a  
✅ **Respostas Automáticas**: Palavras-chave inteligentes  
✅ **Rate Limiting**: Respeita limites do Free Tier  
✅ **Anti-Duplicação**: Cache de menções processadas  
✅ **Logging**: Completo para debugging  

## 📁 Arquivos para Deploy

- `bot_hibrido_oficial.py` - Bot principal (TESTADO E FUNCIONANDO)
- `requirements.txt` - Dependências mínimas
- `Procfile` - Configuração Railway
- `.env` - Variáveis de ambiente (não fazer push)

## 🔄 Passos para Deploy

1. **Push para GitHub**:
   ```bash
   git add .
   git commit -m "Bot X API v2 híbrido oficial - Solução definitiva"
   git push origin main
   ```

2. **Conectar Railway**:
   - Conectar repositório GitHub
   - Configurar variáveis de ambiente
   - Deploy automático

3. **Verificar Deploy**:
   - Logs devem mostrar: "Autenticado como @drtrafeg0"
   - Bot deve processar menções automaticamente

## 🧪 Como Testar

Mencione `@drtrafeg0` no X com palavras-chave:
- "oi" ou "hello" - Saudação
- "ajuda" ou "help" - Oferece ajuda
- "bot" - Confirma que é um bot
- Qualquer outra palavra - Resposta padrão amigável

## ⚠️ Notas Importantes

1. **Autenticação Híbrida**: Solução baseada na documentação oficial
2. **Free Tier**: Limite de 17 posts/24h é respeitado automaticamente
3. **Encoding**: Logs sem emojis para compatibilidade Windows
4. **Rate Limiting**: Implementado conforme especificações oficiais

## 🎉 Status

**✅ PROBLEMA 100% RESOLVIDO**

- Credenciais funcionando
- Bot testado e operacional
- Documentação completa
- Pronto para produção no Railway