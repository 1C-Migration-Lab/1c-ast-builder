"""
Модуль координации AI-агентов для работы с грамматикой.

Этот модуль предоставляет классы для координации работы
различных AI-агентов, управления их жизненным циклом и
обеспечения взаимодействия с системой грамматики.
"""

import logging
from typing import Dict, List, Optional, Set, Tuple

from ast_create.agents.grammar_agent import GrammarAgent
from ast_create.grammar.grammar_manager import get_grammar_manager

# Настройка логирования
logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Координатор для управления AI-агентами.

    Координатор отвечает за создание, запуск и мониторинг агентов,
    а также за обработку результатов их работы и интеграцию с
    системой управления грамматикой.

    Атрибуты:
        grammar_agent (GrammarAgent): Агент для работы с грамматикой
        enabled (bool): Флаг включения/выключения AI-агентов
    """

    def __init__(self, enable_agents: bool = True):
        """
        Инициализирует координатор агентов.

        Args:
            enable_agents: Флаг для включения/выключения AI-агентов
        """
        self.enabled = enable_agents

        # Создание агентов
        self.grammar_agent: Optional[GrammarAgent] = None

        if enable_agents:
            # Инициализация агента грамматики
            grammar_manager = get_grammar_manager()
            current_grammar = grammar_manager.current_version.grammar

            self.grammar_agent = GrammarAgent(current_grammar=current_grammar)
            logger.info("AI-агенты инициализированы")
        else:
            logger.info("AI-агенты отключены")

    def process_parse_error(self, error: Exception, code_snippet: str) -> bool:
        """
        Обрабатывает ошибку парсинга с использованием AI-агентов.

        Анализирует ошибку парсинга, используя агент для работы с грамматикой,
        и пытается автоматически расширить грамматику для поддержки
        неизвестной конструкции.

        Args:
            error: Исключение, возникшее при парсинге
            code_snippet: Фрагмент кода, вызвавший ошибку

        Returns:
            bool: True, если агент смог обработать ошибку и расширить грамматику,
                  False в противном случае
        """
        if not self.enabled or not self.grammar_agent:
            logger.info("AI-агенты отключены, ошибка парсинга не будет обработана")
            return False

        try:
            # Анализируем ошибку парсинга
            error_info = self.grammar_agent.analyze_parse_error(code=code_snippet, error=error)

            if not error_info:
                logger.warning("Не удалось проанализировать ошибку парсинга")
                return False

            # Пытаемся обработать неизвестную конструкцию
            success = self.grammar_agent.process_unknown_construct(code=code_snippet, error=error)

            if success:
                logger.info("Грамматика успешно расширена для поддержки новой конструкции")
                return True
            else:
                logger.warning("Не удалось расширить грамматику для поддержки новой конструкции")
                return False

        except Exception as e:
            logger.error(f"Ошибка при обработке ошибки парсинга агентом: {e}")
            return False

    def export_current_grammar(self, file_path: str) -> bool:
        """
        Экспортирует текущую грамматику в файл.

        Args:
            file_path: Путь к файлу для экспорта грамматики

        Returns:
            bool: True, если экспорт успешен, иначе False
        """
        if not self.enabled or not self.grammar_agent:
            logger.info("AI-агенты отключены, экспорт грамматики невозможен")
            return False

        try:
            return self.grammar_agent.export_grammar_to_file(file_path)
        except Exception as e:
            logger.error(f"Ошибка при экспорте грамматики: {e}")
            return False

    def shutdown(self) -> None:
        """
        Завершает работу всех агентов и освобождает ресурсы.
        """
        if self.enabled:
            logger.info("Завершение работы AI-агентов")

            # Здесь может быть логика для корректного завершения агентов,
            # например, сохранение состояния или экспорт данных

            # Освобождаем ресурсы
            self.grammar_agent = None
            self.enabled = False


# Глобальный экземпляр координатора агентов
_agent_coordinator = None


def get_agent_coordinator(enable_agents: bool = True) -> AgentCoordinator:
    """
    Возвращает глобальный экземпляр координатора агентов.

    Args:
        enable_agents: Флаг для включения/выключения AI-агентов

    Returns:
        AgentCoordinator: Экземпляр координатора агентов
    """
    global _agent_coordinator

    if _agent_coordinator is None:
        _agent_coordinator = AgentCoordinator(enable_agents=enable_agents)

    return _agent_coordinator
