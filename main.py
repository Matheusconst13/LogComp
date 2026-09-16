import sys


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        # Ignora espacos em branco
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1

        # Fim da entrada
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
        elif current.isdigit():
            digits = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                digits += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(digits))
        else:
            raise Exception("[Lexer] Invalid Symbol '" + current + "'")


class Node:
    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            children = []
        self.children = children

    def evaluate(self):
        raise Exception("[Semantic] evaluate() not implemented for this node")


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return self.value


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        operand = self.children[0].evaluate()

        if self.value == "PLUS":
            return operand
        elif self.value == "MINUS":
            return -operand
        else:
            raise Exception("[Semantic] Invalid unary operator " + str(self.value))


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        left = self.children[0].evaluate()
        right = self.children[1].evaluate()

        if self.value == "PLUS":
            return left + right
        elif self.value == "MINUS":
            return left - right
        elif self.value == "MULT":
            return left * right
        elif self.value == "DIV":
            # Divisao inteira truncada em direcao ao zero (estilo C)
            quotient = left // right
            if (left % right != 0) and ((left < 0) != (right < 0)):
                quotient = quotient + 1
            return quotient
        else:
            raise Exception("[Semantic] Invalid binary operator " + str(self.value))


class Parser:
    lexer = None

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

        if Parser.lexer.next.type == "OPEN_PAR":
            Parser.lexer.select_next()
            node = Parser.parse_expression()

            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "INT":
            node = IntVal(Parser.lexer.next.value, [])
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
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        tree = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

        return tree


def main():
    if len(sys.argv) != 2:
        raise Exception("[Parser] Uso: python3 main.py '<expressao>'")

    tree = Parser.run(sys.argv[1])
    print(tree.evaluate())


if __name__ == "__main__":
    main()