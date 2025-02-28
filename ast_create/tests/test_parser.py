"""
Тесты для модуля парсера.

Этот модуль содержит тесты для проверки работы парсера и грамматики языка 1С.
"""

import os
from pathlib import Path

import pytest
from lark import Tree
from lark.exceptions import UnexpectedCharacters, UnexpectedToken

from ast_create.grammar import parser
from ast_create.utils import file_utils

# Получаем путь к текущей директории тестов
TEST_DIR = Path(__file__).parent

# Путь к примерам кода 1С
EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"


def test_parser_initialization():
    """Тест инициализации парсера."""
    p = parser.get_parser()
    assert p is not None
    assert p.grammar_path.exists()


def test_parse_simple_variable_declaration():
    """Тест парсинга объявления переменной."""
    code = "Перем Тест;"
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    var_decl = tree.children[0]
    assert var_decl.data == "var_declaration"
    assert len(var_decl.children) == 1
    assert var_decl.children[0].value == "Тест"


def test_parse_simple_assignment():
    """Тест парсинга простого присваивания."""
    code = "Переменная = 10;"
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    assignment = tree.children[0]
    assert assignment.data == "assignment"
    assert len(assignment.children) == 2
    assert assignment.children[0].value == "Переменная"

    expr = assignment.children[1]
    assert expr.data == "expression"
    assert expr.children[0].data == "literal"
    assert expr.children[0].children[0].value == "10"


def test_parse_if_statement():
    """Тест парсинга условного оператора."""
    code = """
    Если Условие > 0 Тогда
        Результат = 1;
    ИначеЕсли Условие < 0 Тогда
        Результат = -1;
    Иначе
        Результат = 0;
    КонецЕсли;
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"

    # Проверяем, что первый элемент - это if_statement
    if_stmt = tree.children[0]
    assert if_stmt.data == "if_statement"


def test_parse_procedure_declaration():
    """Тест парсинга объявления процедуры."""
    code = """
    Процедура ТестоваяПроцедура()
        Результат = 0;
    КонецПроцедуры
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"

    # Проверяем, что первый элемент - это procedure_declaration
    proc_decl = tree.children[0]
    assert proc_decl.data == "procedure_declaration"

    # Проверяем имя процедуры
    assert proc_decl.children[0].value == "ТестоваяПроцедура"


def test_parse_function_declaration():
    """Тест парсинга объявления функции."""
    code = """
    Функция ТестоваяФункция(Параметр1, Параметр2 = 10) Экспорт
        Результат = Параметр1 + Параметр2;
        Возврат Результат;
    КонецФункции
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"

    # Проверяем, что первый элемент - это function_declaration
    func_decl = tree.children[0]
    assert func_decl.data == "function_declaration"

    # Проверяем имя функции
    assert func_decl.children[0].value == "ТестоваяФункция"


def test_parse_example_file():
    """Тест парсинга примера файла с кодом 1С."""
    example_file = EXAMPLES_DIR / "example_1c_code.txt"

    # Проверяем, что файл существует
    assert example_file.exists(), f"Файл примера не найден: {example_file}"

    # Парсим файл
    tree = parser.parse_file(example_file)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) > 0


def test_syntax_error_handling():
    """Тест обработки синтаксических ошибок."""
    code = """
    Перем Тест
    Если Тест > 0 Тогда
        Результат = "отсутствует точка с запятой"
    КонецЕсли
    """

    # Ожидаем, что при парсинге будет выброшено исключение SyntaxError
    with pytest.raises((SyntaxError, UnexpectedToken, UnexpectedCharacters)):
        parser.parse(code)


if __name__ == "__main__":
    # Запуск тестов при прямом вызове файла
    pytest.main(["-v", __file__])
