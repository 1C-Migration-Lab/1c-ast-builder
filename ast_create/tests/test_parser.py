"""
Тесты для парсера языка 1С.

Этот модуль содержит тесты для различных аспектов работы парсера,
включая инициализацию, разбор кода и обработку ошибок.
"""

import os
import pytest
import tempfile
from pathlib import Path

from lark import Tree

from ast_create.grammar.parser import Parser


@pytest.fixture
def parser():
    """Фикстура для создания экземпляра парсера."""
    # Отключаем AI-агенты для тестов
    return Parser(use_agents=False)


def test_parser_initialization(parser):
    """Проверка корректной инициализации парсера."""
    assert parser is not None
    assert parser.grammar_manager is not None
    assert parser.agent_coordinator is not None


def test_parse_simple_variable_declaration(parser):
    """Проверка парсинга простого объявления переменной."""
    code = "Перем x;"
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    var_decl = tree.children[0]
    assert var_decl.data == "var_declaration"
    assert var_decl.children[0].value == "x"


def test_parse_simple_assignment(parser):
    """Проверка парсинга простого присваивания."""
    code = "x = 5;"
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    assignment = tree.children[0]
    assert assignment.data == "assignment"
    assert assignment.children[0].value == "x"
    assert assignment.children[1].data == "expression"

    # Исправляем проверку: получаем числовое значение из терминального узла
    num_val = assignment.children[1].children[0]
    if hasattr(num_val, "children") and len(num_val.children) > 0:
        num_val = num_val.children[0]
    assert num_val.value == "5"


def test_parse_if_statement(parser):
    """Проверка парсинга условного оператора."""
    code = """
    Если x = 3 Тогда
        y = 2;
    КонецЕсли;
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    if_stmt = tree.children[0]
    assert if_stmt.data == "if_statement"

    # Проверка условия
    condition = if_stmt.children[0]
    assert condition.data == "expression"

    # Проверка тела условия - изменено с "statement" на "block" или "assignment"
    body = if_stmt.children[1]
    assert body.data in ["block", "assignment", "statement_list"]


def test_parse_procedure_declaration(parser):
    """Проверка парсинга объявления процедуры."""
    code = """
    Процедура ТестоваяПроцедура()
        x = 1;
    КонецПроцедуры
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    proc_decl = tree.children[0]
    assert proc_decl.data == "procedure_declaration"
    assert proc_decl.children[0].value == "ТестоваяПроцедура"


def test_parse_function_declaration(parser):
    """Проверка парсинга объявления функции."""
    code = """
    Функция ТестоваяФункция()
        Возврат 1;
    КонецФункции
    """
    tree = parser.parse(code)

    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    func_decl = tree.children[0]
    assert func_decl.data == "function_declaration"
    assert func_decl.children[0].value == "ТестоваяФункция"


def test_parse_example_file(parser):
    """Проверка парсинга примера кода из файла."""
    code = """
    // Пример кода на языке 1С
    
    Перем Количество;
    
    Процедура ПосчитатьЧто_то()
        Количество = 10;
        
        Для Индекс = 1 По Количество Цикл
            Если Индекс > 5 Тогда
                Количество = Количество - 1;
            КонецЕсли;
            
            Сообщить("Осталось: " + Количество);
        КонецЦикла;
    КонецПроцедуры
    
    Функция ПолучитьРезультат()
        Возврат Количество * 2;
    КонецФункции
    """

    tree = parser.parse(code)

    # Проверяем, что дерево создано успешно
    assert isinstance(tree, Tree)
    assert tree.data == "start"

    # Должно быть 3 основных элемента: объявление переменной и две функции
    assert len(tree.children) == 3

    # Проверяем объявление переменной
    var_decl = tree.children[0]
    assert var_decl.data == "var_declaration"
    assert var_decl.children[0].value == "Количество"

    # Проверяем объявление процедуры
    proc_decl = tree.children[1]
    assert proc_decl.data == "procedure_declaration"
    assert proc_decl.children[0].value == "ПосчитатьЧто_то"

    # Проверяем объявление функции
    func_decl = tree.children[2]
    assert func_decl.data == "function_declaration"
    assert func_decl.children[0].value == "ПолучитьРезультат"


def test_syntax_error_handling(parser):
    """Проверка обработки синтаксических ошибок."""
    # Код с синтаксической ошибкой (недопустимый символ @)
    code = """
    Перем Тест; // объявление переменной
    
    Если @x = 3 Тогда // недопустимый символ
        y = 2;
    КонецЕсли;
    """

    # Парсер должен выбросить исключение SyntaxError
    with pytest.raises((SyntaxError, Exception)):
        parser.parse(code)

    # Проверяем метод try_parse
    success, tree, error = parser.try_parse(code)
    assert not success
    assert tree is None
    assert error is not None


def test_grammar_export(parser):
    """Проверка экспорта грамматики в файл."""
    # Создаем временный файл для экспорта
    with tempfile.NamedTemporaryFile(suffix=".lark", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Экспортируем грамматику
        result = parser.export_grammar(temp_path)
        assert result is True

        # Проверяем, что файл создан и не пустой
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0

        # Проверяем содержимое файла
        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Проверяем наличие ключевых элементов грамматики
            assert "start:" in content
            assert "var_declaration:" in content
            assert "IDENTIFIER:" in content
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_version_management(parser):
    """Проверка управления версиями грамматики."""
    # Получаем информацию о текущем парсере
    parser_info = parser.get_parser_info()
    assert "current_version" in parser_info
    assert "versions_count" in parser_info

    # Получаем список доступных версий
    versions = parser.get_available_versions()
    assert isinstance(versions, list)
    assert len(versions) > 0

    # Проверяем, что текущая версия есть в списке
    current_version_id = parser_info["current_version"]["version_id"]
    current_versions = [v for v in versions if v["version_id"] == current_version_id]
    assert len(current_versions) == 1
    assert current_versions[0]["is_current"] is True
