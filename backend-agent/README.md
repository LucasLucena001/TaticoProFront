# 🤖 Tático Pro - Backend do Agente Inteligente

Backend Python com FastAPI, LlamaIndex e LangChain para o agente inteligente de análise tática.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                   TÁTICO PRO AGENT                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐
│  Frontend   │  ──HTTP POST──►  ┌─────────────────────┐
│   (React)   │                   │   FastAPI Webhook   │
└─────────────┘                   └──────────┬──────────┘
                                            │
                                            ▼
                            ┌───────────────────────────────┐
                            │   LangChain (Conversacional)  │
                            │   • Contexto                  │
                            │   • Memória de sessão         │
                            │   • Prompt engineering        │
                            └─────────────┬─────────────────┘
                                          │
                                          ▼
                            ┌────────────────────────────────┐
                            │   LlamaIndex (SQL Retriever)  │
                            │   • Gera SQL seguro           │
                            │   • Executa queries           │
                            │   • Otimiza consultas         │
                            └─────────────┬──────────────────┘
                                          │
                                          ▼
                            ┌────────────────────────────────┐
                            │   Supabase (PostgreSQL)       │
                            │   • Jogos 2024                │
                            │   • Estatísticas              │
                            │   • Classificação             │
                            │   • Inteligência Tática       │
                            └────────────────────────────────┘
```

## 🚀 Instalação

### 1. Criar ambiente virtual

```bash
cd backend-agent
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo de exemplo e configure:

```bash
cp config.example.env .env
```

Edite `.env`:

```env
OPENAI_API_KEY=sk-your-openai-key
DATABASE_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
FRONTEND_URL=http://localhost:5173
```

### 4. Iniciar servidor

```bash
python main.py
```

Ou com uvicorn diretamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: `http://localhost:8000`

## 📡 Endpoints da API

### 1. Health Check

```bash
GET /
GET /health
```

Verifica se o servidor está online e os agentes estão inicializados.

### 2. Chat Webhook (Principal)

```bash
POST /webhook/chat
```

**Request:**
```json
{
  "message": "Quantos gols o Internacional marcou nos últimos 5 jogos?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Olá!"
    },
    {
      "role": "assistant",
      "content": "Olá! Como posso ajudar?"
    }
  ],
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "O Internacional marcou 10 gols nos últimos 5 jogos...",
  "sql_query": "SELECT SUM(home_goals) FROM...",
  "data_preview": {...},
  "session_id": "uuid"
}
```

### 3. SQL Query Direta (Debug)

```bash
POST /webhook/sql-query?query=SELECT * FROM int_stats_comparativas LIMIT 5
```

### 4. Listar Tabelas

```bash
GET /tables
```

Retorna todas as tabelas disponíveis no banco.

## 🧠 Como Funciona

### 1. LangChain - Camada Conversacional

O LangChain gerencia:
- **Contexto da conversa** (memória por sessão)
- **Prompt engineering** (instruções para o GPT-4)
- **Detecção de intenção** (pergunta precisa de dados?)

```python
# Exemplo de uso interno
tatico_agent = TaticoProAgent(llama_sql)
response = await tatico_agent.process_message(
    user_message="Qual a média de chutes do Flamengo?",
    session_id="abc123"
)
```

### 2. LlamaIndex - SQL Retriever

O LlamaIndex:
- **Entende o schema** do banco de dados
- **Gera SQL seguro** a partir de linguagem natural
- **Executa queries** no Supabase
- **Otimiza** consultas complexas

```python
# Exemplo de uso interno
llama_sql = LlamaSQLRetriever(database_url)
result = await llama_sql.natural_language_query(
    "Quantos jogos o Internacional venceu em casa?"
)
```

### 3. Fluxo Completo

```
User: "Quantos gols o Inter marcou nos últimos 5 jogos?"
  │
  ▼
[LangChain] Detecta que precisa de dados
  │
  ▼
[LlamaIndex] Gera SQL:
  SELECT SUM(home_goals + away_goals) 
  FROM Estatisticas_Por_Jogo_2024 
  WHERE ...
  │
  ▼
[Supabase] Executa query → Retorna: 10 gols
  │
  ▼
[LangChain] Formata resposta conversacional:
  "O Internacional marcou 10 gols nos últimos 5 jogos! ⚽🔥"
  │
  ▼
[FastAPI] Retorna JSON para o frontend
```

## 🗄️ Tabelas Disponíveis

O agente tem acesso a:

- `Jogos_Completos_2024` - Jogos do Brasileirão
- `Estatisticas_Por_Jogo_2024` - Estatísticas detalhadas
- `int_stats_comparativas` - Médias dos times
- `int_jogadores_detalhados` - Informações de jogadores
- `int_inteligencia_tatica` - Padrões táticos
- `int_momentum_atual` - Momento dos times
- `int_classificacao_campeonato` - Tabela do campeonato

## 🧪 Testar Localmente

### Usando curl

```bash
# Chat
curl -X POST http://localhost:8000/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Qual a posição do Flamengo no campeonato?",
    "conversation_history": [],
    "session_id": null
  }'

# Listar tabelas
curl http://localhost:8000/tables
```

### Usando Python

```python
import requests

response = requests.post(
    "http://localhost:8000/webhook/chat",
    json={
        "message": "Quantos pontos o Internacional tem?",
        "conversation_history": [],
        "session_id": None
    }
)

print(response.json())
```

## 📦 Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| FastAPI | 0.109.0 | Framework web |
| LlamaIndex | 0.10.0 | SQL Retriever + RAG |
| LangChain | 0.1.4 | Conversational Agent |
| OpenAI | 1.10.0 | GPT-4 API |
| SQLAlchemy | 2.0.25 | ORM Python |
| psycopg2 | 2.9.9 | Driver PostgreSQL |

## 🔒 Segurança

- ✅ CORS configurado para aceitar apenas o frontend
- ✅ LlamaIndex gera SQL parametrizado (previne SQL injection)
- ✅ Não expõe credenciais do banco
- ✅ Rate limiting recomendado (adicione middleware)

## 🚀 Deploy

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t tatico-pro-agent .
docker run -p 8000:8000 --env-file .env tatico-pro-agent
```

### Render / Railway / Fly.io

1. Configure as variáveis de ambiente
2. Comando de start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📝 Logs

O servidor exibe logs detalhados:

```
🚀 Inicializando Tático Pro Agent...
✅ LlamaIndex SQL Retriever inicializado
✅ LangChain Conversational Agent inicializado
🎉 Agente pronto para uso!
```

## 🐛 Troubleshooting

### Erro: "Agente não inicializado"

Aguarde alguns segundos após iniciar o servidor. O LlamaIndex precisa carregar o schema do banco.

### Erro: "OpenAI API Key inválida"

Verifique se a variável `OPENAI_API_KEY` está correta no `.env`.

### Erro de conexão com o banco

Verifique a `DATABASE_URL`. Teste a conexão:

```python
from sqlalchemy import create_engine
engine = create_engine("sua-database-url")
engine.connect()
```

## 📚 Documentação

- FastAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contribuindo

1. Clone o repositório
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

---

**⚽ Tático Pro - Inteligência Artificial para Análise Tática** 🧠


