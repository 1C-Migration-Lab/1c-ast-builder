"""
Модуль парсера для языка 1С.

Этот модуль реализует парсер для языка 1С:Предприятие,
используя новую систему версионирования грамматики и
поддержку расширения правил через AI-агенты.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from lark import Lark, Token, Tree, exceptions

from ast_create.agents.agent_coordinator import get_agent_coordinator
from ast_create.config import config
from ast_create.grammar.grammar_manager import get_grammar_manager

# Настройка логирования
logger = logging.getLogger(__name__)


class Parser:
    """
    Парсер для языка 1С:Предприятие.
    
    Класс предоставляет API для разбора исходного кода на языке 1С
    и построения синтаксического дерева. Использует систему
    версионирования грамматики и поддержку AI-агентов для
    автоматического расширения грамматики.
    
    Атрибуты:
        grammar_manager: Менеджер грамматики
        agent_coordinator: Координатор AI-агентов
    """
    
    def __init__(self, use_agents: bool = True):
        """
        Инициализирует парсер.
        
        Args:
            use_agents: Флаг для включения/выключения AI-агентов
        """
        # Получаем менеджер грамматики
        self.grammar_manager = get_grammar_manager()
        
        # Получаем координатор агентов
        self.agent_coordinator = get_agent_coordinator(enable_agents=use_agents)
        
        logger.info(f"Парсер инициализирован (AI-агенты: {'включены' if use_agents else 'отключены'})")
    
    def parse(self, code: str, max_correction_attempts: int = None) -> Tree:
        """
        Разбирает исходный код на языке 1С.
        
        Args:
            code: Исходный код на языке 1С
            max_correction_attempts: Максимальное количество попыток исправления ошибок
                (если None, используется значение из конфигурации)
                
        Returns:
            Tree: Синтаксическое дерево разбора
            
        Raises:
            SyntaxError: Если код содержит синтаксические ошибки
        """
        if max_correction_attempts is None:
            max_correction_attempts = config.agents.max_tokens
        
        # Счетчик попыток исправления ошибок
        correction_attempts = 0
        
        while True:
            try:
                # Пытаемся разобрать код
                tree = self.grammar_manager.parse(code)
                
                # Если успешно, возвращаем дерево
                return tree
                
            except (exceptions.UnexpectedToken, exceptions.UnexpectedCharacters, SyntaxError) as e:
                # Логируем ошибку
                logger.error(f"Ошибка при разборе кода: {e}")
                
                # Если включена опция автоматического улучшения грамматики и есть AI-агенты
                if config.agents.max_tokens > 0 and self.agent_coordinator.enabled:
                    # Пытаемся улучшить грамматику
                    correction_result = self.agent_coordinator.process_parse_error(code, str(e))
                    
                    if correction_result and correction_result.get("success", False):
                        # Если успешно исправили, пытаемся снова разобрать код
                        correction_attempts += 1
                        logger.info(f"Попытка исправления #{correction_attempts}: грамматика обновлена")
                        continue
                
                # Если достигли максимального числа попыток или не смогли исправить,
                # выбрасываем исключение
                raise SyntaxError(str(e))
            
            except Exception as e:
                # Обрабатываем прочие ошибки
                logger.error(f"Неожиданная ошибка при разборе кода: {e}")
                raise
    
    def try_parse(self, code: str) -> Tuple[bool, Optional[Tree], Optional[Exception]]:
        """
        Пытается разобрать код, возвращая результат и возможную ошибку.
        
        Эта функция не выбрасывает исключения, а возвращает информацию об ошибке,
        что удобно для проверки кода без прерывания выполнения программы.
        
        Args:
            code: Исходный код на языке 1С
            
        Returns:
            Tuple[bool, Optional[Tree], Optional[Exception]]: Кортеж из флага успеха,
                дерева разбора (если успешно) и исключения (если произошла ошибка)
        """
        try:
            tree = self.parse(code)
            return True, tree, None
        except Exception as e:
            return False, None, e
    
    def export_grammar(self, file_path: Union[str, Path]) -> bool:
        """
        Экспортирует текущую грамматику в файл.
        
        Args:
            file_path: Путь к файлу для экспорта
            
        Returns:
            bool: True, если экспорт выполнен успешно, иначе False
        """
        try:
            # Получаем текущую грамматику
            current_grammar = self.grammar_manager.current_version.grammar
            
            # Преобразуем путь в объект Path
            file_path = Path(file_path)
            
            # Создаем директорию, если она не существует
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Записываем грамматику в файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(current_grammar)
            
            logger.info(f"Грамматика экспортирована в файл {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при экспорте грамматики: {e}")
            return False
    
    def get_available_versions(self) -> List[Dict[str, Any]]:
        """
        Возвращает список доступных версий грамматики.
        
        Returns:
            List[Dict[str, Any]]: Список словарей с информацией о версиях
        """
        # Получаем все версии грамматики
        versions = self.grammar_manager.get_all_versions()
        
        # Преобразуем в список словарей с метаинформацией
        return [
            {
                "version_id": v.version_id,
                "timestamp": v.timestamp,
                "description": v.description,
                "created_by": v.created_by,
                "is_current": v.version_id == self.grammar_manager.current_version.version_id
            }
            for v in versions
        ]
    
    def rollback_to_version(self, version_id: str) -> bool:
        """
        Откатывает грамматику к указанной версии.
        
        Args:
            version_id: Идентификатор версии
            
        Returns:
            bool: True, если откат выполнен успешно, иначе False
        """
        return self.grammar_manager.rollback_to_version(version_id)
    
    def get_parser_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о текущем состоянии парсера.
        
        Returns:
            Dict[str, Any]: Словарь с информацией о парсере
        """
        current_version = self.grammar_manager.current_version
        
        return {
            "current_version": {
                "version_id": current_version.version_id,
                "timestamp": current_version.timestamp,
                "description": current_version.description,
                "created_by": current_version.created_by
            },
            "versions_count": len(self.grammar_manager.get_all_versions()),
            "ai_agents_enabled": self.agent_coordinator.enabled,
            "parser_type": config.grammar.parser,
            "ambiguity_resolution": config.grammar.ambiguity
        }

# Глобальный экземпляр парсера
_parser = None

def get_parser(use_agents: bool = True) -> Parser:
    """
    Возвращает глобальный экземпляр парсера.
    
    Args:
        use_agents: Флаг для включения/выключения AI-агентов
        
    Returns:
        Parser: Экземпляр парсера
    """
    global _parser
    
    if _parser is None:
        _parser = Parser(use_agents=use_agents)
    
    return _parser
