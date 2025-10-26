"""
Tático Pro - Agente Inteligente
Módulo de agentes (LlamaIndex + LangChain)
"""

from .llama_sql import LlamaSQLRetriever
from .langchain_chat import TaticoProAgent

__all__ = [
    "LlamaSQLRetriever",
    "TaticoProAgent"
]


