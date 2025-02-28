"""
Конфигурация проекта.

Модуль содержит настройки для различных компонентов проекта,
включая грамматику, парсер и AI-агенты.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Корневая директория проекта
PROJECT_ROOT = Path(__file__).parent.parent.parent


class GrammarConfig(BaseModel):
    """Конфигурация грамматики и парсера."""

    # Тип используемого парсера (lalr, earley)
    parser: str = "lalr"

    # Обработка неоднозначностей (выбор первого варианта)
    ambiguity: str = "resolve"

    # Путь к файлу с базовой грамматикой
    base_grammar_file: str = str(PROJECT_ROOT / "ast_create" / "grammar" / "1c_base.lark")

    # Директория для хранения версий грамматики
    version_storage: str = str(PROJECT_ROOT / "ast_create" / "grammar" / "versions")

    # Максимальное количество хранимых версий (0 - без ограничения)
    max_versions: int = 0

    # Включить автоматическое резервное копирование версий
    auto_backup: bool = True

    # Директория для резервных копий
    backup_dir: str = str(PROJECT_ROOT / "ast_create" / "grammar" / "backups")

    # Интервал резервного копирования (в днях)
    backup_interval_days: int = 7

    # Включить журналирование изменений грамматики
    log_grammar_changes: bool = True

    # Файл журнала изменений
    changelog_file: str = str(PROJECT_ROOT / "ast_create" / "grammar" / "grammar_changelog.md")


class AgentConfig(BaseModel):
    """Конфигурация AI-агентов."""

    # Включить AI-агенты
    enabled: bool = True

    # Автоматическое обновление грамматики при ошибках парсинга
    auto_update_grammar: bool = True

    # Максимальное количество попыток исправления ошибки
    max_correction_attempts: int = 3

    # Минимальный размер кода для анализа контекста (в символах)
    min_context_size: int = 200

    # Максимальный размер кода для анализа контекста (в символах)
    max_context_size: int = 5000

    # Включить логирование работы агентов
    log_agent_activity: bool = True

    # Файл журнала работы агентов
    agent_log_file: str = str(PROJECT_ROOT / "ast_create" / "agents" / "agent_activity.log")

    # Директория для сохранения обучающих данных
    training_data_dir: str = str(PROJECT_ROOT / "ast_create" / "agents" / "training_data")


class LoggingConfig(BaseModel):
    """Конфигурация логирования."""

    # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level: str = "INFO"

    # Формат сообщений лога
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Директория для файлов логов
    log_dir: str = str(PROJECT_ROOT / "logs")

    # Файл основного лога
    main_log_file: str = str(PROJECT_ROOT / "logs" / "ast_create.log")

    # Максимальный размер файла лога (в байтах) перед ротацией
    max_log_size: int = 10 * 1024 * 1024  # 10 МБ

    # Количество файлов лога для хранения
    backup_count: int = 5

    # Включить логирование в консоль
    console_logging: bool = True


class AppConfig(BaseModel):
    """Основная конфигурация приложения."""

    # Название приложения
    name: str = "AST Creator для 1C"

    # Версия приложения
    version: str = "0.2.0"

    # Режим отладки
    debug: bool = False

    # Секции конфигурации
    grammar: GrammarConfig = Field(default_factory=GrammarConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


# Создаем экземпляр конфигурации
config = AppConfig()


def init_config_directories():
    """Инициализирует директории, указанные в конфигурации."""
    directories = [
        Path(config.grammar.version_storage),
        Path(config.grammar.backup_dir),
        Path(config.agent.training_data_dir),
        Path(config.logging.log_dir),
    ]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """Настраивает систему логирования на основе конфигурации."""
    import logging
    from logging.handlers import RotatingFileHandler

    # Корневой логгер
    root_logger = logging.getLogger()

    # Уровень логирования
    level = getattr(logging, config.logging.level)
    root_logger.setLevel(level)

    # Формат сообщений
    formatter = logging.Formatter(config.logging.format)

    # Создаем директорию для логов, если она не существует
    log_dir = Path(config.logging.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Файловый обработчик
    file_handler = RotatingFileHandler(
        config.logging.main_log_file,
        maxBytes=config.logging.max_log_size,
        backupCount=config.logging.backup_count,
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Консольный обработчик
    if config.logging.console_logging:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # Логгер для модуля ast_create
    ast_logger = logging.getLogger("ast_create")
    ast_logger.setLevel(level)

    # Возвращаем настроенный логгер
    return ast_logger


# Выполняем инициализацию при импорте модуля
init_config_directories()
logger = setup_logging()
