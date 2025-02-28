"""
Модуль, содержащий определения интерфейсов узлов AST для языка 1С.

Эти интерфейсы определяют структуру узлов, которые позволяют:
1. Восстанавливать логику (в том числе бизнес-логику)
2. Строить UML-диаграммы
3. Анализировать функциональность
4. Преобразовывать код в другие языки
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class NodeType(Enum):
    """Перечисление типов узлов AST."""

    # Базовые типы
    MODULE = auto()  # Модуль
    VARIABLE_DECLARATION = auto()  # Объявление переменной
    PROCEDURE_DECLARATION = auto()  # Объявление процедуры
    FUNCTION_DECLARATION = auto()  # Объявление функции
    PARAMETER = auto()  # Параметр процедуры/функции

    # Операторы
    ASSIGNMENT = auto()  # Присваивание
    IF_STATEMENT = auto()  # Условный оператор
    ELSE_IF_STATEMENT = auto()  # Оператор "ИначеЕсли"
    ELSE_STATEMENT = auto()  # Оператор "Иначе"
    FOR_STATEMENT = auto()  # Цикл "Для"
    FOR_EACH_STATEMENT = auto()  # Цикл "Для каждого"
    WHILE_STATEMENT = auto()  # Цикл "Пока"
    TRY_STATEMENT = auto()  # Блок "Попытка"
    EXCEPT_STATEMENT = auto()  # Блок "Исключение"
    RETURN_STATEMENT = auto()  # Оператор "Возврат"
    BREAK_STATEMENT = auto()  # Оператор "Прервать"
    CONTINUE_STATEMENT = auto()  # Оператор "Продолжить"
    GOTO_STATEMENT = auto()  # Оператор "Перейти"
    LABEL_STATEMENT = auto()  # Метка
    RAISE_STATEMENT = auto()  # Оператор "ВызватьИсключение"
    EXECUTE_STATEMENT = auto()  # Оператор "Выполнить"

    # Выражения
    BINARY_EXPRESSION = auto()  # Бинарное выражение
    UNARY_EXPRESSION = auto()  # Унарное выражение
    CALL_EXPRESSION = auto()  # Вызов процедуры/функции
    PROPERTY_ACCESS_EXPRESSION = auto()  # Доступ к свойству
    INDEX_ACCESS_EXPRESSION = auto()  # Доступ по индексу
    NEW_EXPRESSION = auto()  # Создание объекта
    TERNARY_EXPRESSION = auto()  # Тернарное выражение

    # Литералы
    LITERAL = auto()  # Литерал
    IDENTIFIER = auto()  # Идентификатор

    # Директивы компиляции
    PREPROCESSOR_IF = auto()  # Директива #Если
    PREPROCESSOR_ELSE_IF = auto()  # Директива #ИначеЕсли
    PREPROCESSOR_ELSE = auto()  # Директива #Иначе
    PREPROCESSOR_END_IF = auto()  # Директива #КонецЕсли
    PREPROCESSOR_REGION = auto()  # Директива #Область
    PREPROCESSOR_END_REGION = auto()  # Директива #КонецОбласти

    # Аннотации
    ANNOTATION = auto()  # Аннотация (&НаКлиенте, &НаСервере и т.д.)

    # Запросы
    QUERY = auto()  # Запрос

    # Прочее
    COMMENT = auto()  # Комментарий
    UNKNOWN = auto()  # Неизвестный тип узла


class ModuleType(Enum):
    """Перечисление типов модулей 1С."""

    COMMON_MODULE = auto()  # Общий модуль
    MANAGER_MODULE = auto()  # Модуль менеджера
    OBJECT_MODULE = auto()  # Модуль объекта
    FORM_MODULE = auto()  # Модуль формы
    COMMAND_MODULE = auto()  # Модуль команды
    EXTERNAL_CONNECTION_MODULE = auto()  # Модуль внешнего соединения
    SESSION_MODULE = auto()  # Модуль сеанса
    UNKNOWN = auto()  # Неизвестный тип модуля


class ExecutionContext(Enum):
    """Перечисление контекстов выполнения кода 1С."""

    CLIENT = auto()  # Клиент
    SERVER = auto()  # Сервер
    SERVER_NO_CONTEXT = auto()  # Сервер без контекста
    THICK_CLIENT_ORDINARY_APPLICATION = auto()  # Толстый клиент обычное приложение
    THICK_CLIENT_MANAGED_APPLICATION = auto()  # Толстый клиент управляемое приложение
    EXTERNAL_CONNECTION = auto()  # Внешнее соединение
    WEB_CLIENT = auto()  # Веб-клиент
    MOBILE_APP_CLIENT = auto()  # Мобильный клиент
    MOBILE_APP_SERVER = auto()  # Мобильный сервер
    UNKNOWN = auto()  # Неизвестный контекст выполнения


@dataclass
class SourceLocation:
    """Класс, представляющий информацию о расположении узла в исходном коде."""

    file_path: str  # Путь к файлу
    start_line: int  # Начальная строка
    start_column: int  # Начальный столбец
    end_line: int  # Конечная строка
    end_column: int  # Конечный столбец
    source_text: Optional[str] = None  # Исходный текст


class INode(ABC):
    """Базовый интерфейс для всех узлов AST."""

    @property
    @abstractmethod
    def node_type(self) -> NodeType:
        """Возвращает тип узла."""

    @property
    @abstractmethod
    def location(self) -> Optional[SourceLocation]:
        """Возвращает информацию о расположении узла в исходном коде."""

    @property
    @abstractmethod
    def children(self) -> List["INode"]:
        """Возвращает список дочерних узлов."""

    @property
    @abstractmethod
    def annotations(self) -> List["IAnnotation"]:
        """Возвращает список аннотаций узла."""

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Возвращает метаданные узла."""


class IAnnotation(INode):
    """Интерфейс для узлов аннотаций."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя аннотации."""

    @property
    @abstractmethod
    def parameters(self) -> List[Any]:
        """Возвращает параметры аннотации."""


class IModule(INode):
    """Интерфейс для узлов модулей."""

    @property
    @abstractmethod
    def module_type(self) -> ModuleType:
        """Возвращает тип модуля."""

    @property
    @abstractmethod
    def variables(self) -> List["IVariableDeclaration"]:
        """Возвращает список объявлений переменных в модуле."""

    @property
    @abstractmethod
    def procedures(self) -> List["IProcedureDeclaration"]:
        """Возвращает список объявлений процедур в модуле."""

    @property
    @abstractmethod
    def functions(self) -> List["IFunctionDeclaration"]:
        """Возвращает список объявлений функций в модуле."""

    @property
    @abstractmethod
    def regions(self) -> List["IPreprocessorRegion"]:
        """Возвращает список областей в модуле."""

    @property
    @abstractmethod
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения модуля."""


class IVariableDeclaration(INode):
    """Интерфейс для узлов объявлений переменных."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя переменной."""

    @property
    @abstractmethod
    def is_exported(self) -> bool:
        """Возвращает признак экспортируемости переменной."""

    @property
    @abstractmethod
    def initial_value(self) -> Optional["IExpression"]:
        """Возвращает начальное значение переменной."""

    @property
    @abstractmethod
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип переменной."""


class IParameter(INode):
    """Интерфейс для узлов параметров."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя параметра."""

    @property
    @abstractmethod
    def by_value(self) -> bool:
        """Возвращает признак передачи параметра по значению."""

    @property
    @abstractmethod
    def default_value(self) -> Optional["IExpression"]:
        """Возвращает значение параметра по умолчанию."""

    @property
    @abstractmethod
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип параметра."""


class IProcedureDeclaration(INode):
    """Интерфейс для узлов объявлений процедур."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя процедуры."""

    @property
    @abstractmethod
    def is_exported(self) -> bool:
        """Возвращает признак экспортируемости процедуры."""

    @property
    @abstractmethod
    def parameters(self) -> List[IParameter]:
        """Возвращает список параметров процедуры."""

    @property
    @abstractmethod
    def body(self) -> List[INode]:
        """Возвращает тело процедуры."""

    @property
    @abstractmethod
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения процедуры."""


class IFunctionDeclaration(INode):
    """Интерфейс для узлов объявлений функций."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя функции."""

    @property
    @abstractmethod
    def is_exported(self) -> bool:
        """Возвращает признак экспортируемости функции."""

    @property
    @abstractmethod
    def parameters(self) -> List[IParameter]:
        """Возвращает список параметров функции."""

    @property
    @abstractmethod
    def body(self) -> List[INode]:
        """Возвращает тело функции."""

    @property
    @abstractmethod
    def return_type(self) -> Optional[str]:
        """Возвращает тип возвращаемого значения функции."""

    @property
    @abstractmethod
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения функции."""


class IStatement(INode):
    """Базовый интерфейс для узлов операторов."""


class IExpression(INode):
    """Базовый интерфейс для узлов выражений."""

    @property
    @abstractmethod
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип выражения."""


class IAssignment(IStatement):
    """Интерфейс для узлов операторов присваивания."""

    @property
    @abstractmethod
    def left(self) -> IExpression:
        """Возвращает левую часть оператора присваивания."""

    @property
    @abstractmethod
    def right(self) -> IExpression:
        """Возвращает правую часть оператора присваивания."""


class IIfStatement(IStatement):
    """Интерфейс для узлов условных операторов."""

    @property
    @abstractmethod
    def condition(self) -> IExpression:
        """Возвращает условие оператора."""

    @property
    @abstractmethod
    def then_branch(self) -> List[IStatement]:
        """Возвращает ветку 'Тогда'."""

    @property
    @abstractmethod
    def else_if_branches(self) -> List[Tuple[IExpression, List[IStatement]]]:
        """Возвращает список веток 'ИначеЕсли'."""

    @property
    @abstractmethod
    def else_branch(self) -> Optional[List[IStatement]]:
        """Возвращает ветку 'Иначе'."""


class IForStatement(IStatement):
    """Интерфейс для узлов операторов цикла 'Для'."""

    @property
    @abstractmethod
    def variable(self) -> IExpression:
        """Возвращает переменную цикла."""

    @property
    @abstractmethod
    def start_value(self) -> IExpression:
        """Возвращает начальное значение."""

    @property
    @abstractmethod
    def end_value(self) -> IExpression:
        """Возвращает конечное значение."""

    @property
    @abstractmethod
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""


class IForEachStatement(IStatement):
    """Интерфейс для узлов операторов цикла 'Для каждого'."""

    @property
    @abstractmethod
    def variable(self) -> IExpression:
        """Возвращает переменную цикла."""

    @property
    @abstractmethod
    def collection(self) -> IExpression:
        """Возвращает коллекцию, по которой выполняется перебор."""

    @property
    @abstractmethod
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""


class IWhileStatement(IStatement):
    """Интерфейс для узлов операторов цикла 'Пока'."""

    @property
    @abstractmethod
    def condition(self) -> IExpression:
        """Возвращает условие цикла."""

    @property
    @abstractmethod
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""


class ITryStatement(IStatement):
    """Интерфейс для узлов операторов 'Попытка'."""

    @property
    @abstractmethod
    def try_body(self) -> List[IStatement]:
        """Возвращает тело блока 'Попытка'."""

    @property
    @abstractmethod
    def except_body(self) -> List[IStatement]:
        """Возвращает тело блока 'Исключение'."""


class IReturnStatement(IStatement):
    """Интерфейс для узлов операторов 'Возврат'."""

    @property
    @abstractmethod
    def expression(self) -> Optional[IExpression]:
        """Возвращает выражение, значение которого возвращается."""


class IRaiseStatement(IStatement):
    """Интерфейс для узлов операторов 'ВызватьИсключение'."""

    @property
    @abstractmethod
    def expression(self) -> Optional[IExpression]:
        """Возвращает выражение, представляющее исключение."""


class IExecuteStatement(IStatement):
    """Интерфейс для узлов операторов 'Выполнить'."""

    @property
    @abstractmethod
    def expression(self) -> IExpression:
        """Возвращает выражение, представляющее выполняемый код."""


class IBinaryExpression(IExpression):
    """Интерфейс для узлов бинарных выражений."""

    @property
    @abstractmethod
    def operator(self) -> str:
        """Возвращает оператор выражения."""

    @property
    @abstractmethod
    def left(self) -> IExpression:
        """Возвращает левый операнд."""

    @property
    @abstractmethod
    def right(self) -> IExpression:
        """Возвращает правый операнд."""


class IUnaryExpression(IExpression):
    """Интерфейс для узлов унарных выражений."""

    @property
    @abstractmethod
    def operator(self) -> str:
        """Возвращает оператор выражения."""

    @property
    @abstractmethod
    def operand(self) -> IExpression:
        """Возвращает операнд."""


class ICallExpression(IExpression):
    """Интерфейс для узлов вызовов процедур и функций."""

    @property
    @abstractmethod
    def callee(self) -> IExpression:
        """Возвращает вызываемое выражение."""

    @property
    @abstractmethod
    def arguments(self) -> List[IExpression]:
        """Возвращает список аргументов."""


class IPropertyAccessExpression(IExpression):
    """Интерфейс для узлов доступа к свойствам."""

    @property
    @abstractmethod
    def object(self) -> IExpression:
        """Возвращает объект, свойство которого получается."""

    @property
    @abstractmethod
    def property_name(self) -> str:
        """Возвращает имя свойства."""


class IIndexAccessExpression(IExpression):
    """Интерфейс для узлов доступа по индексу."""

    @property
    @abstractmethod
    def object(self) -> IExpression:
        """Возвращает объект, к которому осуществляется доступ по индексу."""

    @property
    @abstractmethod
    def index(self) -> IExpression:
        """Возвращает индекс."""


class INewExpression(IExpression):
    """Интерфейс для узлов создания новых объектов."""

    @property
    @abstractmethod
    def type_name(self) -> str:
        """Возвращает имя типа создаваемого объекта."""

    @property
    @abstractmethod
    def arguments(self) -> List[IExpression]:
        """Возвращает список аргументов конструктора."""


class ILiteral(IExpression):
    """Интерфейс для узлов литералов."""

    @property
    @abstractmethod
    def value(self) -> Any:
        """Возвращает значение литерала."""

    @property
    @abstractmethod
    def literal_type(self) -> str:
        """Возвращает тип литерала."""


class IIdentifier(IExpression):
    """Интерфейс для узлов идентификаторов."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя идентификатора."""

    @property
    @abstractmethod
    def reference(self) -> Optional[INode]:
        """Возвращает узел, на который ссылается идентификатор."""


class IPreprocessorDirective(INode):
    """Базовый интерфейс для узлов директив препроцессора."""


class IPreprocessorIf(IPreprocessorDirective):
    """Интерфейс для узлов директив #Если."""

    @property
    @abstractmethod
    def condition(self) -> IExpression:
        """Возвращает условие директивы."""

    @property
    @abstractmethod
    def then_branch(self) -> List[INode]:
        """Возвращает ветку 'Тогда'."""

    @property
    @abstractmethod
    def else_if_branches(self) -> List[Tuple[IExpression, List[INode]]]:
        """Возвращает список веток 'ИначеЕсли'."""

    @property
    @abstractmethod
    def else_branch(self) -> Optional[List[INode]]:
        """Возвращает ветку 'Иначе'."""


class IPreprocessorRegion(IPreprocessorDirective):
    """Интерфейс для узлов директив #Область."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя области."""

    @property
    @abstractmethod
    def body(self) -> List[INode]:
        """Возвращает содержимое области."""


class IQuery(IExpression):
    """Интерфейс для узлов запросов."""

    @property
    @abstractmethod
    def text(self) -> str:
        """Возвращает текст запроса."""

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, IExpression]:
        """Возвращает параметры запроса."""

    @property
    @abstractmethod
    def tables(self) -> List[str]:
        """Возвращает список таблиц, используемых в запросе."""

    @property
    @abstractmethod
    def fields(self) -> List[str]:
        """Возвращает список полей, используемых в запросе."""


class IComment(INode):
    """Интерфейс для узлов комментариев."""

    @property
    @abstractmethod
    def text(self) -> str:
        """Возвращает текст комментария."""

    @property
    @abstractmethod
    def is_doc_comment(self) -> bool:
        """Возвращает признак того, что комментарий является документирующим."""


class IReferenceInfo:
    """Интерфейс для информации о ссылках на метаданные."""

    @property
    @abstractmethod
    def reference_kind(self) -> str:
        """Возвращает вид ссылки."""

    @property
    @abstractmethod
    def reference_name(self) -> str:
        """Возвращает имя ссылки."""

    @property
    @abstractmethod
    def metadata_uuid(self) -> Optional[str]:
        """Возвращает UUID метаданных."""
