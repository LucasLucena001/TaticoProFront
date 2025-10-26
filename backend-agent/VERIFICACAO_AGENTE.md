# ✅ Verificação do Agente Inteligente

## 📋 Checklist pré-teste

Antes de testar o agente, verifique se ele tem acesso a todas as tabelas do banco.

### 1️⃣ Verificar tabelas disponíveis

**Endpoint:** `GET http://localhost:8000/tables`

**Resposta esperada:** Lista com 24 tabelas:

```json
{
  "tables": [
    "Jogos_Completos_2024",
    "Estatisticas_Por_Jogo_2024",
    "Estatisticas_Jogadores_Por_Jogo_2024",
    "Eventos_Jogos_2024",
    "Jogadores_por_Time_2024_2",
    "Relacionados_por_Jogo_2024",
    "Resultados_Jogos_2024",
    "Tecnicos_2024",
    "Times_2024",
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
}
```

### 2️⃣ Verificar Health do Backend

**Endpoint:** `GET http://localhost:8000/health`

**Resposta esperada:**
```json
{
  "status": "healthy",
  "llama_sql": true,
  "tatico_agent": true
}
```

### 3️⃣ Testes de Queries Específicas

#### Teste 1: Jogadores Mais Substituídos (CRÍTICO)

**Pergunta:** "Qual jogador foi mais substituído do Internacional?"

**SQL esperado:**
```sql
SELECT mais_substituidos 
FROM int_jogadores_detalhados 
WHERE adversario = 'Internacional';
```

**❌ SQL INCORRETO (NÃO deve gerar):**
```sql
SELECT player_name, COUNT(*) as substitution_count
FROM Relacionados_por_Jogo_2024
WHERE team_name = 'Internacional' AND lineup_type = 'Substitute'
GROUP BY player_name
ORDER BY substitution_count DESC;
```

**Resposta esperada:**
```
O jogador do Internacional que foi mais substituído é o Thiago Maia, 
que saiu do banco 14 vezes, em média aos 63.6 minutos de jogo ⏱️.

Em seguida temos:
- Bruno Henrique: 12 substituições (média aos 66.5 min)
- Wesley: 11 substituições (média aos 68.2 min) ⚽
```

**❌ Resposta INCORRETA (NÃO deve retornar):**
- "[Nome do Jogador]"
- "Não consegui identificar"
- "Jogador 1, Jogador 2"

---

#### Teste 2: Artilheiros

**Pergunta:** "Quais são os artilheiros do Internacional?"

**SQL esperado:**
```sql
SELECT principais_artilheiros 
FROM int_jogadores_detalhados 
WHERE adversario = 'Internacional';
```

**Resposta esperada:**
```
Os principais artilheiros do Internacional são:
1. Rafael Borré - 8 gols e 3 assistências ⚽
2. Wesley - 8 gols e 1 assistência 
3. Alan Patrick - 6 gols 🎯
```

---

#### Teste 3: Classificação

**Pergunta:** "Qual a posição do Flamengo na classificação?"

**SQL esperado:**
```sql
SELECT posicao, pontos_total, jogos_disputados 
FROM int_classificacao_campeonato 
WHERE time = 'Flamengo';
```

---

#### Teste 4: Estatísticas Comparativas

**Pergunta:** "Compare os chutes e posse de bola do Flamengo e Inter"

**SQL esperado:**
```sql
SELECT time, media_chutes, chutes_no_gol, media_posse 
FROM int_stats_comparativas;
```

---

#### Teste 5: Jogadores Mais Utilizados

**Pergunta:** "Quais jogadores do Inter têm mais minutos jogados?"

**SQL esperado:**
```sql
SELECT jogadores_mais_utilizados 
FROM int_jogadores_detalhados 
WHERE adversario = 'Internacional';
```

**Resposta esperada:**
```
Os jogadores do Internacional com mais minutos são:
1. Sergio Rochet - ~25 jogos completos 🧤
2. Vitão - ~24 jogos completos 🛡️
3. Wesley - ~24 jogos completos ⚽
```

---

## 🔍 Como Verificar os Logs

Durante os testes, o terminal do backend mostrará:

```
🔍 Pergunta requer dados do banco...
📊 Resultado da query: {'answer': '...', 'sql_query': '...', 'success': True}
✅ Dados obtidos: DADOS REAIS DO BANCO DE DADOS: ...
```

**Verifique:**
1. ✅ `sql_query` está usando `int_jogadores_detalhados`
2. ✅ `answer` contém nomes reais de jogadores
3. ✅ Não aparece "COUNT(*)" ou "GROUP BY" para substituições

---

## ❌ Problemas Comuns e Soluções

### Problema 1: SQL incorreto (usando Relacionados_por_Jogo_2024)

**Solução:** Verificar se `llama_sql.py` tem as instruções SQL corretas no `context_str_prefix`

### Problema 2: Resposta com placeholders "[Nome do Jogador]"

**Solução:** Verificar se `langchain_chat.py` tem o `system_prompt` atualizado

### Problema 3: "Não consegui identificar o jogador"

**Solução:** Verificar se os dados estão sendo passados corretamente no `database_context`

### Problema 4: Tabela int_jogadores_detalhados não encontrada

**Solução:** Verificar conexão com Supabase e se a tabela existe usando o endpoint `/tables`

---

## 📊 Estrutura da Tabela int_jogadores_detalhados

```sql
-- Verificar dados da tabela (via Supabase SQL Editor ou psql)
SELECT adversario, mais_substituidos, principais_artilheiros 
FROM int_jogadores_detalhados 
WHERE adversario = 'Internacional';
```

**Resultado esperado:**

| adversario | mais_substituidos | principais_artilheiros |
|-----------|------------------|----------------------|
| Internacional | Thiago Maia (14x aos 63.6min), Bruno Henrique (12x aos 66.5min), Wesley (11x aos 68.2min) | Rafael Borré (8g, 3a), Wesley (8g, 1a), Alan Patrick (6g) |

---

## ✅ Checklist Final

Antes de considerar o agente pronto:

- [ ] Backend iniciando sem erros
- [ ] Endpoint `/health` retorna `healthy`
- [ ] Endpoint `/tables` lista 24 tabelas
- [ ] Query "jogadores mais substituídos" usa `int_jogadores_detalhados`
- [ ] Resposta contém nomes REAIS (não placeholders)
- [ ] Resposta extrai corretamente formato "Nome (Nx aos XXmin)"
- [ ] Queries de artilheiros, classificação e stats funcionam
- [ ] Logs mostram SQL correto sendo gerado
- [ ] Nenhum erro de conexão com Supabase
- [ ] Nenhum erro de API OpenAI (quota OK)

---

## 🎯 Objetivo Final

O agente deve ser capaz de responder CORRETAMENTE:

> **User:** "Qual jogador foi mais substituído do Internacional?"  
> **Agent:** "O jogador do Internacional que foi mais substituído é o **Thiago Maia**, que saiu do banco 14 vezes, em média aos 63.6 minutos de jogo ⏱️. Em seguida temos Bruno Henrique (12 substituições) e Wesley (11 substituições) ⚽"

**Sem:**
- ❌ Placeholders "[Nome]"
- ❌ "Não consegui identificar"
- ❌ SQL incorreto com COUNT/GROUP BY
- ❌ Nomes genéricos "Jogador 1"

---

## 🚀 Próximos Passos Após Validação

1. Testar todas as queries da lista acima
2. Verificar se o agente mantém contexto em conversas longas
3. Testar edge cases (times que não existem, perguntas ambíguas)
4. Documentar respostas no TCC
5. Criar demonstração em vídeo

---

**Data de criação:** Outubro 2025  
**Última atualização:** Agora mesmo 🎉


