"""
Тесты для модуля управления грамматикой.

Этот модуль содержит тесты для проверки работы менеджера грамматики
и системы версионирования.
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from lark import Tree

from ast_create.grammar.grammar_manager import GrammarManager, GrammarVersion, get_grammar_manager


@pytest.fixture
def temp_versions_dir():
    """Создает временную директорию для хранения версий грамматики."""
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Удаляем временную директорию после выполнения тестов
    shutil.rmtree(temp_dir)


@pytest.fixture
def grammar_manager(temp_versions_dir, monkeypatch):
    """Создает экземпляр менеджера грамматики с временной директорией для версий."""
    # Патчим конфигурацию для использования временной директории
    from ast_create.config import config

    monkeypatch.setattr(config.grammar, "version_storage", temp_versions_dir)

    # Получаем базовую грамматику из simple_parser
    from ast_create.grammar.simple_parser import GRAMMAR_1C

    # Создаем менеджер грамматики
    return GrammarManager(initial_grammar=GRAMMAR_1C)


def test_grammar_version_creation():
    """Тест создания версии грамматики."""
    # Создаем версию грамматики
    grammar = "start: statement+"
    version = GrammarVersion(grammar=grammar, description="Тестовая версия")

    # Проверяем атрибуты
    assert version.grammar == grammar
    assert version.description == "Тестовая версия"
    assert version.created_by == "manual"  # Значение по умолчанию
    assert version.version_id is not None


def test_grammar_version_to_dict():
    """Тест преобразования версии грамматики в словарь и обратно."""
    # Создаем версию грамматики
    grammar = "start: statement+"
    version = GrammarVersion(grammar=grammar, description="Тестовая версия")

    # Преобразуем в словарь
    version_dict = version.to_dict()

    # Проверяем поля словаря
    assert "grammar" in version_dict
    assert "description" in version_dict
    assert "created_by" in version_dict
    assert "version_id" in version_dict
    assert "timestamp" in version_dict

    # Создаем версию из словаря
    version2 = GrammarVersion.from_dict(version_dict)

    # Сравниваем атрибуты
    assert version2.grammar == version.grammar
    assert version2.description == version.description
    assert version2.created_by == version.created_by
    assert version2.version_id == version.version_id


def test_grammar_version_file_io(temp_versions_dir):
    """Тест сохранения и загрузки версии грамматики из файла."""
    # Создаем версию грамматики
    grammar = "start: statement+"
    version = GrammarVersion(grammar=grammar, description="Тестовая версия")

    # Определяем путь для сохранения
    file_path = Path(temp_versions_dir) / f"{version.version_id}.json"

    # Сохраняем версию в файл
    success = version.save_to_file(file_path)
    assert success
    assert file_path.exists()

    # Загружаем версию из файла
    loaded_version = GrammarVersion.load_from_file(file_path)

    # Сравниваем атрибуты
    assert loaded_version.grammar == version.grammar
    assert loaded_version.description == version.description
    assert loaded_version.created_by == version.created_by
    assert loaded_version.version_id == version.version_id


def test_grammar_manager_initialization(grammar_manager):
    """Тест инициализации менеджера грамматики."""
    # Проверяем, что менеджер создан успешно
    assert grammar_manager is not None

    # Проверяем, что у менеджера есть текущая версия
    assert grammar_manager.current_version is not None

    # Проверяем, что создан парсер
    assert grammar_manager.lark_parser is not None


def test_grammar_manager_parse(grammar_manager):
    """Тест парсинга кода с использованием менеджера грамматики."""
    # Простой код для парсинга
    code = "Перем x;"

    # Парсим код
    tree = grammar_manager.parse(code)

    # Проверяем результат
    assert isinstance(tree, Tree)
    assert tree.data == "start"
    assert len(tree.children) == 1

    var_decl = tree.children[0]
    assert var_decl.data == "var_declaration"
    assert var_decl.children[0].value == "x"


def test_grammar_manager_add_version(grammar_manager):
    """Тест добавления новой версии грамматики."""
    # Запоминаем текущую версию
    current_version_id = grammar_manager.current_version.version_id

    # Добавляем новую версию
    new_grammar = grammar_manager.current_version.grammar + "\n// Комментарий для новой версии"
    new_version = grammar_manager.add_version(
        grammar=new_grammar, description="Новая тестовая версия", created_by="test"
    )

    # Проверяем, что новая версия создана
    assert new_version is not None
    assert new_version.version_id != current_version_id

    # Проверяем, что текущая версия обновлена
    assert grammar_manager.current_version.version_id == new_version.version_id

    # Проверяем, что новая версия сохранена в файл
    version_file = grammar_manager.versions_path / f"{new_version.version_id}.json"
    assert version_file.exists()


def test_grammar_manager_rollback(grammar_manager):
    """Тест отката к предыдущей версии грамматики."""
    # Запоминаем текущую версию
    current_version = grammar_manager.current_version

    # Добавляем новую версию
    new_grammar = grammar_manager.current_version.grammar + "\n// Комментарий для новой версии"
    new_version = grammar_manager.add_version(
        grammar=new_grammar, description="Новая тестовая версия", created_by="test"
    )

    # Убеждаемся, что новая версия стала текущей
    assert grammar_manager.current_version.version_id == new_version.version_id

    # Откатываемся к предыдущей версии
    success = grammar_manager.rollback_to_version(current_version.version_id)

    # Проверяем результат отката
    assert success
    assert grammar_manager.current_version.version_id == current_version.version_id


def test_grammar_manager_extend_grammar(grammar_manager):
    """Тест расширения грамматики новыми правилами."""
    # Начальное количество версий
    initial_versions_count = len(grammar_manager.get_all_versions())

    # Новое правило для расширения
    new_rule = """
    // Правило для цикла "Для каждого"
    foreach_statement: "Для" "каждого" IDENTIFIER "Из" expression "Цикл" statement+ "КонецЦикла" ";"?
    
    // UPDATE_RULE: statement |= foreach_statement
    """

    # Расширяем грамматику
    success = grammar_manager.extend_grammar(new_rule, "Добавление цикла 'Для каждого'")

    # Проверяем результат
    assert success

    # Проверяем, что была создана новая версия
    assert len(grammar_manager.get_all_versions()) == initial_versions_count + 1

    # Проверяем, что новая грамматика работает
    code = """
    Перем items;
    Для каждого item Из items Цикл
        item = item + 1;
    КонецЦикла;
    """

    # Парсим код с новой конструкцией
    tree = grammar_manager.parse(code)
    assert isinstance(tree, Tree)


def test_grammar_manager_backup(grammar_manager, temp_versions_dir):
    """Тест создания резервной копии версий грамматики."""
    # Добавляем несколько версий
    for i in range(3):
        new_grammar = grammar_manager.current_version.grammar + f"\n// Комментарий для версии {i}"
        grammar_manager.add_version(
            grammar=new_grammar, description=f"Версия {i}", created_by="test"
        )

    # Создаем директорию для резервной копии
    backup_dir = Path(temp_versions_dir) / "backup"

    # Делаем резервную копию
    success = grammar_manager.backup_all_versions(backup_dir)

    # Проверяем результат
    assert success
    assert backup_dir.exists()

    # Проверяем, что файлы скопированы
    version_files = list(grammar_manager.versions_path.glob("*.json"))
    backup_files = list(backup_dir.glob("*.json"))

    # Должны быть все версии + info файл
    assert len(backup_files) == len(version_files) + 1

    # Проверяем наличие info файла
    assert (backup_dir / "backup_info.json").exists()


def test_singleton_grammar_manager():
    """Тест, что get_grammar_manager всегда возвращает один и тот же экземпляр."""
    # Получаем экземпляр менеджера
    manager1 = get_grammar_manager()

    # Получаем еще один экземпляр
    manager2 = get_grammar_manager()

    # Проверяем, что это один и тот же объект
    assert manager1 is manager2
