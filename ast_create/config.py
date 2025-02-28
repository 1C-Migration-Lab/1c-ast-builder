"""
Модуль конфигурации проекта.

Этот модуль содержит классы и функции для работы с конфигурацией проекта,
включая загрузку параметров из файлов, переменных окружения и их валидацию.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
from pydantic import BaseModel, Field


class LogConfig(BaseModel):
    """Конфигурация логирования."""
    level: str = Field(default="INFO", description="Уровень логирования")
    format: str = Field(
        default="{time} | {level} | {message}",
        description="Формат сообщений лога"
    )
    file: Optional[str] = Field(default=None, description="Путь к файлу лога")


class AgentsConfig(BaseModel):
    """Конфигурация AI-агентов."""
    api_key: Optional[str] = Field(
        default=None,
        description="API ключ для LLM сервиса"
    )
    model: str = Field(
        default="gpt-4",
        description="Модель для использования"
    )
    max_tokens: int = Field(
        default=2000,
        description="Максимальное количество токенов для запроса"
    )
    temperature: float = Field(
        default=0.7,
        description="Температура генерации (креативность)"
    )


class GrammarConfig(BaseModel):
    """Конфигурация грамматики."""
    parser: str = Field(
        default="lalr",
        description="Тип парсера (lalr, earley)"
    )
    ambiguity: str = Field(
        default="resolve",
        description="Стратегия обработки неоднозначностей"
    )
    grammar_path: str = Field(
        default="ast_create/grammar/1c_base.lark",
        description="Путь к базовому файлу грамматики"
    )
    version_storage: str = Field(
        default="versions",
        description="Путь к хранилищу версий грамматики"
    )


class AppConfig(BaseModel):
    """Основная конфигурация приложения."""
    log: LogConfig = Field(default_factory=LogConfig)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    grammar: GrammarConfig = Field(default_factory=GrammarConfig)
    debug: bool = Field(default=False, description="Режим отладки")
    max_file_size: int = Field(
        default=10*1024*1024,  # 10 MB
        description="Максимальный размер обрабатываемого файла в байтах"
    )


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Загружает конфигурацию из файла и/или переменных окружения.

    Args:
        config_path: Путь к файлу конфигурации (YAML или JSON)

    Returns:
        AppConfig: Объект конфигурации
    """
    config_dict: Dict[str, Any] = {}

    # Загрузка из файла, если указан
    if config_path:
        path = Path(config_path)
        if path.exists():
            try:
                if path.suffix.lower() in ('.yaml', '.yml'):
                    with open(path, 'r', encoding='utf-8') as f:
                        config_dict = yaml.safe_load(f)
                elif path.suffix.lower() == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        config_dict = json.load(f)
                else:
                    logger.warning(f"Неподдерживаемый формат файла: {path.suffix}")
            except Exception as e:
                logger.error(f"Ошибка при загрузке конфигурации из {path}: {e}")
        else:
            logger.warning(f"Файл конфигурации не найден: {path}")

    # Обновление из переменных окружения
    # Формат: AST_CREATE_SECTION_KEY=value
    # Например: AST_CREATE_AGENTS_API_KEY=my-api-key
    env_prefix = "AST_CREATE_"
    for env_name, env_value in os.environ.items():
        if env_name.startswith(env_prefix):
            # Удаляем префикс и разбиваем по '_'
            parts = env_name[len(env_prefix):].lower().split('_')
            
            # Заполняем конфигурацию
            current = config_dict
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Устанавливаем значение
            current[parts[-1]] = env_value

    # Создаём объект конфигурации
    return AppConfig(**config_dict)


# Глобальный экземпляр конфигурации
config = load_config()


def setup_logger():
    """Настраивает логирование согласно конфигурации."""
    logger.remove()  # Удаляем стандартный обработчик
    
    # Настраиваем вывод в консоль
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=config.log.level,
        format=config.log.format
    )
    
    # Добавляем вывод в файл, если он указан
    if config.log.file:
        logger.add(
            sink=config.log.file,
            level=config.log.level,
            format=config.log.format,
            rotation="10 MB",  # Ротация по размеру
            compression="zip"  # Сжатие старых логов
        ) 