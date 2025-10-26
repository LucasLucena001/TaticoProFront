"""
TÁTICO PRO - Agente Inteligente Backend
FastAPI + LlamaIndex + LangChain

Arquitetura:
1. LlamaIndex → SQL Retriever (consultas estruturadas no Supabase)
2. LangChain → Conversational Agent (contexto e memória)
3. FastAPI → Webhook REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar módulos do agente
from agent.llama_sql import LlamaSQLRetriever
from agent.langchain_chat import TaticoProAgent

# Inicializar FastAPI
app = FastAPI(
    title="Tático Pro - Agente Inteligente",
    description="API do agente inteligente para análise tática de futebol",
    version="1.0.0"
)

# Configurar CORS (permitir requisições do frontend)
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",  # Porta alternativa do Vite
    "http://127.0.0.1:8080",
    os.getenv("FRONTEND_URL", "http://localhost:5173")
]
print(f"🌐 CORS configurado para: {', '.join(allowed_origins)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Models para API
class ChatMessage(BaseModel):
    role: str  # "user" ou "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sql_query: Optional[str] = None
    data_preview: Optional[dict] = None
    session_id: str

# Inicializar agentes globais
llama_sql = None
tatico_agent = None

@app.on_event("startup")
async def startup_event():
    """Inicializar agentes na inicialização do servidor"""
    global llama_sql, tatico_agent
    
    print("🚀 Inicializando Tático Pro Agent...")
    
    # Inicializar LlamaIndex SQL Retriever
    database_url = os.getenv("DATABASE_URL")
    llama_sql = LlamaSQLRetriever(database_url)
    print("✅ LlamaIndex SQL Retriever inicializado")
    
    # Inicializar LangChain Agent
    tatico_agent = TaticoProAgent(llama_sql)
    print("✅ LangChain Conversational Agent inicializado")
    
    print("🎉 Agente pronto para uso!")

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Tático Pro - Agente Inteligente",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Verificar saúde do serviço"""
    return {
        "status": "healthy",
        "llama_sql": llama_sql is not None,
        "tatico_agent": tatico_agent is not None
    }

@app.post("/webhook/chat", response_model=ChatResponse)
async def chat_webhook(request: ChatRequest):
    """
    Webhook principal para o chat
    
    Recebe mensagem do usuário e retorna resposta do agente
    """
    try:
        if not tatico_agent:
            raise HTTPException(
                status_code=503,
                detail="Agente não inicializado. Aguarde alguns segundos."
            )
        
        # Processar mensagem com o agente
        response_data = await tatico_agent.process_message(
            user_message=request.message,
            conversation_history=request.conversation_history,
            session_id=request.session_id
        )
        
        return ChatResponse(**response_data)
    
    except Exception as e:
        print(f"❌ Erro no webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )

@app.post("/webhook/sql-query")
async def sql_query_webhook(query: str):
    """
    Webhook para executar query SQL direta (opcional, para debug)
    """
    try:
        if not llama_sql:
            raise HTTPException(
                status_code=503,
                detail="SQL Retriever não inicializado"
            )
        
        result = await llama_sql.execute_raw_query(query)
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na query: {str(e)}"
        )

@app.get("/tables")
async def list_tables():
    """Listar todas as tabelas disponíveis no banco"""
    try:
        if not llama_sql:
            raise HTTPException(status_code=503, detail="SQL Retriever não inicializado")
        
        tables = await llama_sql.get_available_tables()
        return {"tables": tables}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

