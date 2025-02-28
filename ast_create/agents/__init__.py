"""
Пакет для работы с AI-агентами.

Этот пакет содержит модули для работы с AI-агентами,
которые используются для автоматического расширения грамматики
и анализа кода на языке 1С.
"""

from .agent_coordinator import AgentCoordinator, get_agent_coordinator
from .grammar_agent import GrammarAgent

__all__ = ['AgentCoordinator', 'get_agent_coordinator', 'GrammarAgent']
