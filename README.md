# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.1)

## EBNF

```ebnf
PROGRAM        = { STATEMENT } ;
BLOCK          = "{", "\n", { STATEMENT }, "}" ;
STATEMENT      = ( ( "Println", "(", BOOLEXPRESSION, ")" ) | ( "for", BOOLEXPRESSION, BLOCK ) | ( "if", BOOLEXPRESSION, BLOCK, ( "else", BLOCK ) | ε ) | ( IDENTIFIER, "=", BOOLEXPRESSION ) | BLOCK | ε ), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM       = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION  = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION     = TERM, { ("+" | "-"), TERM } ;
TERM           = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR         = NUMBER | IDENTIFIER | ("!" | "+" | "-"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
IDENTIFIER     = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER         = DIGIT, { DIGIT } ;
LETTER         = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
DIGIT          = "0" | "1" | ... | "9" ;
```

## Tokens

| Categoria | Símbolos |
| --- | --- |
| Aritméticos | `+` `PLUS`, `-` `MINUS`, `*` `MULT`, `/` `DIV` |
| Relacionais | `==` `EQ`, `>` `GT`, `<` `LT` |
| Booleanos | `&&` `AND`, `\|\|` `OR`, `!` `NOT` |
| Atribuição | `=` `ASSIGN` |
| Agrupamento | `(` `OPEN_PAR`, `)` `CLOSE_PAR`, `{` `OPEN_BRA`, `}` `CLOSE_BRA` |
| Palavras reservadas | `if` `IF`, `else` `ELSE`, `for` `WHILE`, `Println` `PRINT`, `Scanln` `READ` |
| Outros | `INT`, `IDEN`, `\n` `END`, `EOF` |

Valores booleanos são representados por inteiros: `0` é falso e qualquer valor
diferente de zero é verdadeiro. Os operadores relacionais e booleanos devolvem
`1` ou `0`.

## Como executar

```bash
python3 main.py testes/teste.go < testes/teste.in
```

## Testes

`testes/teste.go` é o programa de testes do Roteiro 6 e exercita todos os
elementos pedidos: leitura do terminal (`Scanln`), condicionais com `&&`, `||`
e `!` (incluindo `if` aninhado e `if` sem `else`), laços com `&&`, `||` e `!`, e
expressões booleanas usadas fora de condicionais. As entradas estão em
`testes/teste.in` e a saída esperada em `testes/teste.out`.

`testes/roteiro6.go` é o exemplo do enunciado (fatorial), com um `Println` no
final para mostrar o resultado.
