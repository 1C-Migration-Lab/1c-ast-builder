"""
Модуль парсера для языка 1С.

Этот модуль содержит классы и функции для парсинга кода на языке 1С
с использованием грамматики Lark.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from lark import Lark, Tree, UnexpectedCharacters, UnexpectedToken
from loguru import logger

from ast_create.config import config


class Parser:
    """
    Класс для парсинга кода на языке 1С.

    Attributes:
        grammar_path (Path): Путь к файлу грамматики.
        _parser (Lark): Экземпляр парсера Lark.
    """

    def __init__(self, grammar_path: Optional[Union[str, Path]] = None):
        """
        Инициализирует парсер с заданной грамматикой.

        Args:
            grammar_path: Путь к файлу грамматики Lark.
                          Если не указан, используется путь из конфигурации.
        """
        if grammar_path is None:
            # Используем путь из конфигурации
            grammar_path = config.grammar.grammar_path

        self.grammar_path = Path(grammar_path)

        # Проверяем существование файла грамматики
        if not self.grammar_path.exists():
            raise FileNotFoundError(f"Файл грамматики не найден: {self.grammar_path}")

        logger.info(f"Инициализация парсера с грамматикой: {self.grammar_path}")

        # Загружаем грамматику
        with open(self.grammar_path, "r", encoding="utf-8") as f:
            grammar_content = f.read()

        # Создаем парсер
        self._parser = Lark(
            grammar_content,
            parser=config.grammar.parser,
            ambiguity=config.grammar.ambiguity,
            debug=config.debug,
        )

        logger.debug("Парсер успешно инициализирован")

    def parse(self, code: str) -> Tree:
        """
        Парсит код на языке 1С и возвращает дерево разбора.

        Args:
            code: Исходный код на языке 1С.

        Returns:
            Tree: Дерево разбора Lark.

        Raises:
            SyntaxError: Если в коде есть синтаксические ошибки.
        """
        try:
            logger.debug("Начало парсинга кода")
            tree = self._parser.parse(code)
            logger.debug("Парсинг успешно завершен")
            return tree
        except UnexpectedToken as e:
            # Обработка ошибки неожиданного токена
            error_context = self._get_error_context(code, e.line, e.column)
            error_message = (
                f"Синтаксическая ошибка: неожиданный токен '{e.token}' "
                f"в строке {e.line}, позиция {e.column}.\n"
                f"Ожидались: {', '.join(e.expected)}\n"
                f"Контекст:\n{error_context}"
            )
            logger.error(error_message)
            raise SyntaxError(error_message) from e
        except UnexpectedCharacters as e:
            # Обработка ошибки неожиданных символов
            error_context = self._get_error_context(code, e.line, e.column)
            error_message = (
                f"Синтаксическая ошибка: неожиданный символ '{e.char}' "
                f"в строке {e.line}, позиция {e.column}.\n"
                f"Контекст:\n{error_context}"
            )
            logger.error(error_message)
            raise SyntaxError(error_message) from e
        except Exception as e:
            # Обработка других ошибок
            logger.error(f"Ошибка при парсинге: {e}")
            raise

    def parse_file(self, file_path: Union[str, Path]) -> Tree:
        """
        Парсит файл с кодом на языке 1С.

        Args:
            file_path: Путь к файлу с исходным кодом.

        Returns:
            Tree: Дерево разбора Lark.

        Raises:
            FileNotFoundError: Если файл не найден.
            SyntaxError: Если в коде есть синтаксические ошибки.
        """
        file_path = Path(file_path)

        # Проверяем существование файла
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        logger.info(f"Парсинг файла: {file_path}")

        # Читаем файл
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Парсим код
        return self.parse(code)

    def _get_error_context(self, code: str, line: int, column: int, context_lines: int = 3) -> str:
        """
        Возвращает контекст ошибки в коде.

        Args:
            code: Исходный код.
            line: Номер строки с ошибкой.
            column: Позиция символа с ошибкой.
            context_lines: Количество строк контекста до и после ошибки.

        Returns:
            str: Фрагмент кода с выделенной ошибкой.
        """
        lines = code.split("\n")
        start_line = max(0, line - context_lines - 1)
        end_line = min(len(lines), line + context_lines)

        result = []
        for i, l in enumerate(lines[start_line:end_line], start=start_line + 1):
            # Добавляем номер строки и саму строку
            result.append(f"{i}: {l}")

            # Если это строка с ошибкой, добавляем указатель
            if i == line:
                result.append(" " * (len(str(i)) + 2 + column) + "^")

        return "\n".join(result)


# Создаем глобальный экземпляр парсера
parser = None


def get_parser() -> Parser:
    """
    Возвращает глобальный экземпляр парсера, создавая его при необходимости.

    Returns:
        Parser: Экземпляр парсера.
    """
    global parser
    if parser is None:
        parser = Parser()
    return parser


def parse(code: str) -> Tree:
    """
    Парсит код на языке 1С, используя глобальный экземпляр парсера.

    Args:
        code: Исходный код на языке 1С.

    Returns:
        Tree: Дерево разбора Lark.
    """
    return get_parser().parse(code)


def parse_file(file_path: Union[str, Path]) -> Tree:
    """
    Парсит файл с кодом на языке 1С, используя глобальный экземпляр парсера.

    Args:
        file_path: Путь к файлу с исходным кодом.

    Returns:
        Tree: Дерево разбора Lark.
    """
    return get_parser().parse_file(file_path)
