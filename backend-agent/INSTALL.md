# 🚀 Guia de Instalação - Agente Inteligente Tático Pro

## 📋 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Conta OpenAI com API Key
- Acesso ao banco de dados Supabase

## 🔧 Instalação Passo a Passo

### 1. Criar Ambiente Virtual

```bash
# Navegar para o diretório do backend
cd backend-agent

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

**Principais dependências instaladas:**
- FastAPI (framework web)
- LlamaIndex (SQL Retriever)
- LangChain (conversational AI)
- OpenAI (GPT-4o)
- SQLAlchemy (ORM)
- psycopg2 (PostgreSQL driver)

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend-agent` com:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
DATABASE_URL=postgresql://usuario:senha@host:porta/database
FRONTEND_URL=http://localhost:5173
HOST=0.0.0.0
PORT=8000
```

⚠️ **IMPORTANTE:** Substitua pelos valores reais do seu projeto Supabase e OpenAI.

### 4. Iniciar o Servidor

```bash
# Método 1: Usando Python diretamente
python main.py

# Método 2: Usando uvicorn (recomendado para desenvolvimento)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output esperado:**
```
🚀 Inicializando Tático Pro Agent...
✅ LlamaIndex SQL Retriever inicializado
✅ LangChain Conversational Agent inicializado
🎉 Agente pronto para uso!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5. Verificar se está funcionando

Abra o navegador em: `http://localhost:8000`

Você deve ver:
```json
{
  "status": "online",
  "service": "Tático Pro - Agente Inteligente",
  "version": "1.0.0"
}
```

## 🧪 Testar o Agente

### Via navegador (Frontend)

1. Certifique-se de que o backend está rodando (porta 8000)
2. Inicie o frontend: `npm run dev` (na pasta `team-tactician-suite`)
3. Acesse `http://localhost:5173/chat`
4. Envie uma mensagem: "Quantos gols o Internacional marcou nos últimos 5 jogos?"

### Via curl (Terminal)

```bash
curl -X POST http://localhost:8000/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Qual a posição do Flamengo no campeonato?",
    "conversation_history": [],
    "session_id": null
  }'
```

### Via Python

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

print(response.json()["response"])
```

## 📊 Documentação Interativa

FastAPI gera documentação automática:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🔍 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Health check |
| `/health` | GET | Status dos agentes |
| `/webhook/chat` | POST | Chat principal |
| `/webhook/sql-query` | POST | Query SQL direta |
| `/tables` | GET | Listar tabelas |

## 🐛 Troubleshooting

### Erro: ModuleNotFoundError

```bash
# Verifique se o ambiente virtual está ativado
# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "OpenAI API Key inválida"

Verifique se a chave no `.env` está correta e ativa.

### Erro: Conexão com banco de dados

```python
# Testar conexão manualmente
from sqlalchemy import create_engine
engine = create_engine("sua-database-url")
engine.connect()
```

### Porta 8000 já em uso

```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

## 📦 Estrutura de Arquivos

```
backend-agent/
├── main.py                 # Servidor FastAPI principal
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente (CONFIGURADO)
├── config.example.env      # Exemplo de configuração
├── README.md               # Documentação completa
├── INSTALL.md              # Este arquivo
└── agent/
    ├── __init__.py
    ├── llama_sql.py        # LlamaIndex SQL Retriever
    └── langchain_chat.py   # LangChain Conversational Agent
```

## 🎯 Próximos Passos

1. ✅ Backend configurado e rodando
2. ⏭️ Teste o chat no frontend (`/chat`)
3. ⏭️ Faça perguntas sobre o Brasileirão 2024
4. ⏭️ Explore a documentação interativa

## 🚀 Deploy (Produção)

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

### Render / Railway

1. Conecte seu repositório
2. Configure as variáveis de ambiente
3. Comando de build: `pip install -r requirements.txt`
4. Comando de start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

**⚽ Tático Pro - IA para Análise Tática** 🧠

**Dúvidas?** Veja o README.md completo ou a documentação em `/docs`


