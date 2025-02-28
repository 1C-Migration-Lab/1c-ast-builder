"""
Модуль управления грамматикой.

Этот модуль содержит классы для управления версиями грамматики,
обновления правил и создания парсера. Он поддерживает:
- Версионирование грамматики
- Сохранение и загрузку версий
- Горячее обновление парсера
- Расширение грамматики новыми правилами
"""

import datetime
import json
import logging
import os
import re
import shutil
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from lark import Lark, Tree, exceptions

from ast_create.config import config

# Настройка логирования
logger = logging.getLogger(__name__)


class GrammarVersion:
    """
    Класс, представляющий версию грамматики.

    Атрибуты:
        grammar (str): Строка с грамматикой в формате Lark.
        description (str): Описание версии.
        created_by (str): Идентификатор создателя версии (ручное создание или имя агента).
        version_id (str): Уникальный идентификатор версии.
        timestamp (str): Временная метка создания версии.
    """

    def __init__(
        self,
        grammar: str,
        description: str,
        created_by: str = "manual",
        version_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ):
        """
        Инициализирует новую версию грамматики.

        Args:
            grammar: Строка с грамматикой в формате Lark.
            description: Описание версии.
            created_by: Идентификатор создателя версии (по умолчанию "manual").
            version_id: Уникальный идентификатор версии (если не указан, создается новый).
            timestamp: Временная метка создания (если не указана, используется текущее время).
        """
        self.grammar = grammar
        self.description = description
        self.created_by = created_by
        self.version_id = version_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """
        Преобразует версию грамматики в словарь.

        Returns:
            Dict: Словарь с атрибутами версии.
        """
        return {
            "grammar": self.grammar,
            "description": self.description,
            "created_by": self.created_by,
            "version_id": self.version_id,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "GrammarVersion":
        """
        Создает версию грамматики из словаря.

        Args:
            data: Словарь с атрибутами версии.

        Returns:
            GrammarVersion: Экземпляр версии грамматики.
        """
        return cls(
            grammar=data["grammar"],
            description=data["description"],
            created_by=data["created_by"],
            version_id=data["version_id"],
            timestamp=data["timestamp"],
        )

    def save_to_file(self, file_path: Union[str, Path]) -> bool:
        """
        Сохраняет версию грамматики в файл.

        Args:
            file_path: Путь к файлу для сохранения.

        Returns:
            bool: True, если сохранение успешно, иначе False.
        """
        try:
            # Преобразуем путь в объект Path
            file_path = Path(file_path)

            # Создаем директорию, если она не существует
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Сохраняем данные в файл
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

            logger.info(f"Грамматика версии {self.version_id} сохранена в {file_path}")
            return True

        except Exception as e:
            logger.error(f"Ошибка при сохранении грамматики: {e}")
            return False

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> Optional["GrammarVersion"]:
        """
        Загружает версию грамматики из файла.

        Args:
            file_path: Путь к файлу для загрузки.

        Returns:
            Optional[GrammarVersion]: Экземпляр версии грамматики или None, если произошла ошибка.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            version = cls.from_dict(data)
            logger.info(f"Грамматика версии {version.version_id} загружена из {file_path}")
            return version

        except Exception as e:
            logger.error(f"Ошибка при загрузке грамматики из {file_path}: {e}")
            return None


class GrammarManager:
    """
    Менеджер для управления версиями грамматики.

    Атрибуты:
        current_version (GrammarVersion): Текущая версия грамматики.
        lark_parser (Lark): Парсер Lark, созданный на основе текущей грамматики.
        versions_path (Path): Путь к директории с версиями грамматики.
    """

    # Словарь для кэширования экземпляров парсеров для разных версий
    _parser_cache: Dict[str, Lark] = {}

    def __init__(self, initial_grammar: Optional[str] = None):
        """
        Инициализирует менеджер грамматики.

        Args:
            initial_grammar: Исходная грамматика (если не указана, загружается из файла).
        """
        # Путь к директории с версиями грамматики
        self.versions_path = Path(config.grammar.version_storage)

        # Создаем директорию, если она не существует
        self.versions_path.mkdir(parents=True, exist_ok=True)

        # Инициализация грамматики
        if initial_grammar:
            # Создаем начальную версию
            self.current_version = GrammarVersion(
                grammar=initial_grammar,
                description="Начальная версия грамматики",
                created_by="initialization",
            )

            # Сохраняем начальную версию
            self._save_version(self.current_version)
        else:
            # Загружаем последнюю версию
            self.current_version = self._load_latest_version()

            # Если не найдено ни одной версии, используем базовую грамматику из файла
            if not self.current_version:
                # Загружаем базовую грамматику из файла
                base_grammar_path = Path(config.grammar.base_grammar_file)

                if base_grammar_path.exists():
                    try:
                        # Сначала пробуем UTF-8
                        with open(base_grammar_path, "r", encoding="utf-8") as f:
                            base_grammar = f.read()
                    except UnicodeDecodeError:
                        # Если не получилось, пробуем UTF-16
                        with open(base_grammar_path, "r", encoding="utf-16") as f:
                            base_grammar = f.read()
                else:
                    # Если файл не найден, используем пустую грамматику
                    base_grammar = "start: statement*\n?statement: "
                    logger.warning(f"Файл базовой грамматики не найден: {base_grammar_path}")

                # Создаем начальную версию
                self.current_version = GrammarVersion(
                    grammar=base_grammar,
                    description="Базовая версия грамматики",
                    created_by="initialization",
                )

                # Сохраняем начальную версию
                self._save_version(self.current_version)

        # Создаем парсер на основе текущей грамматики
        self.lark_parser = self._create_parser(self.current_version.grammar)

        logger.info(
            f"Менеджер грамматики инициализирован с версией {self.current_version.version_id}"
        )

    def _create_parser(self, grammar: str) -> Lark:
        """
        Создает парсер Lark на основе грамматики.

        Args:
            grammar: Строка с грамматикой.

        Returns:
            Lark: Экземпляр парсера.
        """
        # Используем LALR парсер и определяем токены в грамматике
        return Lark(grammar, parser="lalr", lexer="contextual")

    def _save_version(self, version: GrammarVersion) -> bool:
        """
        Сохраняет версию грамматики в файл.

        Args:
            version: Версия грамматики для сохранения.

        Returns:
            bool: True, если сохранение успешно, иначе False.
        """
        # Путь к файлу версии
        file_path = self.versions_path / f"{version.version_id}.json"

        # Сохраняем версию
        return version.save_to_file(file_path)

    def _load_version(self, version_id: str) -> Optional[GrammarVersion]:
        """
        Загружает версию грамматики из файла.

        Args:
            version_id: Идентификатор версии.

        Returns:
            Optional[GrammarVersion]: Экземпляр версии грамматики или None, если версия не найдена.
        """
        # Путь к файлу версии
        file_path = self.versions_path / f"{version_id}.json"

        # Проверяем, существует ли файл
        if not file_path.exists():
            logger.error(f"Файл версии не найден: {file_path}")
            return None

        # Загружаем версию
        return GrammarVersion.load_from_file(file_path)

    def _load_latest_version(self) -> Optional[GrammarVersion]:
        """
        Загружает последнюю версию грамматики.

        Returns:
            Optional[GrammarVersion]: Экземпляр последней версии грамматики или None, если версии не найдены.
        """
        # Получаем список файлов версий
        version_files = list(self.versions_path.glob("*.json"))

        # Если нет файлов, возвращаем None
        if not version_files:
            logger.warning("Не найдено ни одной версии грамматики")
            return None

        # Загружаем версии и сортируем по временной метке
        versions = []
        for file_path in version_files:
            version = GrammarVersion.load_from_file(file_path)
            if version:
                versions.append(version)

        # Если нет версий, возвращаем None
        if not versions:
            logger.warning("Не удалось загрузить ни одной версии грамматики")
            return None

        # Сортируем версии по временной метке (новые в конце)
        versions.sort(key=lambda v: v.timestamp)

        # Возвращаем последнюю версию
        return versions[-1]

    def parse(self, code: str) -> Tree:
        """
        Разбирает код с использованием текущей грамматики.

        Args:
            code: Исходный код для разбора.

        Returns:
            Tree: Дерево разбора.

        Raises:
            SyntaxError: Если код не соответствует грамматике.
        """
        try:
            # Разбираем код
            tree = self.lark_parser.parse(code)
            return tree

        except exceptions.UnexpectedToken as e:
            # Обрабатываем ошибку неожиданного токена
            error_message = (
                f"Синтаксическая ошибка: неожиданный токен '{e.token}' в позиции {e.pos_in_stream}"
            )
            logger.error(error_message)

            # Находим строку и столбец ошибки
            line, column = self._get_line_col(code, e.pos_in_stream)
            context = self._get_error_context(code, line)

            # Формируем сообщение об ошибке
            detailed_error = f"{error_message}\nСтрока {line}, столбец {column}:\n{context}"

            # Выбрасываем исключение с подробным сообщением
            raise SyntaxError(detailed_error) from e

        except exceptions.UnexpectedCharacters as e:
            # Обрабатываем ошибку неожиданных символов
            error_message = (
                f"Синтаксическая ошибка: неожиданный символ '{e.char}' в позиции {e.pos_in_stream}"
            )
            logger.error(error_message)

            # Формируем сообщение об ошибке
            detailed_error = f"{error_message}\nСтрока {e.line}, столбец {e.column}:\n{self._get_error_context(code, e.line)}"

            # Выбрасываем исключение с подробным сообщением
            raise SyntaxError(detailed_error) from e

        except Exception as e:
            # Обрабатываем прочие ошибки
            error_message = f"Ошибка при разборе кода: {e}"
            logger.error(error_message)

            # Выбрасываем исключение
            raise SyntaxError(error_message) from e

    def _get_line_col(self, text: str, pos: int) -> Tuple[int, int]:
        """
        Преобразует позицию в тексте в номер строки и столбца.

        Args:
            text: Текст для анализа.
            pos: Позиция в тексте.

        Returns:
            Tuple[int, int]: Номер строки и столбца.
        """
        # Находим начала строк
        line_starts = [0]
        for i, c in enumerate(text):
            if c == "\n":
                line_starts.append(i + 1)

        # Находим номер строки
        line = 1
        for i, start in enumerate(line_starts[1:], 1):
            if pos < start:
                line = i
                break
            else:
                line = i + 1

        # Находим номер столбца
        column = pos - line_starts[line - 1] + 1

        return line, column

    def _get_error_context(self, text: str, line: int, context_lines: int = 2) -> str:
        """
        Получает контекст ошибки в виде строк кода.

        Args:
            text: Исходный код.
            line: Номер строки с ошибкой.
            context_lines: Количество строк контекста до и после ошибки.

        Returns:
            str: Контекст ошибки.
        """
        # Разбиваем текст на строки
        lines = text.split("\n")

        # Определяем диапазон строк для контекста
        start_line = max(0, line - context_lines - 1)
        end_line = min(len(lines), line + context_lines)

        # Формируем контекст
        context = []
        for i in range(start_line, end_line):
            line_num = i + 1
            prefix = "-> " if line_num == line else "   "
            context.append(f"{prefix}{line_num}: {lines[i]}")

        return "\n".join(context)

    def add_version(
        self, grammar: str, description: str, created_by: str = "manual"
    ) -> GrammarVersion:
        """
        Добавляет новую версию грамматики.

        Args:
            grammar: Строка с грамматикой.
            description: Описание версии.
            created_by: Идентификатор создателя версии.

        Returns:
            GrammarVersion: Новая версия грамматики.
        """
        # Создаем новую версию
        new_version = GrammarVersion(
            grammar=grammar, description=description, created_by=created_by
        )

        # Сохраняем новую версию
        self._save_version(new_version)

        # Обновляем текущую версию
        self.current_version = new_version

        # Создаем новый парсер
        try:
            self.lark_parser = self._create_parser(new_version.grammar)
            logger.info(f"Создана новая версия грамматики: {new_version.version_id}")
        except Exception as e:
            logger.error(f"Ошибка при создании парсера для новой версии: {e}")
            raise

        return new_version

    def rollback_to_version(self, version_id: str) -> bool:
        """
        Откатывает грамматику к указанной версии.

        Args:
            version_id: Идентификатор версии.

        Returns:
            bool: True, если откат успешен, иначе False.
        """
        # Загружаем указанную версию
        version = self._load_version(version_id)

        # Если версия не найдена, возвращаем False
        if not version:
            logger.error(f"Не удалось загрузить версию {version_id}")
            return False

        # Обновляем текущую версию
        self.current_version = version

        # Создаем новый парсер
        try:
            self.lark_parser = self._create_parser(version.grammar)
            logger.info(f"Выполнен откат к версии {version_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при создании парсера при откате к версии {version_id}: {e}")
            return False

    def get_all_versions(self) -> List[GrammarVersion]:
        """
        Получает список всех версий грамматики.

        Returns:
            List[GrammarVersion]: Список версий грамматики.
        """
        # Получаем список файлов версий
        version_files = list(self.versions_path.glob("*.json"))

        # Загружаем версии
        versions = []
        for file_path in version_files:
            version = GrammarVersion.load_from_file(file_path)
            if version:
                versions.append(version)

        # Сортируем версии по временной метке
        versions.sort(key=lambda v: v.timestamp)

        return versions

    def extend_grammar(self, new_rules: str, description: str, created_by: str = "manual") -> bool:
        """
        Расширяет грамматику новыми правилами.

        Args:
            new_rules: Строка с новыми правилами. Может содержать обновления существующих правил
                       в формате "// UPDATE_RULE: rule_name |= new_option".
            description: Описание изменений.
            created_by: Идентификатор создателя версии.

        Returns:
            bool: True, если расширение успешно, иначе False.
        """
        # Получаем текущую грамматику
        current_grammar = self.current_version.grammar

        # Проверяем наличие команд обновления существующих правил
        updated_grammar = current_grammar

        # Ищем команды обновления правил (формат: // UPDATE_RULE: rule_name |= new_option)
        update_matches = re.finditer(
            r"//\s*UPDATE_RULE:\s*(\w+)\s*\|=\s*(.+)$", new_rules, re.MULTILINE
        )

        for match in update_matches:
            rule_name = match.group(1)
            new_option = match.group(2).strip()

            # Ищем определение правила в текущей грамматике
            rule_pattern = rf"(?m)^(?:\?)?{rule_name}\s*:(.*?)(?:$|\n\n|\n(?:\w+):)"
            rule_match = re.search(rule_pattern, updated_grammar, re.DOTALL)

            if rule_match:
                # Находим определение правила
                rule_def = rule_match.group(0)
                rule_content = rule_match.group(1).strip()

                # Создаем обновленное определение правила
                updated_rule = f"{rule_name}: {rule_content} | {new_option}"

                # Заменяем старое определение новым
                updated_grammar = updated_grammar.replace(rule_def, updated_rule)
                logger.info(f"Обновлено правило: {rule_name}")

        # Удаляем команды обновления из новых правил
        cleaned_rules = re.sub(r"//\s*UPDATE_RULE:.*$", "", new_rules, flags=re.MULTILINE)

        # Объединяем грамматики
        extended_grammar = f"{updated_grammar}\n\n// Расширение: {description}\n{cleaned_rules}"

        # Проверяем новую грамматику
        try:
            test_parser = self._create_parser(extended_grammar)
            logger.info("Новая грамматика прошла проверку")
        except Exception as e:
            logger.error(f"Ошибка при проверке новой грамматики: {e}")
            return False

        # Добавляем новую версию
        try:
            self.add_version(
                grammar=extended_grammar, description=description, created_by=created_by
            )
            return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении новой версии: {e}")
            return False

    def backup_all_versions(self, backup_dir: Union[str, Path]) -> bool:
        """
        Создает резервную копию всех версий грамматики.

        Args:
            backup_dir: Путь к директории для резервной копии.

        Returns:
            bool: True, если резервное копирование успешно, иначе False.
        """
        # Преобразуем путь в объект Path
        backup_dir = Path(backup_dir)

        # Создаем директорию, если она не существует
        backup_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Получаем список файлов версий
            version_files = list(self.versions_path.glob("*.json"))

            # Копируем файлы
            for file_path in version_files:
                shutil.copy2(file_path, backup_dir)

            # Создаем файл с информацией о резервной копии
            info_file = backup_dir / "backup_info.json"
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "backup_timestamp": datetime.datetime.now().isoformat(),
                        "versions_count": len(version_files),
                        "current_version_id": self.current_version.version_id,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

            logger.info(
                f"Создана резервная копия {len(version_files)} версий грамматики в {backup_dir}"
            )
            return True

        except Exception as e:
            logger.error(f"Ошибка при создании резервной копии: {e}")
            return False


# Единственный экземпляр менеджера грамматики
_grammar_manager_instance = None


def get_grammar_manager() -> GrammarManager:
    """
    Возвращает единственный экземпляр менеджера грамматики.

    Returns:
        GrammarManager: Экземпляр менеджера грамматики.
    """
    global _grammar_manager_instance

    if _grammar_manager_instance is None:
        _grammar_manager_instance = GrammarManager()

    return _grammar_manager_instance
