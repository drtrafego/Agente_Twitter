## Plano de Trabalho: Robô do X (Twitter)

Este documento descreve o plano de desenvolvimento para o robô do X, com foco em uma arquitetura online usando Neon e Railway.

### Fase 1: Resposta automática a menções e comentários

**Metas:**
- Autenticar-se com segurança na API do X.
- Ouvir em tempo real as menções e salvá-las em um banco de dados Neon (PostgreSQL).
- Processar a fila de respostas de forma assíncrona.
- Fazer o deploy do bot na plataforma Railway para operação 24/7.

**Etapas:**
1.  **Configuração da Arquitetura Online:**
    - [x] Adaptar o projeto para usar um banco de dados PostgreSQL (Neon).
    - [x] Adicionar as dependências necessárias (`psycopg2-binary`, `python-dotenv`).
    - [x] Criar um `Procfile` para o deploy no Railway.
    - [ ] Configurar variáveis de ambiente para as credenciais (Twitter e Neon).
2.  **Lógica de Negócio:**
    - [x] Implementar a lógica de autenticação no bot.
    - [x] Implementar a escuta de menções e salvá-las no banco de dados.
    - [x] Criar a função para enviar respostas, lendo de `respostas.txt`.
    - [x] Implementar o worker que processa a fila do banco de dados com o delay de 2-4 minutos.
3.  **Deploy e Testes:**
    - [ ] Criar um projeto no Railway e um banco de dados no Neon.
    - [ ] Configurar as variáveis de ambiente no Railway.
    - [ ] Fazer o deploy da aplicação.
    - [ ] Realizar testes em produção para validar o fluxo completo.

### Fase 2: Postagem de conteúdo a partir de um arquivo

**Metas:**
- Ler um arquivo de texto com o conteúdo a ser postado.
- Agendar postagens em intervalos definidos.
- Publicar o conteúdo como novos tweets.

**Etapas:**
1.  **Leitura de Arquivo e Agendamento:**
    - [ ] Implementar a lógica para ler o arquivo de conteúdo.
    - [ ] Criar um novo processo ou thread para funcionar como agendador.
2.  **Lógica de Postagem:**
    - [ ] Criar a função para postar um novo tweet a partir do conteúdo lido.
3.  **Testes e Deploy:**
    - [ ] Testar a nova funcionalidade em ambiente de desenvolvimento.
    - [ ] Fazer o deploy da nova versão no Railway.