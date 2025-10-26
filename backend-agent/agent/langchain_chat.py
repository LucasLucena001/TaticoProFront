"""
LangChain Conversational Agent
Responsável pela interface conversacional com o usuário
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import List, Dict, Any, Optional
import uuid
import os

class TaticoProAgent:
    """
    Agente conversacional do Tático Pro
    Usa LangChain para manter contexto e LlamaIndex para queries SQL
    """
    
    def __init__(self, llama_sql):
        """
        Inicializar agente
        
        Args:
            llama_sql: Instância do LlamaSQLRetriever
        """
        self.llama_sql = llama_sql
        self.sessions = {}  # Memória por sessão (InMemoryChatMessageHistory)
        
        # Configurar LLM principal (GPT-4o - mais recente)
        self.llm = ChatOpenAI(
            model="gpt-4o",  # GPT-4o - modelo mais recente e rápido
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        print("✅ TaticoProAgent inicializado")
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> tuple:
        """
        Obter ou criar sessão de conversa
        
        Args:
            session_id: ID da sessão (opcional)
            
        Returns:
            Tuple (session_id, chat_history)
        """
        if session_id and session_id in self.sessions:
            return session_id, self.sessions[session_id]
        
        # Criar nova sessão
        new_session_id = session_id or str(uuid.uuid4())
        chat_history = InMemoryChatMessageHistory()
        self.sessions[new_session_id] = chat_history
        
        return new_session_id, chat_history
    
    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processar mensagem do usuário
        
        Args:
            user_message: Mensagem do usuário
            conversation_history: Histórico de conversa
            session_id: ID da sessão
            
        Returns:
            Dict com resposta e metadados
        """
        try:
            # Obter/criar sessão
            session_id, chat_history = self.get_or_create_session(session_id)
            
            # Restaurar histórico na memória
            if conversation_history:
                for msg in conversation_history[-5:]:  # Últimas 5 mensagens apenas
                    # Acessar atributos do objeto Pydantic ou dicionário
                    role = msg.role if hasattr(msg, 'role') else msg['role']
                    content = msg.content if hasattr(msg, 'content') else msg['content']
                    
                    if role == 'user':
                        chat_history.add_message(HumanMessage(content=content))
                    else:
                        chat_history.add_message(AIMessage(content=content))
            
            # Detectar se é uma pergunta que precisa de dados
            needs_data = self.requires_database_query(user_message)
            
            sql_query = None
            data_preview = None
            database_context = ""
            
            if needs_data:
                # Usar LlamaIndex para buscar dados
                print(f"🔍 Pergunta requer dados do banco...")
                query_result = await self.llama_sql.natural_language_query(user_message)
                
                print(f"📊 Resultado da query: {query_result}")  # DEBUG
                
                if query_result['success']:
                    database_context = f"\n\n**DADOS REAIS DO BANCO DE DADOS:**\n{query_result['answer']}\n\n**INSTRUÇÕES CRÍTICAS:**\n- Use EXATAMENTE os nomes de times/jogadores que aparecem acima\n- NÃO invente ou generalize nomes (não use 'Time A', 'Time B', etc)\n- Cite os números EXATOS fornecidos\n- NÃO diga que não tem acesso aos dados!"
                    sql_query = query_result.get('sql_query')
                    print(f"✅ Dados obtidos: {database_context[:500]}...")  # DEBUG - aumentei para ver mais
            
            # Gerar resposta usando LLM diretamente
            system_prompt = """Você é o **Agente Inteligente do Tático Pro**, um assistente especializado em análise tática de futebol.

Você tem acesso a um banco de dados completo com:
- Jogos do Brasileirão 2024
- Estatísticas detalhadas por jogo
- Classificação do campeonato
- Informações de jogadores
- Inteligência tática

📅 **CONTEXTO TEMPORAL IMPORTANTE:**
- Estamos nas **RODADAS FINAIS** do Brasileirão 2024 (rodadas 36, 37, 38 de 38 totais)
- O campeonato está em DEZEMBRO de 2024
- Próximos jogos do Flamengo: rodadas 36, 37 e 38
- O próximo adversário do Flamengo é o **Internacional**

**⚠️ REGRAS CRÍTICAS - SIGA EXATAMENTE:**

1. **NUNCA use placeholders genéricos como:**
   - ❌ "[Nome do Jogador]"
   - ❌ "[Número de Substituições]"
   - ❌ "Jogador 1", "Jogador 2"
   - ❌ "Time A", "Time B"
   - ❌ "[Estatística]"
   
2. **SEMPRE use os dados EXATOS que foram fornecidos:**
   - ✅ "Thiago Maia"
   - ✅ "14 vezes aos 63.6 minutos"
   - ✅ "Rafael Borré (8 gols, 3 assistências)"

3. **Se você receber dados no formato "Nome (estatística)":**
   - Formato: "Thiago Maia (14x aos 63.6min), Bruno Henrique (12x aos 66.5min)"
   - Você DEVE extrair e apresentar: "Thiago Maia foi substituído 14 vezes em média aos 63.6 minutos"
   - NUNCA responda: "Não consegui identificar o jogador"

4. **Quando os dados estiverem em "DADOS REAIS DO BANCO DE DADOS":**
   - Esses são dados REAIS consultados do PostgreSQL
   - Você DEVE usar esses dados na resposta
   - NÃO diga "não tenho acesso" - VOCÊ TEM!

5. Sempre responda em português brasileiro
6. Use emojis para deixar as respostas mais dinâmicas ⚽
7. Seja direto e objetivo
8. Cite números e estatísticas com precisão

**EXEMPLOS DE RESPOSTAS CORRETAS:**

Pergunta: "Qual jogador foi mais substituído do Internacional?"
Dados: "Thiago Maia (14x aos 63.6min), Bruno Henrique (12x aos 66.5min), Wesley (11x aos 68.2min)"

✅ RESPOSTA CORRETA:
"O jogador do Internacional que foi mais substituído é o **Thiago Maia**, que saiu do banco 14 vezes, em média aos 63.6 minutos de jogo ⏱️. 

Em seguida temos:
- **Bruno Henrique**: 12 substituições (média aos 66.5 min)
- **Wesley**: 11 substituições (média aos 68.2 min) ⚽"

❌ RESPOSTAS ERRADAS:
- "O jogador mais substituído é **[Nome do Jogador]**" ❌
- "Não consegui identificar" ❌
- "Jogador 1, Jogador 2" ❌

**LEMBRE-SE: Se os dados foram fornecidos, USE-OS EXPLICITAMENTE NA RESPOSTA!**"""

            # Montar mensagens
            messages = [
                HumanMessage(content=system_prompt)
            ]
            
            # Adicionar histórico
            messages.extend(chat_history.messages[-6:])  # Últimas 6 mensagens
            
            # Adicionar pergunta atual
            full_question = user_message + database_context
            messages.append(HumanMessage(content=full_question))
            
            # Gerar resposta
            response = await self.llm.ainvoke(messages)
            final_response = response.content
            
            # Salvar na memória
            chat_history.add_message(HumanMessage(content=user_message))
            chat_history.add_message(AIMessage(content=final_response))
            
            return {
                "response": final_response,
                "sql_query": sql_query,
                "data_preview": data_preview,
                "session_id": session_id
            }
        
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "response": f"Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.",
                "sql_query": None,
                "data_preview": None,
                "session_id": session_id or str(uuid.uuid4())
            }
    
    def requires_database_query(self, message: str) -> bool:
        """
        Detectar se a mensagem precisa de consulta ao banco
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            True se precisa de dados, False caso contrário
        """
        # Keywords que indicam necessidade de dados
        data_keywords = [
            "quantos", "quanto", "qual", "quais", "quem",
            "estatística", "média", "total", "últimos", "próximos", "proximo", "proximos",
            "classificação", "posição", "pontos", "gols",
            "jogadores", "artilheiros", "time", "confronto",
            "histórico", "resultados", "jogos", "partidas", "jogo", "adversário", "adversario",
            "compare", "comparar", "diferença", "melhor", "pior",
            "substituído", "substituídos", "substituições", "substituir",
            "mais utilizados", "titulares", "escalação", "formação",
            "minutos", "tempo de jogo", "resistentes", "quando", "onde", "data"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in data_keywords)
    

