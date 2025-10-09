# 🤖 Bot Twitter X API v2 - Documentação Completa

## 📋 Resumo do Projeto
Bot automatizado para Twitter/X que monitora menções e comentários, respondendo automaticamente com frases criativas do universo Web3/crypto.

## 🚀 Funcionalidades Implementadas

### 1. **Monitoramento de Menções** ✅
- Busca menções diretas (@drtrafeg0) em tempo real
- Filtra retweets para evitar spam
- Resposta automática com frases aleatórias
- Rate limit respeitado (429 handling)

### 2. **Monitoramento de Comentários nos Posts Próprios** ✅ **NOVO**
- Busca posts próprios dos últimos 7 dias automaticamente
- Monitora replies/comentários usando `conversation_id`
- Atualiza lista de posts monitorados a cada hora
- Evita auto-resposta e duplicação de replies
- Filtra apenas comentários de outros usuários

### 3. **Sistema Anti-Detecção Avançado** ✅ **NOVO**
- **Intervalos aleatórios**: 2-4 minutos entre cada resposta
- **Respostas variadas**: 40 frases diferentes selecionadas aleatoriamente
- **Priorização inteligente**: Menções primeiro, depois comentários
- **Limite diário**: Máximo 17 posts por dia (reset automático)

### 4. **Autenticação Robusta** ✅
- OAuth 1.0a para criação de tweets
- Bearer Token para busca e leitura
- Validação completa de credenciais na inicialização
- Headers OAuth gerados dinamicamente

### 5. **Deploy Railway Otimizado** ✅
- Configuração específica para produção
- Logging apenas para console (sem arquivos)
- Health check endpoints (`/` e `/status`)
- Inicialização automática em thread separada
- Tratamento de erros robusto

## 📊 Métricas e Monitoramento

### Endpoint `/status` retorna:
```json
{
  "status": "healthy",
  "bot_running": true,
  "daily_limit": 17,
  "daily_posts": 5,
  "last_activity": "2025-01-09T18:00:00",
  "monitored_posts": 8,
  "replies_found": 12,
  "timestamp": "2025-01-09T18:05:00",
  "error": null
}
```

### Métricas Disponíveis:
- `daily_posts`: Posts enviados hoje
- `monitored_posts`: Posts próprios sendo monitorados
- `replies_found`: Comentários encontrados no último ciclo
- `last_activity`: Timestamp da última atividade
- `bot_running`: Status de execução

## 🎯 Respostas Criativas (40 frases)

O bot usa frases alinhadas com Web3/crypto:
- "You don't need alpha, you need community. 💡"
- "Forget charts, remember friends. 📊➡️👯"
- "RTs are the real DeFi yields. 📈🔁"
- "Social capital > market cap. 🌍"
- "Community isn't bullish or bearish. It's timeless. ⏳"
- [... e mais 35 frases criativas]

## ⚙️ Configuração Técnica

### Variáveis de Ambiente Obrigatórias:
```
API_KEY=sua_api_key
API_KEY_SECRET=sua_api_key_secret
ACCESS_TOKEN=seu_access_token
ACCESS_TOKEN_SECRET=seu_access_token_secret
BEARER_TOKEN=seu_bearer_token
BOT_USERNAME=drtrafeg0
```

### Arquivos de Configuração:
- `Procfile`: `web: ./start.sh`
- `railway.json`: Configuração específica Railway
- `start.sh`: Script de inicialização com validação
- `requirements.txt`: Dependências Python
- `runtime.txt`: Versão Python (3.11.0)

## 🔄 Fluxo de Operação

### Ciclo Principal (5 minutos):
1. **Reset Diário**: Zera contador se mudou o dia
2. **Processar Menções**: Prioridade máxima
3. **Processar Comentários**: Se ainda há limite disponível
4. **Atualizar Métricas**: Status global atualizado
5. **Aguardar**: 5 minutos até próximo ciclo

### Lógica de Resposta:
1. Busca menções/comentários
2. Filtra duplicados e auto-menções
3. Seleciona resposta aleatória
4. Envia resposta como reply
5. Aguarda intervalo aleatório (2-4 min)
6. Atualiza contadores e métricas

## 🛡️ Tratamento de Erros

### Rate Limiting:
- Status 429: Aguarda e continua
- Logs informativos sem parar execução

### Autenticação:
- Validação na inicialização
- Falha crítica para execução

### Conectividade:
- Timeout de 30s em todas as requests
- Retry automático no próximo ciclo

## 📈 Histórico de Versões

### v1.0 - Bot Básico
- Monitoramento de menções
- Resposta simples
- Deploy Railway

### v2.0 - Funcionalidades Avançadas ✅ **ATUAL**
- Monitoramento de comentários nos posts próprios
- Sistema anti-detecção com intervalos aleatórios
- 40 respostas criativas Web3/crypto
- Métricas detalhadas
- Priorização inteligente

## 🔗 Links Importantes

- **Railway Project**: https://railway.com/project/d06d53cd-d87c-4548-aeac-02c85b1e4c10
- **GitHub Repository**: https://github.com/drtrafego/Agente_Twitter
- **X API Documentation**: https://developer.x.com/en/docs/x-api

## 🎯 Próximas Funcionalidades Planejadas

### Sistema de Postagens Agendadas (Em Estudo):
- Arquivo com posts programados
- Data/hora específica para cada post
- Verificação automática de horários
- Postagem automática no momento certo
- Formato: `YYYY-MM-DD HH:MM | Texto do post`

---

**Status**: ✅ **TOTALMENTE FUNCIONAL**  
**Última Atualização**: 09/01/2025  
**Desenvolvido por**: Trae AI Assistant