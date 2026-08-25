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
    def parse_expression():
        if Parser.lexer.next.type != "INT":
            raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

        result = Parser.lexer.next.value
        Parser.lexer.select_next()

        while Parser.lexer.next.type == "PLUS" or Parser.lexer.next.type == "MINUS":
            operator = Parser.lexer.next.type
            Parser.lexer.select_next()

            if Parser.lexer.next.type != "INT":
                raise Exception("[Parser] Unexpected token " + Parser.lexer.next.type)

            if operator == "PLUS":
                result = result + Parser.lexer.next.value
            else:
                result = result - Parser.lexer.next.value

            Parser.lexer.select_next()

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