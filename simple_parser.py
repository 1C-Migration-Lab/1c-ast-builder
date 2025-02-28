from lark import Lark

grammar = r'''
start: statement+

statement: var_decl | assignment | if_stmt

var_decl: "Перем" CNAME ";"
assignment: CNAME "=" expr ";"
if_stmt: "Если" expr "Тогда" statement+ "КонецЕсли" ";"

?expr: sum ((">" | "<" | ">=" | "<=" | "==" | "!=") sum)?
?sum: term (("+" | "-") term)*
?term: factor (("*" | "/") factor)*
?factor: NUMBER           -> number
       | CNAME            -> var
       | "(" expr ")"

%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS
'''

# Создание парсера с использованием Lark
parser = Lark(grammar, start='start', parser='lalr')

# Пример кода 1С для разбора
code = '''
Перем x;
x = 5;
Если x > 3 Тогда
    x = x - 1;
КонецЕсли;
'''

# Парсинг кода
tree = parser.parse(code)
print(tree.pretty()) 