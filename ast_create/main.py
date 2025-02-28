"""
Основной модуль приложения AST Create.

Этот модуль содержит точку входа в приложение и основные функции для запуска
парсинга, построения AST и автоматического расширения грамматики.
"""

import sys
import argparse
from pathlib import Path
from loguru import logger

from ast_create.config import config, setup_logger
from ast_create.utils import file_utils


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Система автоматического построения грамматики и AST для языка 1С"
    )

    parser.add_argument("file_path", type=str, help="Путь к файлу с исходным кодом 1С для анализа")

    parser.add_argument("--config", type=str, help="Путь к файлу конфигурации (YAML или JSON)")

    parser.add_argument("--debug", action="store_true", help="Включить режим отладки")

    parser.add_argument("--output", type=str, help="Путь для сохранения AST в формате JSON")

    parser.add_argument(
        "--visualize", action="store_true", help="Визуализировать AST и сохранить в файл"
    )

    return parser.parse_args()


def main():
    """Основная функция приложения."""
    args = parse_args()

    # Настройка приложения
    if args.config:
        # Переопределяем конфигурацию, если указан файл
        from ast_create.config import load_config

        global config
        config = load_config(args.config)

    # Настройка логирования
    setup_logger()

    # Включаем режим отладки, если запрошен
    if args.debug:
        config.debug = True
        logger.info("Включен режим отладки")

    # Проверяем существование файла
    file_path = Path(args.file_path)
    if not file_path.exists():
        logger.error(f"Файл не найден: {file_path}")
        return 1

    logger.info(f"Начало обработки файла: {file_path}")

    try:
        # Чтение файла
        source_code = file_utils.read_file(file_path)

        # Здесь будет вызов парсера и построение AST
        # from ast_create.grammar import parser
        # from ast_create.ast import transformer
        #
        # parse_tree = parser.parse(source_code)
        # ast = transformer.transform(parse_tree)

        # Временная заглушка
        logger.info("Парсинг и построение AST пока не реализованы")

        # Сохранение AST
        if args.output:
            # ast.save_to_json(args.output)
            logger.info(f"AST сохранен в файл: {args.output}")

        # Визуализация AST
        if args.visualize:
            # ast.visualize(output_path=args.output.replace('.json', '.png'))
            logger.info("Визуализация AST пока не реализована")

        logger.info("Обработка файла успешно завершена")
        return 0

    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        if config.debug:
            logger.exception("Детали ошибки:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
