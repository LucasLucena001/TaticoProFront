# ⚡ Início Rápido - Agente Inteligente Tático Pro

## 🚀 Como Iniciar (5 minutos)

### 1. Backend (Terminal 1)

```bash
cd backend-agent
python -m venv venv
venv\Scripts\activate                    # Windows
# source venv/bin/activate                # Linux/Mac
pip install -r requirements.txt
python main.py
```

✅ **Aguarde ver:** "🎉 Agente pronto para uso!"

### 2. Frontend (Terminal 2)

```bash
cd team-tactician-suite
npm run dev
```

✅ **Acesse:** `http://localhost:5173/chat`

## 💬 Teste o Agente

Digite no chat:

```
"Quantos gols o Internacional marcou nos últimos 5 jogos?"
```

✅ **Resposta esperada:** O agente vai consultar o banco e responder com dados reais!

## 📊 O que foi configurado

| Componente | Status | Detalhes |
|------------|--------|----------|
| **OpenAI API** | ✅ Configurado | GPT-4o |
| **Supabase** | ✅ Conectado | Database URL |
| **LlamaIndex** | ✅ SQL Retriever | Consultas automáticas |
| **LangChain** | ✅ Chat Agent | Contexto conversacional |
| **FastAPI** | ✅ Webhook | `/webhook/chat` |
| **React** | ✅ UI Chat | Interface moderna |

## 🎯 Arquitetura Simplificada

```
[Usuário digita pergunta]
         ↓
[React Frontend] → POST /webhook/chat
         ↓
[LangChain] → Detecta se precisa de dados
         ↓
[LlamaIndex] → Gera SQL automático
         ↓
[Supabase] → Retorna dados
         ↓
[GPT-4o] → Formata resposta natural
         ↓
[Frontend exibe] 🎉
```

## 📁 Estrutura de Pastas

```
TaticoProFront/
├── backend-agent/               # ✅ Backend Python
│   ├── main.py                 # FastAPI server
│   ├── .env                    # ✅ Configurado (API Key)
│   ├── requirements.txt        # Dependências
│   └── agent/
│       ├── llama_sql.py        # LlamaIndex
│       └── langchain_chat.py   # LangChain
│
└── team-tactician-suite/       # ✅ Frontend React
    ├── src/pages/Chat.tsx      # ✅ Atualizado (Webhook)
    └── README.md               # Docs principal
```

## 🔥 Perguntas que o Agente Responde

### ⚽ Gols e Estatísticas
```
"Quantos gols o Internacional marcou nos últimos 5 jogos?"
"Qual a média de chutes do Flamengo?"
"Compare a posse de bola dos dois times"
```

### 🏆 Classificação
```
"Qual a posição do Flamengo no campeonato?"
"Quantos pontos o Internacional tem?"
"Mostre a tabela completa do Brasileirão"
```

### 👥 Jogadores
```
"Quem são os principais artilheiros do Inter?"
"Quais jogadores mais recuperam bola no Flamengo?"
"Qual a formação provável do Internacional?"
```

### 📊 Análises Avançadas
```
"Qual o período mais perigoso do Internacional?"
"Quantas substituições o Inter faz em média?"
"Quem são os criadores de jogada do Flamengo?"
```

## 🐛 Problemas Comuns

### Backend não inicia

```bash
# Verifique se o ambiente virtual está ativado
# Reinstale dependências
pip install --upgrade -r requirements.txt
```

### Frontend não conecta

1. Backend rodando? → `http://localhost:8000`
2. Veja erro no console do navegador (F12)
3. Teste: `curl http://localhost:8000/health`

### Resposta "Backend não disponível"

O backend demora ~10-30s para inicializar (carrega schema do banco).
Aguarde a mensagem "🎉 Agente pronto para uso!"

## 📚 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| `backend-agent/README.md` | Documentação completa do backend |
| `backend-agent/INSTALL.md` | Guia de instalação detalhado |
| `team-tactician-suite/AGENT_SETUP.md` | Setup do frontend |
| `team-tactician-suite/README.md` | README principal do projeto |

## 🎉 Pronto!

Agora você tem:
- ✅ Agente inteligente com GPT-4o
- ✅ Consultas SQL automáticas
- ✅ Interface de chat moderna
- ✅ Contexto conversacional
- ✅ Dados reais do Brasileirão 2024

**Divirta-se conversando com o agente! ⚽🤖**

---

## 🚀 Próximos Passos

1. Explore as perguntas sugeridas
2. Veja a query SQL gerada (clique em "📊 Ver query SQL")
3. Teste perguntas complexas
4. Leia a documentação completa
5. Customize a interface

**Dúvidas?** Veja os arquivos README em cada pasta!


