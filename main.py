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


class Parser:
    lexer = None

    @staticmethod
    def parse_factor():
        if Parser.lexer.next.type == "PLUS":
            Parser.lexer.select_next()
            result = Parser.parse_factor()
            return result

        if Parser.lexer.next.type == "MINUS":
            Parser.lexer.select_next()
            result = Parser.parse_factor()
            return -result

        if Parser.lexer.next.type == "OPEN_PAR":
            Parser.lexer.select_next()
            result = Parser.parse_expression()

            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

            Parser.lexer.select_next()
            return result

        if Parser.lexer.next.type == "INT":
            result = Parser.lexer.next.value
            Parser.lexer.select_next()
            return result

        raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

    @staticmethod
    def parse_term():
        result = Parser.parse_factor()

        while Parser.lexer.next.type == "MULT" or Parser.lexer.next.type == "DIV":
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()
            value = Parser.parse_factor()

            if operator == "MULT":
                result = result * value
            else:
                # Divisao inteira truncada em direcao ao zero (estilo C)
                quotient = result // value
                if (result % value != 0) and ((result < 0) != (value < 0)):
                    quotient = quotient + 1
                result = quotient

        return result

    @staticmethod
    def parse_expression():
        result = Parser.parse_term()

        while Parser.lexer.next.type == "PLUS" or Parser.lexer.next.type == "MINUS":
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()
            value = Parser.parse_term()

            if operator == "PLUS":
                result = result + value
            else:
                result = result - value

        return result

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        result = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

        return result


def main():
    if len(sys.argv) != 2:
        raise Exception("[Parser] Uso: python3 main.py '<expressao>'")

    result = Parser.run(sys.argv[1])
    print(result)


if __name__ == "__main__":
    main()