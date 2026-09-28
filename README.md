# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.0)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
STATEMENT = ( ε | ASSIGNMENT | PRINT ), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "Println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( "a" | ... | "z" | "A" | ... | "Z" ) ;
DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ) ;
```