"""
Модуль AI-агента для работы с грамматикой.

Этот модуль содержит классы для автоматического расширения грамматики
с использованием AI для обработки новых конструкций языка 1С.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from loguru import logger

# Импортируем GrammarManager
from ast_create.grammar.grammar_manager import get_grammar_manager


class GrammarAgent:
    """
    Базовый класс для AI-агента, работающего с грамматикой.
    
    Attributes:
        parser: Экземпляр парсера 1С.
        grammar_manager: Экземпляр менеджера грамматики.
    """
    
    def __init__(self, current_grammar=None):
        """Инициализация агента."""
        self.grammar_manager = get_grammar_manager()
        
        # Отложенный импорт во избежание циклической зависимости
        self.parser = None
        
        logger.info("Инициализирован AI-агент для работы с грамматикой")
    
    def analyze_parse_error(self, code: str, error: Exception) -> Dict:
        """
        Анализирует ошибку парсинга для выявления неизвестных конструкций.
        
        Args:
            code: Код на языке 1С, вызвавший ошибку
            error: Исключение, возникшее при парсинге
            
        Returns:
            Dict: Информация о неизвестной конструкции
        """
        # Инициализируем парсер при первом использовании (отложенная инициализация)
        if self.parser is None:
            from ast_create.grammar.parser import get_parser
            self.parser = get_parser(use_agents=False)  # Важно! use_agents=False для избежания цикла
        
        # Базовая информация об ошибке
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "code_context": "",
            "likely_construct": "",
            "suggested_rule": ""
        }
        
        # Получаем контекст ошибки
        if hasattr(error, "line") and hasattr(error, "column"):
            line = getattr(error, "line")
            column = getattr(error, "column")
            
            # Получаем строку, вызвавшую ошибку
            lines = code.split("\n")
            if 0 <= line - 1 < len(lines):
                error_line = lines[line - 1]
                error_info["code_context"] = error_line
                
                # Получаем фрагмент кода вокруг ошибки (+-2 строки)
                start_line = max(0, line - 3)
                end_line = min(len(lines), line + 2)
                error_info["code_snippet"] = "\n".join(lines[start_line:end_line])
        
        # В дальнейшем здесь будет более сложная логика анализа ошибки
        # с использованием AI для определения неизвестной конструкции
        
        return error_info
    
    def generate_grammar_rule(self, unknown_construct: Dict) -> Optional[str]:
        """
        Генерирует правило грамматики для неизвестной конструкции.
        
        В реальной реализации этот метод будет использовать AI
        для генерации правила грамматики.
        
        Args:
            unknown_construct: Информация о неизвестной конструкции
            
        Returns:
            Optional[str]: Сгенерированное правило грамматики или None
        """
        # Заглушка для демонстрации
        # В реальной реализации здесь будет вызов LLM API
        
        logger.info(f"Генерация правила грамматики для: {unknown_construct.get('likely_construct')}")
        
        # Примитивная заглушка для демонстрации
        if "Для каждого" in unknown_construct.get("code_context", ""):
            return """
            // Правило для цикла "Для каждого"
            foreach_statement: "Для" "каждого" IDENTIFIER "Из" expression "Цикл" statement+ "КонецЦикла" ";"?
            
            // Обновление правила statement
            ?statement: var_declaration | assignment | if_statement | procedure_declaration | function_declaration | for_statement | while_statement | try_except_statement | return_statement | call_statement | foreach_statement
            """
        
        # В реальной реализации здесь будет сложная логика,
        # использующая AI для анализа неизвестной конструкции
        # и генерации соответствующего правила грамматики
        
        return None
    
    def validate_grammar_rule(self, new_rule: str) -> Tuple[bool, str]:
        """
        Проверяет корректность нового правила грамматики.
        
        Args:
            new_rule: Новое правило грамматики
            
        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        # Получаем текущую грамматику
        current_grammar = self.grammar_manager.current_version.grammar
        
        # Пробуем объединить правила
        try:
            combined_grammar = f"{current_grammar}\n\n// Новое правило\n{new_rule}"
            
            # Пробуем создать временный парсер с новой грамматикой
            from lark import Lark
            temp_parser = Lark(combined_grammar, start="start", parser="lalr")
            
            # Проверяем работоспособность на простом примере
            test_code = "Перем x;"
            temp_parser.parse(test_code)
            
            return True, "Правило грамматики прошло валидацию"
        except Exception as e:
            return False, f"Ошибка валидации правила: {e}"
    
    def process_unknown_construct(self, code: str, error: Exception) -> bool:
        """
        Обрабатывает неизвестную конструкцию и расширяет грамматику.
        
        Args:
            code: Код на языке 1С, вызвавший ошибку
            error: Исключение, возникшее при парсинге
            
        Returns:
            bool: True, если грамматика успешно расширена, иначе False
        """
        try:
            # Анализируем ошибку
            unknown_construct = self.analyze_parse_error(code, error)
            
            # Генерируем правило грамматики
            new_rule = self.generate_grammar_rule(unknown_construct)
            if not new_rule:
                logger.warning("Не удалось сгенерировать правило грамматики")
                return False
            
            # Проверяем корректность правила
            is_valid, message = self.validate_grammar_rule(new_rule)
            if not is_valid:
                logger.error(f"Ошибка валидации правила: {message}")
                return False
            
            # Расширяем грамматику
            description = f"Автоматическое расширение для конструкции: {unknown_construct.get('likely_construct')}"
            success = self.grammar_manager.extend_grammar(new_rule, description)
            
            if success:
                logger.info(f"Грамматика успешно расширена: {description}")
            else:
                logger.error("Ошибка при расширении грамматики")
            
            return success
        except Exception as e:
            logger.error(f"Ошибка при обработке неизвестной конструкции: {e}")
            return False
    
    def export_grammar_to_file(self, file_path: Optional[Union[str, Path]] = None) -> bool:
        """
        Экспортирует текущую грамматику в файл.
        
        Args:
            file_path: Путь к файлу для сохранения грамматики
            
        Returns:
            bool: True, если операция успешна, иначе False
        """
        try:
            # Если путь не указан, используем путь по умолчанию
            if file_path is None:
                from ast_create.grammar.simple_parser import grammar_path
                file_path = grammar_path
            
            # Получаем текущую грамматику
            current_grammar = self.grammar_manager.current_version.grammar
            
            # Сохраняем в файл
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(current_grammar)
            
            logger.info(f"Грамматика успешно экспортирована в файл: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при экспорте грамматики: {e}")
            return False 