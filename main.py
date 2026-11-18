import re
import sys


class PrePro:
    @staticmethod
    def filter(code):
        # Remove tudo entre "//" e o fim da linha, preservando o "\n".
        # Strings entre aspas sao mantidas intactas (ex: "http://x" nao e comentario)
        return re.sub(r'("[^"\n]*")|//.*', lambda match: match.group(1) or "", code)


class Variable:
    # is_function = True quando a "variavel" guarda uma funcao (value = no FuncDec, type = tipo de retorno)
    def __init__(self, value, type, is_function=False):
        self.value = value
        self.type = type
        self.is_function = is_function


class SymbolTable:
    # Valor inicial de uma variavel declarada sem atribuicao (zero value do Go)
    DEFAULT_VALUES = {"int": 0, "string": "", "bool": False}

    # parent = tabela do escopo de fora (lista ligada reversa: o escopo global tem parent None)
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent

    def create_variable(self, name, type, is_function=False):
        # So olha o escopo atual: declarar um nome que ja existe num escopo de fora e permitido (sombreamento)
        if name in self.table:
            raise Exception("[Semantic] Identifier '" + name + "' already declared")
        self.table[name] = Variable(SymbolTable.DEFAULT_VALUES.get(type), type, is_function)

    def get_value(self, name):
        if name in self.table:
            return self.table[name]
        if self.parent is not None:
            return self.parent.get_value(name)
        raise Exception("[Semantic] Undefined identifier '" + name + "'")

    def set_value(self, name, variable):
        if name not in self.table:
            if self.parent is not None:
                return self.parent.set_value(name, variable)
            raise Exception("[Semantic] Variable '" + name + "' not declared")

        if self.table[name].is_function:
            raise Exception("[Semantic] Cannot assign to function '" + name + "'")

        declared_type = self.table[name].type
        if variable.type != declared_type:
            raise Exception(
                "[Semantic] Cannot assign " + variable.type + " to variable '" + name + "' of type " + declared_type
            )

        self.table[name] = Variable(variable.value, declared_type)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    RESERVED_WORDS = {
        "Println": "PRINT",
        "Scanln": "READ",
        "if": "IF",
        "else": "ELSE",
        "for": "WHILE",
        "var": "VAR",
        "func": "FUNC",
        "return": "RETURN",
    }

    TYPES = ("int", "string", "bool")

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        # Ignora espacos, tabs e "\r" (o "\n" vira o token END)
        while self.position < len(self.source) and self.source[self.position] in " \t\r":
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return

        current = self.source[self.position]

        if current == "+":
            self.next = Token("PLUS", "+")
            self.position += 1
        elif current == "-":
            self.next = Token("MINUS", "-")
            self.position += 1
        elif current == "*":
            self.next = Token("MULT", "*")
            self.position += 1
        elif current == "/":
            self.next = Token("DIV", "/")
            self.position += 1
        elif current == ",":
            self.next = Token("COMMA", ",")
            self.position += 1
        elif current == "(":
            self.next = Token("OPEN_PAR", "(")
            self.position += 1
        elif current == ")":
            self.next = Token("CLOSE_PAR", ")")
            self.position += 1
        elif current == "{":
            self.next = Token("OPEN_BRA", "{")
            self.position += 1
        elif current == "}":
            self.next = Token("CLOSE_BRA", "}")
            self.position += 1
        elif current == ">":
            self.next = Token("GT", ">")
            self.position += 1
        elif current == "<":
            self.next = Token("LT", "<")
            self.position += 1
        elif current == "!":
            self.next = Token("NOT", "!")
            self.position += 1
        elif current == "=":
            # "==" e o operador relacional EQ; "=" sozinho e a atribuicao
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                self.next = Token("EQ", "==")
                self.position += 2
            else:
                self.next = Token("ASSIGN", "=")
                self.position += 1
        elif current == "&":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "&":
                self.next = Token("AND", "&&")
                self.position += 2
            else:
                raise Exception("[Lexer] Invalid Symbol '&' (expected '&&')")
        elif current == "|":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "|":
                self.next = Token("OR", "||")
                self.position += 2
            else:
                raise Exception("[Lexer] Invalid Symbol '|' (expected '||')")
        elif current == "\n":
            self.next = Token("END", "\n")
            self.position += 1
        elif current == '"':
            # Tudo entre as aspas vira o valor do token STR (sem quebra de linha)
            self.position += 1
            text = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                if self.source[self.position] == "\n":
                    raise Exception("[Lexer] Unterminated string")
                text += self.source[self.position]
                self.position += 1

            if self.position >= len(self.source):
                raise Exception("[Lexer] Unterminated string")

            # Consome a aspa de fechamento
            self.position += 1
            self.next = Token("STR", text)
        elif current.isdigit():
            digits = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                digits += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(digits))
        elif current.isalpha():
            word = ""
            while self.position < len(self.source) and (
                self.source[self.position].isalnum() or self.source[self.position] == "_"
            ):
                word += self.source[self.position]
                self.position += 1

            if word in Lexer.RESERVED_WORDS:
                self.next = Token(Lexer.RESERVED_WORDS[word], word)
            elif word in Lexer.TYPES:
                self.next = Token("TYPE", word)
            elif word == "true" or word == "false":
                self.next = Token("BOOL", word == "true")
            else:
                self.next = Token("IDEN", word)
        else:
            raise Exception("[Lexer] Invalid Symbol '" + current + "'")


class Node:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            children = []
        self.children = children

    def evaluate(self, st):
        raise Exception("[Semantic] evaluate() not implemented for this node")


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        return Variable(self.value, "int")


class BoolVal(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        return Variable(self.value, "bool")


class StringVal(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        return Variable(self.value, "string")


def to_text(variable):
    # Representacao de um valor como texto (bool sai como no Go: true/false)
    if variable.type == "bool":
        return "true" if variable.value else "false"
    return str(variable.value)


def evaluate_condition(node, st, statement):
    condition = node.evaluate(st)
    if condition.type != "bool":
        raise Exception("[Semantic] " + statement + " condition must be bool, got " + condition.type)
    return condition.value


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        operand = self.children[0].evaluate(st)

        if self.value in ("PLUS", "MINUS"):
            if operand.type != "int":
                raise Exception("[Semantic] Unary " + self.value + " requires int, got " + operand.type)
            return Variable(operand.value if self.value == "PLUS" else -operand.value, "int")
        elif self.value == "NOT":
            if operand.type != "bool":
                raise Exception("[Semantic] Operator ! requires bool, got " + operand.type)
            return Variable(not operand.value, "bool")
        else:
            raise Exception("[Semantic] Invalid unary operator " + str(self.value))


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)

        type_error = Exception(
            "[Semantic] Invalid operand types for " + self.value + ": " + left.type + " and " + right.type
        )

        # Chamada de funcao sem tipo de retorno nao produz valor para operar
        if left.type == "void" or right.type == "void":
            raise type_error

        if self.value == "PLUS":
            # Se algum lado e string, "+" concatena (o outro lado vira texto: 1 -> "1", true -> "true").
            # Precisa ser testado antes da soma, senao int + string cairia no erro de tipos
            if left.type == "string" or right.type == "string":
                return Variable(to_text(left) + to_text(right), "string")
            if left.type == "int" and right.type == "int":
                return Variable(left.value + right.value, "int")
            raise type_error

        elif self.value in ("MINUS", "MULT", "DIV"):
            if left.type != "int" or right.type != "int":
                raise type_error

            if self.value == "MINUS":
                return Variable(left.value - right.value, "int")
            if self.value == "MULT":
                return Variable(left.value * right.value, "int")

            if right.value == 0:
                raise Exception("[Semantic] Division by zero")

            # Divisao inteira truncada em direcao ao zero (estilo C)
            quotient = left.value // right.value
            if (left.value % right.value != 0) and ((left.value < 0) != (right.value < 0)):
                quotient = quotient + 1
            return Variable(quotient, "int")

        elif self.value == "EQ":
            if left.type != right.type:
                raise type_error
            return Variable(left.value == right.value, "bool")

        elif self.value in ("GT", "LT"):
            # Ordem so existe entre ints ou entre strings (lexicografica)
            if left.type != right.type or left.type == "bool":
                raise type_error
            if self.value == "GT":
                return Variable(left.value > right.value, "bool")
            return Variable(left.value < right.value, "bool")

        elif self.value in ("AND", "OR"):
            if left.type != "bool" or right.type != "bool":
                raise type_error
            if self.value == "AND":
                return Variable(left.value and right.value, "bool")
            return Variable(left.value or right.value, "bool")

        else:
            raise Exception("[Semantic] Invalid binary operator " + str(self.value))


class Identifier(Node):
    # Folha: value guarda o NOME da variavel; o valor fica na SymbolTable
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        variable = st.get_value(self.value)
        if variable.is_function:
            raise Exception("[Semantic] Function '" + self.value + "' used as a value (missing '()')")
        return variable


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        value = self.children[0].evaluate(st)
        if value.type == "void":
            raise Exception("[Semantic] Cannot print the result of a function without return type")
        print(to_text(value))


class Read(Node):
    # Folha: le uma linha do terminal e devolve o inteiro correspondente
    def __init__(self, value=None, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        entry = input()
        try:
            return Variable(int(entry.strip()), "int")
        except ValueError:
            raise Exception("[Semantic] Scanln expected an integer, got '" + entry + "'")


class VarDec(Node):
    # value = tipo da variavel, children[0] = Identifier, children[1] = expressao (opcional)
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        name = self.children[0].value
        st.create_variable(name, self.value, False)

        if len(self.children) == 2:
            st.set_value(name, self.children[1].evaluate(st))


class Assignment(Node):
    # children[0] = Identifier (so o nome e usado), children[1] = expressao
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        name = self.children[0].value
        st.set_value(name, self.children[1].evaluate(st))


class If(Node):
    # children[0] = condicao, children[1] = bloco then, children[2] = bloco else (opcional)
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        # Cada bloco tem seu proprio escopo; se ele executar um return, o valor sobe
        if evaluate_condition(self.children[0], st, "if"):
            return self.children[1].evaluate(SymbolTable(st))
        elif len(self.children) == 3:
            return self.children[2].evaluate(SymbolTable(st))


class While(Node):
    # children[0] = condicao, children[1] = bloco
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        # Escopo novo a cada iteracao (um "var" dentro do laco nao e redeclarado); um return interrompe o laco
        while evaluate_condition(self.children[0], st, "for"):
            result = self.children[1].evaluate(SymbolTable(st))
            if result is not None:
                return result


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(st)

            # Bloco dentro de bloco ganha uma tabela encadeada (escopo novo)
            if isinstance(child, Block):
                result = child.evaluate(SymbolTable(st))
            else:
                result = child.evaluate(st)

            # Um return executado dentro de um if/for/bloco interno encerra este bloco tambem.
            # O valor de uma chamada de funcao usada como instrucao e descartado
            if result is not None and not isinstance(child, FuncCall):
                return result


class Return(Node):
    # children[0] = expressao retornada
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        return self.children[0].evaluate(st)


class FuncDec(Node):
    # value = tipo de retorno ("void" se nao declarar), children[0] = Identifier com o nome,
    # children[1:-1] = VarDec dos argumentos, children[-1] = Block do corpo
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        # A "variavel" da funcao guarda o proprio no como valor
        name = self.children[0].value
        st.create_variable(name, self.value, True)
        st.get_value(name).value = self


class FuncCall(Node):
    # value = nome da funcao, children = expressoes passadas como argumento
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        function = st.get_value(self.value)
        if not function.is_function:
            raise Exception("[Semantic] '" + self.value + "' is not a function")

        declaration = function.value
        arguments = declaration.children[1:-1]
        if len(arguments) != len(self.children):
            raise Exception(
                "[Semantic] Function '" + self.value + "' expects " + str(len(arguments))
                + " argument(s), got " + str(len(self.children))
            )

        # O escopo da funcao e encadeado no escopo global (onde as funcoes sao declaradas),
        # nao no escopo de quem chamou
        global_st = st
        while global_st.parent is not None:
            global_st = global_st.parent
        function_st = SymbolTable(global_st)

        # Declara cada argumento e atribui o valor passado (avaliado no escopo de quem chamou)
        for argument, expression in zip(arguments, self.children):
            argument.evaluate(function_st)
            function_st.set_value(argument.children[0].value, expression.evaluate(st))

        result = declaration.children[-1].evaluate(function_st)

        if declaration.value == "void":
            if result is not None:
                raise Exception("[Semantic] Function '" + self.value + "' has no return type and cannot return a value")
            return Variable(None, "void")

        if result is None:
            raise Exception("[Semantic] Function '" + self.value + "' must return a value of type " + declaration.value)
        if result.type != declaration.value:
            raise Exception(
                "[Semantic] Function '" + self.value + "' must return " + declaration.value + ", got " + result.type
            )
        return Variable(result.value, result.type)


class NoOp(Node):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        pass


def parse_function_call(name):
    # Chamado com o "(" como proximo token: consome "(", argumentos separados por "," e ")"
    Parser.lexer.select_next()

    arguments = []
    if Parser.lexer.next.type != "CLOSE_PAR":
        arguments.append(Parser.parse_bool_expression())
        while Parser.lexer.next.type == "COMMA":
            Parser.lexer.select_next()
            arguments.append(Parser.parse_bool_expression())

    if Parser.lexer.next.type != "CLOSE_PAR":
        raise Exception("[Parser] Expected ')' after arguments of '" + name + "', got " + Parser.lexer.next.type)
    Parser.lexer.select_next()

    return FuncCall(name, arguments)


class Parser:
    lexer = None

    @staticmethod
    def parse_program():
        # Fora das funcoes so podem existir declaracoes de funcoes e de variaveis globais
        children = []
        while Parser.lexer.next.type != "EOF":
            if Parser.lexer.next.type == "END":
                Parser.lexer.select_next()

            elif Parser.lexer.next.type in ("VAR", "FUNC"):
                if Parser.lexer.next.type == "VAR":
                    children.append(Parser.parse_var_declaration())
                else:
                    children.append(Parser.parse_func_declaration())

                if Parser.lexer.next.type != "END":
                    raise Exception("[Parser] Expected end of line after declaration, got " + Parser.lexer.next.type)
                Parser.lexer.select_next()

            else:
                raise Exception("[Parser] Expected function or variable declaration, got " + Parser.lexer.next.type)

        return Block("BLOCK", children)

    @staticmethod
    def parse_var_declaration():
        # "var" IDENTIFIER TYPE [ "=" BOOLEXPRESSION ] -> VarDec (o "\n" do final e cobrado por quem chamou)
        Parser.lexer.select_next()

        if Parser.lexer.next.type != "IDEN":
            raise Exception("[Parser] Expected identifier after var, got " + Parser.lexer.next.type)
        identifier = Identifier(Parser.lexer.next.value)
        Parser.lexer.select_next()

        if Parser.lexer.next.type != "TYPE":
            raise Exception("[Parser] Expected type after identifier, got " + Parser.lexer.next.type)
        var_type = Parser.lexer.next.value
        Parser.lexer.select_next()

        children = [identifier]
        if Parser.lexer.next.type == "ASSIGN":
            Parser.lexer.select_next()
            children.append(Parser.parse_bool_expression())

        return VarDec(var_type, children)

    @staticmethod
    def parse_func_declaration():
        # Consome "func"
        Parser.lexer.select_next()

        if Parser.lexer.next.type != "IDEN":
            raise Exception("[Parser] Expected function name after func, got " + Parser.lexer.next.type)
        children = [Identifier(Parser.lexer.next.value)]
        Parser.lexer.select_next()

        if Parser.lexer.next.type != "OPEN_PAR":
            raise Exception("[Parser] Expected '(' after function name, got " + Parser.lexer.next.type)
        Parser.lexer.select_next()

        # Argumentos: "nome tipo" separados por ","; cada um vira um VarDec sem valor
        while Parser.lexer.next.type != "CLOSE_PAR":
            if len(children) > 1:
                if Parser.lexer.next.type != "COMMA":
                    raise Exception("[Parser] Expected ',' or ')' in arguments, got " + Parser.lexer.next.type)
                Parser.lexer.select_next()

            if Parser.lexer.next.type != "IDEN":
                raise Exception("[Parser] Expected argument name, got " + Parser.lexer.next.type)
            argument = Identifier(Parser.lexer.next.value)
            Parser.lexer.select_next()

            if Parser.lexer.next.type != "TYPE":
                raise Exception("[Parser] Expected type after argument name, got " + Parser.lexer.next.type)
            children.append(VarDec(Parser.lexer.next.value, [argument]))
            Parser.lexer.select_next()

        # Consome ")"
        Parser.lexer.select_next()

        # Tipo de retorno e opcional: sem ele a funcao nao pode dar return
        return_type = "void"
        if Parser.lexer.next.type == "TYPE":
            return_type = Parser.lexer.next.value
            Parser.lexer.select_next()

        children.append(Parser.parse_block())

        return FuncDec(return_type, children)

    @staticmethod
    def parse_block():
        if Parser.lexer.next.type != "OPEN_BRA":
            raise Exception("[Parser] Expected '{', got " + Parser.lexer.next.type)
        Parser.lexer.select_next()

        if Parser.lexer.next.type != "END":
            raise Exception("[Parser] Expected end of line after '{', got " + Parser.lexer.next.type)

        children = []
        while Parser.lexer.next.type != "CLOSE_BRA":
            if Parser.lexer.next.type == "EOF":
                raise Exception("[Parser] Expected '}', got EOF")
            children.append(Parser.parse_statement())

        # Consome o "}" (o END que o segue e cobrado por quem chamou)
        Parser.lexer.select_next()

        return Block("BLOCK", children)

    @staticmethod
    def parse_statement():
        token = Parser.lexer.next

        if token.type == "END":
            node = NoOp()

        elif token.type == "IDEN":
            identifier = Identifier(token.value)
            Parser.lexer.select_next()

            # "nome(" e chamada de funcao; "nome =" e atribuicao
            if Parser.lexer.next.type == "OPEN_PAR":
                node = parse_function_call(token.value)
            elif Parser.lexer.next.type == "ASSIGN":
                Parser.lexer.select_next()
                node = Assignment("ASSIGN", [identifier, Parser.parse_bool_expression()])
            else:
                raise Exception("[Parser] Expected '=' or '(' after identifier, got " + Parser.lexer.next.type)

        elif token.type == "RETURN":
            Parser.lexer.select_next()
            node = Return("RETURN", [Parser.parse_bool_expression()])

        elif token.type == "VAR":
            node = Parser.parse_var_declaration()

        elif token.type == "PRINT":
            Parser.lexer.select_next()

            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] Expected '(' after Println, got " + Parser.lexer.next.type)
            Parser.lexer.select_next()

            expression = Parser.parse_bool_expression()

            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Expected ')', got " + Parser.lexer.next.type)
            Parser.lexer.select_next()

            node = Print("PRINT", [expression])

        elif token.type == "IF":
            Parser.lexer.select_next()

            condition = Parser.parse_bool_expression()
            children = [condition, Parser.parse_block()]

            if Parser.lexer.next.type == "ELSE":
                Parser.lexer.select_next()
                children.append(Parser.parse_block())

            node = If("IF", children)

        elif token.type == "WHILE":
            Parser.lexer.select_next()

            condition = Parser.parse_bool_expression()
            node = While("WHILE", [condition, Parser.parse_block()])

        elif token.type == "OPEN_BRA":
            node = Parser.parse_block()

        else:
            raise Exception("[Parser] Unexpected token " + token.type)

        # Toda instrucao termina com END ("\n")
        if Parser.lexer.next.type != "END":
            raise Exception("[Parser] Expected end of line, got " + Parser.lexer.next.type)
        Parser.lexer.select_next()

        return node

    @staticmethod
    def parse_factor():
        if Parser.lexer.next.type == "PLUS":
            Parser.lexer.select_next()
            child = Parser.parse_factor()
            return UnOp("PLUS", [child])

        if Parser.lexer.next.type == "MINUS":
            Parser.lexer.select_next()
            child = Parser.parse_factor()
            return UnOp("MINUS", [child])

        if Parser.lexer.next.type == "NOT":
            Parser.lexer.select_next()
            child = Parser.parse_factor()
            return UnOp("NOT", [child])

        if Parser.lexer.next.type == "OPEN_PAR":
            Parser.lexer.select_next()
            node = Parser.parse_bool_expression()

            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "READ":
            Parser.lexer.select_next()

            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] Expected '(' after Scanln, got " + Parser.lexer.next.type)
            Parser.lexer.select_next()

            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Expected ')' after Scanln(, got " + Parser.lexer.next.type)
            Parser.lexer.select_next()

            return Read("READ", [])

        if Parser.lexer.next.type == "INT":
            node = IntVal(Parser.lexer.next.value, [])
            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "STR":
            node = StringVal(Parser.lexer.next.value, [])
            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "BOOL":
            node = BoolVal(Parser.lexer.next.value, [])
            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "IDEN":
            name = Parser.lexer.next.value
            Parser.lexer.select_next()

            if Parser.lexer.next.type == "OPEN_PAR":
                return parse_function_call(name)
            return Identifier(name)

        raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

    @staticmethod
    def parse_term():
        result = Parser.parse_factor()

        while Parser.lexer.next.type == "MULT" or Parser.lexer.next.type == "DIV":
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()
            right = Parser.parse_factor()
            result = BinOp(operator, [result, right])

        return result

    @staticmethod
    def parse_expression():
        result = Parser.parse_term()

        while Parser.lexer.next.type == "PLUS" or Parser.lexer.next.type == "MINUS":
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()
            right = Parser.parse_term()
            result = BinOp(operator, [result, right])

        return result

    @staticmethod
    def parse_rel_expression():
        result = Parser.parse_expression()

        while Parser.lexer.next.type in ("EQ", "GT", "LT"):
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()
            right = Parser.parse_expression()
            result = BinOp(operator, [result, right])

        return result

    @staticmethod
    def parse_bool_term():
        result = Parser.parse_rel_expression()

        while Parser.lexer.next.type == "AND":
            Parser.lexer.select_next()
            right = Parser.parse_rel_expression()
            result = BinOp("AND", [result, right])

        return result

    @staticmethod
    def parse_bool_expression():
        result = Parser.parse_bool_term()

        while Parser.lexer.next.type == "OR":
            Parser.lexer.select_next()
            right = Parser.parse_bool_term()
            result = BinOp("OR", [result, right])

        return result

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        tree = Parser.parse_program()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

        # Depois de declarar globais e funcoes, o programa comeca chamando main() (obrigatoria)
        tree.children.append(FuncCall("main", []))

        return tree


def main():
    if len(sys.argv) != 2:
        raise Exception("[Parser] Uso: python3 main.py <arquivo.go>")

    with open(sys.argv[1], "r") as file:
        code = file.read() + "\n"

    code = PrePro.filter(code)

    tree = Parser.run(code)

    st = SymbolTable()
    tree.evaluate(st)


if __name__ == "__main__":
    main()
