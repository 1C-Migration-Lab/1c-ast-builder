"""
Утилиты для работы с файлами.

Этот модуль содержит функции для чтения, записи и обработки файлов
с исходным кодом 1С и другими данными проекта.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from loguru import logger

from ast_create.config import config


def read_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Читает содержимое файла.

    Args:
        file_path: Путь к файлу
        encoding: Кодировка файла (по умолчанию utf-8)

    Returns:
        str: Содержимое файла

    Raises:
        FileNotFoundError: Если файл не найден
        PermissionError: Если нет прав на чтение файла
        UnicodeDecodeError: Если файл не может быть декодирован с указанной кодировкой
    """
    file_path = Path(file_path)

    # Проверяем существование файла
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Проверяем размер файла
    if file_path.stat().st_size > config.max_file_size:
        raise ValueError(
            f"Размер файла превышает максимально допустимый "
            f"({file_path.stat().st_size} > {config.max_file_size} байт)"
        )

    # Читаем файл
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        # Пробуем другие популярные кодировки
        for alt_encoding in ["cp1251", "latin-1", "cp866"]:
            try:
                logger.warning(
                    f"Не удалось прочитать файл с кодировкой {encoding}, " f"пробуем {alt_encoding}"
                )
                with open(file_path, "r", encoding=alt_encoding) as f:
                    content = f.read()
                return content
            except UnicodeDecodeError:
                continue

        # Если все попытки не удались
        raise UnicodeDecodeError(f"Не удалось прочитать файл {file_path} с доступными кодировками")


def write_file(
    file_path: Union[str, Path], content: str, encoding: str = "utf-8", create_dirs: bool = True
) -> bool:
    """
    Записывает содержимое в файл.

    Args:
        file_path: Путь к файлу
        content: Содержимое для записи
        encoding: Кодировка файла (по умолчанию utf-8)
        create_dirs: Создавать директории, если они не существуют

    Returns:
        bool: True если операция успешна, иначе False

    Raises:
        PermissionError: Если нет прав на запись файла
    """
    file_path = Path(file_path)

    # Создаем директории, если нужно
    if create_dirs:
        os.makedirs(file_path.parent, exist_ok=True)

    # Записываем файл
    try:
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Ошибка при записи файла {file_path}: {e}")
        return False


def save_json(
    data: Union[Dict[str, Any], List[Any]],
    file_path: Union[str, Path],
    indent: int = 4,
    encoding: str = "utf-8",
) -> bool:
    """
    Сохраняет данные в формате JSON.

    Args:
        data: Данные для сохранения (словарь или список)
        file_path: Путь к файлу
        indent: Отступ для форматирования JSON
        encoding: Кодировка файла

    Returns:
        bool: True если операция успешна, иначе False
    """
    try:
        json_content = json.dumps(data, indent=indent, ensure_ascii=False)
        return write_file(file_path, json_content, encoding)
    except Exception as e:
        logger.error(f"Ошибка при сохранении JSON в файл {file_path}: {e}")
        return False


def load_json(file_path: Union[str, Path], encoding: str = "utf-8") -> Optional[Dict[str, Any]]:
    """
    Загружает данные из JSON-файла.

    Args:
        file_path: Путь к файлу
        encoding: Кодировка файла

    Returns:
        Optional[Dict[str, Any]]: Загруженные данные или None в случае ошибки
    """
    try:
        content = read_file(file_path, encoding)
        return json.loads(content)
    except Exception as e:
        logger.error(f"Ошибка при загрузке JSON из файла {file_path}: {e}")
        return None


def ensure_directory(dir_path: Union[str, Path]) -> bool:
    """
    Убеждается, что указанная директория существует.

    Args:
        dir_path: Путь к директории

    Returns:
        bool: True если директория создана или уже существует, иначе False
    """
    try:
        os.makedirs(Path(dir_path), exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании директории {dir_path}: {e}")
        return False
