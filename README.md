# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.0)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
STATEMENT = ( "Println", "(", EXPRESSION, ")" | IDENTIFIER, "=", EXPRESSION | ε ), "\n" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | IDENTIFIER | ("+" | "-"), FACTOR | "(", EXPRESSION, ")" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
DIGIT = "0" | "1" | ... | "9" ;
```