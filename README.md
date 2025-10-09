# 🤖 Bot Twitter X API v2

Bot automatizado para Twitter/X que monitora menções e comentários nos posts próprios, respondendo automaticamente com frases criativas do universo Web3/crypto.

## ✨ Funcionalidades

- 🎯 **Monitoramento de Menções**: Responde automaticamente a menções diretas
- 💬 **Monitoramento de Comentários**: Responde a comentários nos seus posts dos últimos 7 dias
- 🛡️ **Sistema Anti-Detecção**: Intervalos aleatórios de 2-4 minutos entre respostas
- 🎲 **Respostas Variadas**: 40 frases criativas selecionadas aleatoriamente
- 📊 **Métricas Detalhadas**: Monitoramento completo via endpoint `/status`
- ⚙️ **Deploy Railway**: Otimizado para produção

## 🚀 Deploy Rápido

1. **Clone o repositório**:
```bash
git clone https://github.com/drtrafego/Agente_Twitter.git
cd Agente_Twitter
```

2. **Configure as variáveis de ambiente** (veja `RAILWAY_VARS.md`)

3. **Deploy no Railway**:
   - Conecte seu repositório GitHub
   - Configure as variáveis de ambiente
   - Deploy automático ativado

## 📊 Status do Bot

Acesse `/status` para ver métricas em tempo real:
- Posts enviados hoje
- Posts próprios monitorados  
- Comentários encontrados
- Última atividade
- Status de execução

## 🎯 Respostas

O bot usa 40 frases criativas do universo Web3/crypto, como:
- "You don't need alpha, you need community. 💡"
- "Social capital > market cap. 🌍"
- "Community isn't bullish or bearish. It's timeless. ⏳"

## 📁 Estrutura do Projeto

```
├── bot_railway_optimized.py    # Bot principal
├── respostas.txt              # Frases de resposta
├── requirements.txt           # Dependências
├── Procfile                   # Configuração Railway
├── start.sh                   # Script de inicialização
├── railway.json              # Configuração específica
└── DOCUMENTACAO_COMPLETA.md   # Documentação detalhada
```

## 🔧 Configuração

Veja `RAILWAY_VARS.md` para lista completa de variáveis de ambiente necessárias.

## 📈 Versão Atual: v2.0

- ✅ Monitoramento de comentários nos posts próprios
- ✅ Sistema anti-detecção com intervalos aleatórios
- ✅ 40 respostas criativas Web3/crypto
- ✅ Métricas detalhadas
- ✅ Priorização inteligente (menções → comentários)

---

**Status**: 🟢 **TOTALMENTE FUNCIONAL**  
**Railway**: [Projeto Ativo](https://railway.com/project/d06d53cd-d87c-4548-aeac-02c85b1e4c10)  
**Desenvolvido com**: Python 3.11 + X API v2