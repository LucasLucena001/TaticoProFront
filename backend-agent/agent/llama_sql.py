"""
LlamaIndex SQL Retriever
Responsável por gerar e executar queries SQL seguras no Supabase
"""

from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine, text
from typing import List, Dict, Any
import os

class LlamaSQLRetriever:
    """
    Classe responsável por consultas SQL usando LlamaIndex
    """
    
    def __init__(self, database_url: str):
        """
        Inicializar conexão com banco e LlamaIndex
        
        Args:
            database_url: URL de conexão PostgreSQL
        """
        self.database_url = database_url
        self.engine = create_engine(database_url)
        
        # Inicializar LlamaIndex SQL Database com TODAS as tabelas importantes
        self.sql_database = SQLDatabase(
            self.engine,
            include_tables=[
                # Tabelas brutas de dados
                "Jogos_Completos_2024",
                "Estatisticas_Por_Jogo_2024",
                "Estatisticas_Jogadores_Por_Jogo_2024",
                "Eventos_Jogos_2024",
                "Jogadores_por_Time_2024_2",
                "Relacionados_por_Jogo_2024",
                "Resultados_Jogos_2024",
                "Tecnicos_2024",
                "Times_2024",
                # Tabelas analíticas do Internacional (int_*)
                "int_stats_comparativas",
                "int_jogadores_detalhados",
                "int_inteligencia_tatica",
                "int_momentum_atual",
                "int_classificacao_campeonato",
                "int_vulnerabilidades_taticas",
                "int_analise_pressao",
                "int_analise_tatica_avancada",
                "int_confrontos_diretos",
                "int_impacto_jogadores",
                "int_reacao_pos_gol",
                "int_vulnerabilidades_campo",
                "int_perfil_psicologico",
                "int_proximo_adversario"
            ]
        )
        
        # Configurar LLM (GPT-4o - mais recente e rápido)
        self.llm = OpenAI(
            model="gpt-4o",  # GPT-4o - modelo mais recente
            temperature=0,  # Mais determinístico para SQL
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Criar Query Engine com instruções SQL personalizadas
        sql_context_str = """
        ⚠️ INSTRUÇÕES CRÍTICAS PARA GERAR SQL - SIGA EXATAMENTE ⚠️
        
        REGRA PRINCIPAL: SEMPRE use as tabelas analíticas pré-processadas (int_*) quando disponíveis.
        NUNCA calcule dados que já estão processados nas tabelas int_*.
        
        1. ❌ ERRADO - NUNCA FAÇA ISSO:
           SELECT player_name, COUNT(*) FROM Relacionados_por_Jogo_2024 WHERE lineup_type = 'Substitute' GROUP BY player_name;
           
        2. ✅ CORRETO - SEMPRE USE AS TABELAS int_*:
        
        A. JOGADORES MAIS SUBSTITUÍDOS do Internacional:
           Query SQL: SELECT mais_substituidos FROM int_jogadores_detalhados WHERE adversario = 'Internacional';
           Retorna: "Thiago Maia (14x aos 63.6min), Bruno Henrique (12x aos 66.5min), Wesley (11x aos 68.2min)"
        
        B. ARTILHEIROS do Internacional:
           Query SQL: SELECT principais_artilheiros FROM int_jogadores_detalhados WHERE adversario = 'Internacional';
           Retorna: "Rafael Borré (8g, 3a), Wesley (8g, 1a), Alan Patrick (6g)"
        
        C. JOGADORES MAIS UTILIZADOS:
           Query SQL: SELECT jogadores_mais_utilizados FROM int_jogadores_detalhados WHERE adversario = 'Internacional';
           Retorna: "Sergio Rochet (~25 jogos), Vitão (~24 jogos), Wesley (~24 jogos)"
        
        D. CLASSIFICAÇÃO DO CAMPEONATO:
           Query SQL: SELECT posicao, time, pontos_total, jogos_disputados, total_vitorias, total_empates, total_derrotas 
                      FROM int_classificacao_campeonato 
                      ORDER BY posicao;
           
        E. ESTATÍSTICAS COMPARATIVAS:
           Query SQL: SELECT * FROM int_stats_comparativas;
           
        F. MOMENTUM (últimos 5 jogos):
           Query SQL: SELECT time, pontos_recentes, sequencia_recente FROM int_momentum_atual;
           
        G. PRÓXIMO JOGO:
           Query SQL: SELECT * FROM int_proximo_adversario;
        
        IMPORTANTE:
        - int_jogadores_detalhados contém TODOS os dados de jogadores JÁ PROCESSADOS
        - NÃO use COUNT(), GROUP BY, ou agregações em Relacionados_por_Jogo_2024
        - Os dados estão no formato "Nome (estatística)" - exemplo: "Thiago Maia (14x aos 63.6min)"
        - SEMPRE retorne o valor COMPLETO da coluna, NÃO tente parsear ou extrair partes
        """
        
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
            synthesize_response=True,
            context_str_prefix=sql_context_str
        )
        
        print("✅ LlamaSQLRetriever inicializado")
    
    async def natural_language_query(self, question: str) -> Dict[str, Any]:
        """
        Executar query em linguagem natural
        
        Args:
            question: Pergunta em linguagem natural
            
        Returns:
            Dict com resposta, SQL gerado e dados
        """
        try:
            # Executar query
            response = self.query_engine.query(question)
            
            # Extrair SQL gerado (se disponível)
            sql_query = None
            if hasattr(response, 'metadata') and 'sql_query' in response.metadata:
                sql_query = response.metadata['sql_query']
            
            return {
                "answer": str(response),
                "sql_query": sql_query,
                "success": True
            }
        
        except Exception as e:
            print(f"❌ Erro na query LlamaIndex: {str(e)}")
            return {
                "answer": f"Desculpe, não consegui processar sua pergunta: {str(e)}",
                "sql_query": None,
                "success": False,
                "error": str(e)
            }
    
    async def execute_raw_query(self, sql: str) -> List[Dict]:
        """
        Executar query SQL direta (para debugging)
        
        Args:
            sql: Query SQL
            
        Returns:
            Lista de resultados
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                rows = result.fetchall()
                
                # Converter para dict
                columns = result.keys()
                return [dict(zip(columns, row)) for row in rows]
        
        except Exception as e:
            print(f"❌ Erro ao executar SQL: {str(e)}")
            raise e
    
    async def get_available_tables(self) -> List[str]:
        """
        Listar todas as tabelas disponíveis
        
        Returns:
            Lista de nomes de tabelas
        """
        return self.sql_database.get_usable_table_names()
    
    async def get_table_info(self, table_name: str) -> str:
        """
        Obter informações sobre uma tabela específica
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            String com schema da tabela
        """
        return self.sql_database.get_single_table_info(table_name)
    
    def get_context_for_question(self, question: str) -> str:
        """
        Gerar contexto sobre o banco de dados para uma pergunta
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            Contexto formatado
        """
        # Lista de TODAS as tabelas e suas descrições DETALHADAS
        table_descriptions = {
            # Tabelas brutas de dados (USE APENAS SE NÃO EXISTIR TABELA int_* EQUIVALENTE)
            "Jogos_Completos_2024": "Jogos completos do Brasileirão 2024 (fixture_id, round, date, home_team, away_team, venue, status)",
            "Estatisticas_Por_Jogo_2024": "Estatísticas detalhadas por jogo (chutes, posse, faltas, cartões, escanteios, passes)",
            "Estatisticas_Jogadores_Por_Jogo_2024": "Estatísticas individuais de jogadores por jogo (rating, gols, assistências, passes, dribles, tackles)",
            "Eventos_Jogos_2024": "Eventos dos jogos (gols, cartões, substituições, momento/minuto do evento)",
            "Jogadores_por_Time_2024_2": "Lista de jogadores por time (nome, posição, número, idade)",
            "Relacionados_por_Jogo_2024": "⚠️ NÃO USE para contar substituições! Use int_jogadores_detalhados. Escalações por jogo (titulares, reservas)",
            "Resultados_Jogos_2024": "Resultados finais dos jogos (placar, vencedor, estádio, árbitro)",
            "Tecnicos_2024": "Informações sobre técnicos (nome, time, idade, nacionalidade)",
            "Times_2024": "Informações gerais dos times (nome, estádio, cidade, fundação)",
            
            # ✅ TABELAS ANALÍTICAS PRÉ-PROCESSADAS - USE ESTAS SEMPRE QUE POSSÍVEL!
            "int_stats_comparativas": """⭐ Comparação Flamengo vs Internacional (JÁ CALCULADO):
                Colunas: time, media_chutes, chutes_no_gol, media_escanteios, media_posse, media_faltas
                Use para: comparar estatísticas médias entre os times""",
            
            "int_jogadores_detalhados": """⭐⭐⭐ PRINCIPAL TABELA DE JOGADORES (JÁ PROCESSADO):
                Colunas importantes:
                - mais_substituidos (STRING): "Thiago Maia (14x aos 63.6min), Bruno Henrique (12x aos 66.5min)"
                - principais_artilheiros (STRING): "Rafael Borré (8g, 3a), Wesley (8g, 1a)"
                - jogadores_mais_utilizados (STRING): "Sergio Rochet (~25 jogos), Vitão (~24 jogos)"
                - titulares_provaveis (STRING): lista de 11 jogadores
                - formacao_preferida (STRING): ex: "4-3-3"
                - jogadores_resistentes (STRING): raramente substituídos
                ⚠️ IMPORTANTE: Use SELECT [coluna] FROM int_jogadores_detalhados WHERE adversario = 'Internacional'
                ⚠️ NÃO FAÇA: COUNT, GROUP BY, ou cálculos - os dados JÁ estão prontos!""",
            
            "int_inteligencia_tatica": """Inteligência tática avançada:
                Colunas: padrao_substituicoes, principais_recuperadores, criadores_jogadas, especialistas_penaltis,
                periodo_mais_perigoso, periodo_menos_perigoso""",
            
            "int_momentum_atual": """Momentum recente (últimos 5 jogos):
                Colunas: time, pontos_recentes, sequencia_recente, gols_marcados_recentes, gols_sofridos_recentes""",
            
            "int_classificacao_campeonato": """Classificação COMPLETA do Brasileirão:
                Colunas: posicao, time, pontos_total, jogos_disputados, total_vitorias, total_empates, total_derrotas,
                gols_marcados, gols_sofridos, saldo_gols, aproveitamento_pct, ultimos_5_jogos""",
            
            "int_proximo_adversario": "Próximo jogo do Flamengo (adversario, data, horario, local, rodada_campeonato)",
            "int_vulnerabilidades_taticas": "Vulnerabilidades táticas do Inter (falhas_goleiro, disciplina, eficiencia_escanteios)",
            "int_analise_pressao": "Análise psicológica sob pressão (comportamento_jogos_grandes, performance_final_campeonato)",
            "int_analise_tatica_avancada": "Análise tática avançada (padroes_gols, vulnerabilidades_casa_fora, indisciplina)",
            "int_confrontos_diretos": "Histórico Flamengo x Inter (total_jogos, vitorias_flamengo, vitorias_inter, empates)",
            "int_impacto_jogadores": "Impacto de jogadores chave (jogadores_fundamentais, jogadores_problematicos, maior_impacto_ofensivo)",
            "int_reacao_pos_gol": "Reação após sofrer gol (comportamento_pos_gol, media_cartoes_pos_gol)",
            "int_vulnerabilidades_campo": "Vulnerabilidades por área (tipo_gols_sofridos, periodo_fadiga, melhor_periodo)",
            "int_perfil_psicologico": "Perfil psicológico (periodo_jogo_intenso, capacidade_reacao, controle_emocional, dna_tatico)"
        }
        
        context = "📊 **Banco de Dados - Tático Pro**\n\n"
        context += "Tabelas disponíveis:\n"
        for table, desc in table_descriptions.items():
            context += f"• {table}: {desc}\n"
        
        return context

