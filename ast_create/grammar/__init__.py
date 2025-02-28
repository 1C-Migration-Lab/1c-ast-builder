"""
Пакет для работы с грамматикой языка 1С.

Этот пакет содержит модули для определения грамматики языка 1С,
парсинга исходного кода и управления версиями грамматики.
"""

from .grammar_manager import GrammarManager, GrammarVersion, get_grammar_manager
from .parser import Parser

__all__ = ["Parser", "GrammarManager", "GrammarVersion", "get_grammar_manager"]
