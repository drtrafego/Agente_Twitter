#!/bin/bash
echo "🚀 Iniciando Bot Railway..."
echo "📁 Arquivos disponíveis:"
ls -la
echo "🔍 Verificando bot_railway_optimized.py:"
if [ -f "bot_railway_optimized.py" ]; then
    echo "✅ Arquivo encontrado!"
else
    echo "❌ Arquivo não encontrado!"
    exit 1
fi
echo "🏃 Executando waitress..."
exec waitress-serve --host=0.0.0.0 --port=$PORT bot_railway_optimized:app