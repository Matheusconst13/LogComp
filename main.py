import re
import sys


class PrePro:
    @staticmethod
    def filter(code):
        # Remove tudo entre "//" e o fim da linha, preservando o "\n"
        return re.sub(r"//.*", "", code)


class Variable:
    def __init__(self, value):
        self.value = value


class SymbolTable:
    def __init__(self):
        self.table = {}

    def get_value(self, name):
        if name not in self.table:
            raise Exception("[Semantic] Undefined variable '" + name + "'")
        return self.table[name]

    def set_value(self, name, value):
        self.table[name] = Variable(value)


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
    }

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
        return self.value


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        operand = self.children[0].evaluate(st)

        if self.value == "PLUS":
            return operand
        elif self.value == "MINUS":
            return -operand
        elif self.value == "NOT":
            return 0 if operand != 0 else 1
        else:
            raise Exception("[Semantic] Invalid unary operator " + str(self.value))


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)

        if self.value == "PLUS":
            return left + right
        elif self.value == "MINUS":
            return left - right
        elif self.value == "MULT":
            return left * right
        elif self.value == "DIV":
            if right == 0:
                raise Exception("[Semantic] Division by zero")

            # Divisao inteira truncada em direcao ao zero (estilo C)
            quotient = left // right
            if (left % right != 0) and ((left < 0) != (right < 0)):
                quotient = quotient + 1
            return quotient
        elif self.value == "EQ":
            return 1 if left == right else 0
        elif self.value == "GT":
            return 1 if left > right else 0
        elif self.value == "LT":
            return 1 if left < right else 0
        elif self.value == "AND":
            return 1 if (left != 0 and right != 0) else 0
        elif self.value == "OR":
            return 1 if (left != 0 or right != 0) else 0
        else:
            raise Exception("[Semantic] Invalid binary operator " + str(self.value))


class Identifier(Node):
    # Folha: value guarda o NOME da variavel; o valor fica na SymbolTable
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        return st.get_value(self.value).value


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        print(self.children[0].evaluate(st))


class Read(Node):
    # Folha: le uma linha do terminal e devolve o inteiro correspondente
    def __init__(self, value=None, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        entry = input()
        try:
            return int(entry.strip())
        except ValueError:
            raise Exception("[Semantic] Scanln expected an integer, got '" + entry + "'")


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
        if self.children[0].evaluate(st) != 0:
            self.children[1].evaluate(st)
        elif len(self.children) == 3:
            self.children[2].evaluate(st)


class While(Node):
    # children[0] = condicao, children[1] = bloco
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        while self.children[0].evaluate(st) != 0:
            self.children[1].evaluate(st)


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)


class NoOp(Node):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)

    def evaluate(self, st):
        pass


class Parser:
    lexer = None

    @staticmethod
    def parse_program():
        children = []
        while Parser.lexer.next.type != "EOF":
            children.append(Parser.parse_statement())
        return Block("BLOCK", children)

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

            if Parser.lexer.next.type != "ASSIGN":
                raise Exception("[Parser] Expected '=' after identifier, got " + Parser.lexer.next.type)
            Parser.lexer.select_next()

            node = Assignment("ASSIGN", [identifier, Parser.parse_bool_expression()])

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

        if Parser.lexer.next.type == "IDEN":
            node = Identifier(Parser.lexer.next.value)
            Parser.lexer.select_next()
            return node

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
