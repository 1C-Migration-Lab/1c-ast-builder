"""
Модуль, содержащий базовые абстрактные классы узлов AST для языка 1С.

Эти классы реализуют интерфейсы из модуля nodes.py и предоставляют
базовую функциональность для конкретных реализаций узлов AST.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ast_create.ast.nodes import (
    ExecutionContext,
    IAnnotation,
    IAssignment,
    IBinaryExpression,
    ICallExpression,
    IComment,
    IExecuteStatement,
    IExpression,
    IForEachStatement,
    IForStatement,
    IFunctionDeclaration,
    IIdentifier,
    IIfStatement,
    IIndexAccessExpression,
    ILiteral,
    IModule,
    INewExpression,
    INode,
    IParameter,
    IPreprocessorDirective,
    IPreprocessorIf,
    IPreprocessorRegion,
    IProcedureDeclaration,
    IPropertyAccessExpression,
    IQuery,
    IRaiseStatement,
    IReferenceInfo,
    IReturnStatement,
    IStatement,
    ITryStatement,
    IUnaryExpression,
    IVariableDeclaration,
    IWhileStatement,
    ModuleType,
    NodeType,
    SourceLocation,
)


class BaseNode(INode, ABC):
    """Базовый абстрактный класс для всех узлов AST."""

    def __init__(
        self,
        node_type: NodeType,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self._node_type = node_type
        self._location = location
        self._children = children or []
        self._annotations = annotations or []
        self._metadata = metadata or {}

    @property
    def node_type(self) -> NodeType:
        """Возвращает тип узла."""
        return self._node_type

    @property
    def location(self) -> Optional[SourceLocation]:
        """Возвращает информацию о расположении узла в исходном коде."""
        return self._location

    @property
    def children(self) -> List[INode]:
        """Возвращает список дочерних узлов."""
        return self._children

    @property
    def annotations(self) -> List[IAnnotation]:
        """Возвращает список аннотаций узла."""
        return self._annotations

    @property
    def metadata(self) -> Dict[str, Any]:
        """Возвращает метаданные узла."""
        return self._metadata


class BaseAnnotation(BaseNode, IAnnotation, ABC):
    """Базовый абстрактный класс для узлов аннотаций."""

    def __init__(
        self,
        name: str,
        parameters: Optional[List[Any]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.ANNOTATION, location, children, annotations, metadata)
        self._name = name
        self._parameters = parameters or []

    @property
    def name(self) -> str:
        """Возвращает имя аннотации."""
        return self._name

    @property
    def parameters(self) -> List[Any]:
        """Возвращает параметры аннотации."""
        return self._parameters


class BaseExpression(BaseNode, IExpression, ABC):
    """Базовый абстрактный класс для узлов выражений."""

    def __init__(
        self,
        node_type: NodeType,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(node_type, location, children, annotations, metadata)
        self._inferred_type = inferred_type

    @property
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип выражения."""
        return self._inferred_type


class BaseStatement(BaseNode, IStatement, ABC):
    """Базовый абстрактный класс для узлов операторов."""

    def __init__(
        self,
        node_type: NodeType,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        # Инициализация базового класса оператора
        # В будущем здесь может быть добавлена дополнительная логика для операторов
        # pylint: disable=useless-parent-delegation
        super().__init__(node_type, location, children, annotations, metadata)


class BaseModule(BaseNode, IModule, ABC):
    """Базовый абстрактный класс для узлов модулей."""

    def __init__(
        self,
        module_type: ModuleType,
        variables: Optional[List[IVariableDeclaration]] = None,
        procedures: Optional[List[IProcedureDeclaration]] = None,
        functions: Optional[List[IFunctionDeclaration]] = None,
        regions: Optional[List[IPreprocessorRegion]] = None,
        execution_context: ExecutionContext = ExecutionContext.UNKNOWN,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.MODULE, location, children, annotations, metadata)
        self._module_type = module_type
        self._variables = variables or []
        self._procedures = procedures or []
        self._functions = functions or []
        self._regions = regions or []
        self._execution_context = execution_context

    @property
    def module_type(self) -> ModuleType:
        """Возвращает тип модуля."""
        return self._module_type

    @property
    def variables(self) -> List[IVariableDeclaration]:
        """Возвращает список объявлений переменных в модуле."""
        return self._variables

    @property
    def procedures(self) -> List[IProcedureDeclaration]:
        """Возвращает список объявлений процедур в модуле."""
        return self._procedures

    @property
    def functions(self) -> List[IFunctionDeclaration]:
        """Возвращает список объявлений функций в модуле."""
        return self._functions

    @property
    def regions(self) -> List[IPreprocessorRegion]:
        """Возвращает список областей в модуле."""
        return self._regions

    @property
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения модуля."""
        return self._execution_context


class BaseVariableDeclaration(BaseNode, IVariableDeclaration, ABC):
    """Базовый абстрактный класс для узлов объявлений переменных."""

    def __init__(
        self,
        name: str,
        is_exported: bool = False,
        initial_value: Optional[IExpression] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.VARIABLE_DECLARATION, location, children, annotations, metadata)
        self._name = name
        self._is_exported = is_exported
        self._initial_value = initial_value
        self._inferred_type = inferred_type

    @property
    def name(self) -> str:
        """Возвращает имя переменной."""
        return self._name

    @property
    def is_exported(self) -> bool:
        """Возвращает флаг экспорта переменной."""
        return self._is_exported

    @property
    def initial_value(self) -> Optional[IExpression]:
        """Возвращает начальное значение переменной."""
        return self._initial_value

    @property
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип переменной."""
        return self._inferred_type


class BaseParameter(BaseNode, IParameter, ABC):
    """Базовый абстрактный класс для узлов параметров процедур и функций."""

    def __init__(
        self,
        name: str,
        by_value: bool = False,
        default_value: Optional[IExpression] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.PARAMETER, location, children, annotations, metadata)
        self._name = name
        self._by_value = by_value
        self._default_value = default_value
        self._inferred_type = inferred_type

    @property
    def name(self) -> str:
        """Возвращает имя параметра."""
        return self._name

    @property
    def by_value(self) -> bool:
        """Возвращает флаг передачи параметра по значению."""
        return self._by_value

    @property
    def default_value(self) -> Optional[IExpression]:
        """Возвращает значение параметра по умолчанию."""
        return self._default_value

    @property
    def inferred_type(self) -> Optional[str]:
        """Возвращает выведенный тип параметра."""
        return self._inferred_type


class BaseProcedureDeclaration(BaseNode, IProcedureDeclaration, ABC):
    """Базовый абстрактный класс для узлов объявлений процедур."""

    def __init__(
        self,
        name: str,
        is_exported: bool = False,
        parameters: Optional[List[IParameter]] = None,
        body: Optional[List[INode]] = None,
        execution_context: ExecutionContext = ExecutionContext.UNKNOWN,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.PROCEDURE_DECLARATION, location, children, annotations, metadata)
        self._name = name
        self._is_exported = is_exported
        self._parameters = parameters or []
        self._body = body or []
        self._execution_context = execution_context

    @property
    def name(self) -> str:
        """Возвращает имя процедуры."""
        return self._name

    @property
    def is_exported(self) -> bool:
        """Возвращает флаг экспорта процедуры."""
        return self._is_exported

    @property
    def parameters(self) -> List[IParameter]:
        """Возвращает список параметров процедуры."""
        return self._parameters

    @property
    def body(self) -> List[INode]:
        """Возвращает тело процедуры."""
        return self._body

    @property
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения процедуры."""
        return self._execution_context


class BaseFunctionDeclaration(BaseNode, IFunctionDeclaration, ABC):
    """Базовый абстрактный класс для узлов объявлений функций."""

    def __init__(
        self,
        name: str,
        is_exported: bool = False,
        parameters: Optional[List[IParameter]] = None,
        body: Optional[List[INode]] = None,
        return_type: Optional[str] = None,
        execution_context: ExecutionContext = ExecutionContext.UNKNOWN,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.FUNCTION_DECLARATION, location, children, annotations, metadata)
        self._name = name
        self._is_exported = is_exported
        self._parameters = parameters or []
        self._body = body or []
        self._return_type = return_type
        self._execution_context = execution_context

    @property
    def name(self) -> str:
        """Возвращает имя функции."""
        return self._name

    @property
    def is_exported(self) -> bool:
        """Возвращает флаг экспорта функции."""
        return self._is_exported

    @property
    def parameters(self) -> List[IParameter]:
        """Возвращает список параметров функции."""
        return self._parameters

    @property
    def body(self) -> List[INode]:
        """Возвращает тело функции."""
        return self._body

    @property
    def return_type(self) -> Optional[str]:
        """Возвращает тип возвращаемого значения функции."""
        return self._return_type

    @property
    def execution_context(self) -> ExecutionContext:
        """Возвращает контекст выполнения функции."""
        return self._execution_context


class BaseAssignment(BaseStatement, IAssignment, ABC):
    """Базовый абстрактный класс для узлов операторов присваивания."""

    def __init__(
        self,
        left: IExpression,
        right: IExpression,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.ASSIGNMENT, location, children, annotations, metadata)
        self._left = left
        self._right = right

    @property
    def left(self) -> IExpression:
        """Возвращает левую часть присваивания."""
        return self._left

    @property
    def right(self) -> IExpression:
        """Возвращает правую часть присваивания."""
        return self._right


class BaseIfStatement(BaseStatement, IIfStatement, ABC):
    """Базовый абстрактный класс для узлов условных операторов."""

    def __init__(
        self,
        condition: IExpression,
        then_branch: Optional[List[IStatement]] = None,
        else_if_branches: Optional[List[Tuple[IExpression, List[IStatement]]]] = None,
        else_branch: Optional[List[IStatement]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.IF_STATEMENT, location, children, annotations, metadata)
        self._condition = condition
        self._then_branch = then_branch or []
        self._else_if_branches = else_if_branches or []
        self._else_branch = else_branch

    @property
    def condition(self) -> IExpression:
        """Возвращает условие оператора."""
        return self._condition

    @property
    def then_branch(self) -> List[IStatement]:
        """Возвращает ветку "Тогда"."""
        return self._then_branch

    @property
    def else_if_branches(self) -> List[Tuple[IExpression, List[IStatement]]]:
        """Возвращает список веток "ИначеЕсли" (условие, список операторов)."""
        return self._else_if_branches

    @property
    def else_branch(self) -> Optional[List[IStatement]]:
        """Возвращает ветку "Иначе"."""
        return self._else_branch


class BaseForStatement(BaseStatement, IForStatement, ABC):
    """Базовый абстрактный класс для узлов операторов цикла "Для"."""

    def __init__(
        self,
        variable: IExpression,
        start_value: IExpression,
        end_value: IExpression,
        body: Optional[List[IStatement]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.FOR_STATEMENT, location, children, annotations, metadata)
        self._variable = variable
        self._start_value = start_value
        self._end_value = end_value
        self._body = body or []

    @property
    def variable(self) -> IExpression:
        """Возвращает переменную цикла."""
        return self._variable

    @property
    def start_value(self) -> IExpression:
        """Возвращает начальное значение."""
        return self._start_value

    @property
    def end_value(self) -> IExpression:
        """Возвращает конечное значение."""
        return self._end_value

    @property
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""
        return self._body


class BaseForEachStatement(BaseStatement, IForEachStatement, ABC):
    """Базовый абстрактный класс для узлов операторов цикла "Для каждого"."""

    def __init__(
        self,
        variable: IExpression,
        collection: IExpression,
        body: Optional[List[IStatement]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.FOR_EACH_STATEMENT, location, children, annotations, metadata)
        self._variable = variable
        self._collection = collection
        self._body = body or []

    @property
    def variable(self) -> IExpression:
        """Возвращает переменную цикла."""
        return self._variable

    @property
    def collection(self) -> IExpression:
        """Возвращает коллекцию."""
        return self._collection

    @property
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""
        return self._body


class BaseWhileStatement(BaseStatement, IWhileStatement, ABC):
    """Базовый абстрактный класс для узлов операторов цикла "Пока"."""

    def __init__(
        self,
        condition: IExpression,
        body: Optional[List[IStatement]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.WHILE_STATEMENT, location, children, annotations, metadata)
        self._condition = condition
        self._body = body or []

    @property
    def condition(self) -> IExpression:
        """Возвращает условие цикла."""
        return self._condition

    @property
    def body(self) -> List[IStatement]:
        """Возвращает тело цикла."""
        return self._body


class BaseTryStatement(BaseStatement, ITryStatement, ABC):
    """Базовый абстрактный класс для узлов операторов "Попытка"."""

    def __init__(
        self,
        try_body: Optional[List[IStatement]] = None,
        except_body: Optional[List[IStatement]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.TRY_STATEMENT, location, children, annotations, metadata)
        self._try_body = try_body or []
        self._except_body = except_body or []

    @property
    def try_body(self) -> List[IStatement]:
        """Возвращает тело блока "Попытка"."""
        return self._try_body

    @property
    def except_body(self) -> List[IStatement]:
        """Возвращает тело блока "Исключение"."""
        return self._except_body


class BaseReturnStatement(BaseStatement, IReturnStatement, ABC):
    """Базовый абстрактный класс для узлов операторов "Возврат"."""

    def __init__(
        self,
        expression: Optional[IExpression] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.RETURN_STATEMENT, location, children, annotations, metadata)
        self._expression = expression

    @property
    def expression(self) -> Optional[IExpression]:
        """Возвращает выражение, возвращаемое оператором."""
        return self._expression


class BaseRaiseStatement(BaseStatement, IRaiseStatement, ABC):
    """Базовый абстрактный класс для узлов операторов "ВызватьИсключение"."""

    def __init__(
        self,
        expression: Optional[IExpression] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.RAISE_STATEMENT, location, children, annotations, metadata)
        self._expression = expression

    @property
    def expression(self) -> Optional[IExpression]:
        """Возвращает выражение исключения."""
        return self._expression


class BaseExecuteStatement(BaseStatement, IExecuteStatement, ABC):
    """Базовый абстрактный класс для узлов операторов "Выполнить"."""

    def __init__(
        self,
        expression: IExpression,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.EXECUTE_STATEMENT, location, children, annotations, metadata)
        self._expression = expression

    @property
    def expression(self) -> IExpression:
        """Возвращает выражение, которое нужно выполнить."""
        return self._expression


class BaseBinaryExpression(BaseExpression, IBinaryExpression, ABC):
    """Базовый абстрактный класс для узлов бинарных выражений."""

    def __init__(
        self,
        operator: str,
        left: IExpression,
        right: IExpression,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.BINARY_EXPRESSION, inferred_type, location, children, annotations, metadata
        )
        self._operator = operator
        self._left = left
        self._right = right

    @property
    def operator(self) -> str:
        """Возвращает оператор выражения."""
        return self._operator

    @property
    def left(self) -> IExpression:
        """Возвращает левый операнд."""
        return self._left

    @property
    def right(self) -> IExpression:
        """Возвращает правый операнд."""
        return self._right


class BaseUnaryExpression(BaseExpression, IUnaryExpression, ABC):
    """Базовый абстрактный класс для узлов унарных выражений."""

    def __init__(
        self,
        operator: str,
        operand: IExpression,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.UNARY_EXPRESSION, inferred_type, location, children, annotations, metadata
        )
        self._operator = operator
        self._operand = operand

    @property
    def operator(self) -> str:
        """Возвращает оператор выражения."""
        return self._operator

    @property
    def operand(self) -> IExpression:
        """Возвращает операнд."""
        return self._operand


class BaseCallExpression(BaseExpression, ICallExpression, ABC):
    """Базовый абстрактный класс для узлов вызовов процедур и функций."""

    def __init__(
        self,
        callee: IExpression,
        arguments: Optional[List[IExpression]] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.CALL_EXPRESSION, inferred_type, location, children, annotations, metadata
        )
        self._callee = callee
        self._arguments = arguments or []

    @property
    def callee(self) -> IExpression:
        """Возвращает вызываемое выражение."""
        return self._callee

    @property
    def arguments(self) -> List[IExpression]:
        """Возвращает список аргументов."""
        return self._arguments


class BasePropertyAccessExpression(BaseExpression, IPropertyAccessExpression, ABC):
    """Базовый абстрактный класс для узлов доступа к свойствам."""

    def __init__(
        self,
        object_expr: IExpression,
        property_name: str,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.PROPERTY_ACCESS_EXPRESSION,
            inferred_type,
            location,
            children,
            annotations,
            metadata,
        )
        self._object = object_expr
        self._property_name = property_name

    @property
    def object(self) -> IExpression:
        """Возвращает объект, к свойству которого осуществляется доступ."""
        return self._object

    @property
    def property_name(self) -> str:
        """Возвращает имя свойства."""
        return self._property_name


class BaseIndexAccessExpression(BaseExpression, IIndexAccessExpression, ABC):
    """Базовый абстрактный класс для узлов доступа по индексу."""

    def __init__(
        self,
        object_expr: IExpression,
        index: IExpression,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.INDEX_ACCESS_EXPRESSION,
            inferred_type,
            location,
            children,
            annotations,
            metadata,
        )
        self._object = object_expr
        self._index = index

    @property
    def object(self) -> IExpression:
        """Возвращает объект, к элементу которого осуществляется доступ."""
        return self._object

    @property
    def index(self) -> IExpression:
        """Возвращает индекс."""
        return self._index


class BaseNewExpression(BaseExpression, INewExpression, ABC):
    """Базовый абстрактный класс для узлов создания объектов."""

    def __init__(
        self,
        type_name: str,
        arguments: Optional[List[IExpression]] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.NEW_EXPRESSION, inferred_type, location, children, annotations, metadata
        )
        self._type_name = type_name
        self._arguments = arguments or []

    @property
    def type_name(self) -> str:
        """Возвращает имя типа создаваемого объекта."""
        return self._type_name

    @property
    def arguments(self) -> List[IExpression]:
        """Возвращает список аргументов конструктора."""
        return self._arguments


class BaseLiteral(BaseExpression, ILiteral, ABC):
    """Базовый абстрактный класс для узлов литералов."""

    def __init__(
        self,
        value: Any,
        literal_type: str,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.LITERAL, inferred_type, location, children, annotations, metadata)
        self._value = value
        self._literal_type = literal_type

    @property
    def value(self) -> Any:
        """Возвращает значение литерала."""
        return self._value

    @property
    def literal_type(self) -> str:
        """Возвращает тип литерала (строка, число, дата, булево, NULL)."""
        return self._literal_type


class BaseIdentifier(BaseExpression, IIdentifier, ABC):
    """Базовый абстрактный класс для узлов идентификаторов."""

    def __init__(
        self,
        name: str,
        reference: Optional[INode] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            NodeType.IDENTIFIER, inferred_type, location, children, annotations, metadata
        )
        self._name = name
        self._reference = reference

    @property
    def name(self) -> str:
        """Возвращает имя идентификатора."""
        return self._name

    @property
    def reference(self) -> Optional[INode]:
        """Возвращает узел, на который ссылается идентификатор."""
        return self._reference


class BasePreprocessorDirective(BaseNode, IPreprocessorDirective, ABC):
    """Базовый абстрактный класс для узлов директив препроцессора."""

    def __init__(
        self,
        node_type: NodeType,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        # Инициализация базового класса директивы препроцессора
        # В будущем здесь может быть добавлена дополнительная логика для директив
        # pylint: disable=useless-parent-delegation
        super().__init__(node_type, location, children, annotations, metadata)


class BasePreprocessorIf(BasePreprocessorDirective, IPreprocessorIf, ABC):
    """Базовый абстрактный класс для узлов директив #Если."""

    def __init__(
        self,
        condition: IExpression,
        then_branch: Optional[List[INode]] = None,
        else_if_branches: Optional[List[Tuple[IExpression, List[INode]]]] = None,
        else_branch: Optional[List[INode]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.PREPROCESSOR_IF, location, children, annotations, metadata)
        self._condition = condition
        self._then_branch = then_branch or []
        self._else_if_branches = else_if_branches or []
        self._else_branch = else_branch

    @property
    def condition(self) -> IExpression:
        """Возвращает условие директивы."""
        return self._condition

    @property
    def then_branch(self) -> List[INode]:
        """Возвращает ветку "Тогда"."""
        return self._then_branch

    @property
    def else_if_branches(self) -> List[Tuple[IExpression, List[INode]]]:
        """Возвращает список веток "ИначеЕсли" (условие, список узлов)."""
        return self._else_if_branches

    @property
    def else_branch(self) -> Optional[List[INode]]:
        """Возвращает ветку "Иначе"."""
        return self._else_branch


class BasePreprocessorRegion(BasePreprocessorDirective, IPreprocessorRegion, ABC):
    """Базовый абстрактный класс для узлов директив #Область."""

    def __init__(
        self,
        name: str,
        body: Optional[List[INode]] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.PREPROCESSOR_REGION, location, children, annotations, metadata)
        self._name = name
        self._body = body or []

    @property
    def name(self) -> str:
        """Возвращает имя области."""
        return self._name

    @property
    def body(self) -> List[INode]:
        """Возвращает содержимое области."""
        return self._body


class BaseQuery(BaseExpression, IQuery, ABC):
    """Базовый абстрактный класс для узлов запросов."""

    def __init__(
        self,
        text: str,
        parameters: Optional[Dict[str, IExpression]] = None,
        tables: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        inferred_type: Optional[str] = None,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.QUERY, inferred_type, location, children, annotations, metadata)
        self._text = text
        self._parameters = parameters or {}
        self._tables = tables or []
        self._fields = fields or []

    @property
    def text(self) -> str:
        """Возвращает текст запроса."""
        return self._text

    @property
    def parameters(self) -> Dict[str, IExpression]:
        """Возвращает параметры запроса."""
        return self._parameters

    @property
    def tables(self) -> List[str]:
        """Возвращает список таблиц, используемых в запросе."""
        return self._tables

    @property
    def fields(self) -> List[str]:
        """Возвращает список полей, используемых в запросе."""
        return self._fields


class BaseComment(BaseNode, IComment, ABC):
    """Базовый абстрактный класс для узлов комментариев."""

    def __init__(
        self,
        text: str,
        is_doc_comment: bool = False,
        location: Optional[SourceLocation] = None,
        children: Optional[List[INode]] = None,
        annotations: Optional[List[IAnnotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(NodeType.COMMENT, location, children, annotations, metadata)
        self._text = text
        self._is_doc_comment = is_doc_comment

    @property
    def text(self) -> str:
        """Возвращает текст комментария."""
        return self._text

    @property
    def is_doc_comment(self) -> bool:
        """Возвращает флаг, указывающий, является ли комментарий документирующим."""
        return self._is_doc_comment


class BaseReferenceInfo(IReferenceInfo, ABC):
    """Базовый абстрактный класс для информации о ссылках на объекты конфигурации."""

    def __init__(
        self, reference_kind: str, reference_name: str, metadata_uuid: Optional[str] = None
    ):
        self._reference_kind = reference_kind
        self._reference_name = reference_name
        self._metadata_uuid = metadata_uuid

    @property
    def reference_kind(self) -> str:
        """Возвращает тип ссылки (модуль, объект конфигурации, переменная и т.д.)."""
        return self._reference_kind

    @property
    def reference_name(self) -> str:
        """Возвращает имя объекта, на который ссылается."""
        return self._reference_name

    @property
    def metadata_uuid(self) -> Optional[str]:
        """Возвращает UUID метаданных объекта, на который ссылается."""
        return self._metadata_uuid
