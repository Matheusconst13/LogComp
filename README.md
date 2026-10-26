# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.2)

## EBNF

```ebnf
PROGRAM        = { STATEMENT } ;
BLOCK          = "{", "\n", { STATEMENT }, "}" ;
STATEMENT      = ( ( "Println", "(", BOOLEXPRESSION, ")" ) | ( "for", BOOLEXPRESSION, BLOCK ) | ( "if", BOOLEXPRESSION, BLOCK, ( "else", BLOCK ) | ε ) | ( IDENTIFIER, "=", BOOLEXPRESSION ) | ( "var", IDENTIFIER, TYPE, ( "=", BOOLEXPRESSION ) | ε ) | BLOCK | ε ), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM       = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION  = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION     = TERM, { ("+" | "-"), TERM } ;
TERM           = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR         = NUMBER | STRING | BOOL | IDENTIFIER | ("!" | "+" | "-"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE           = "int" | "string" | "bool" ;
BOOL           = "true" | "false" ;
STRING         = '"', { "..." }, '"' ;
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
| Palavras reservadas | `if` `IF`, `else` `ELSE`, `for` `WHILE`, `Println` `PRINT`, `Scanln` `READ`, `var` `VAR` |
| Tipos | `int`, `string`, `bool` `TYPE` |
| Literais | `INT`, `true`/`false` `BOOL`, `"..."` `STR` |
| Outros | `IDEN`, `\n` `END`, `EOF` |

## Tipos

Toda variável precisa ser declarada com `var nome tipo` (opcionalmente com
`= expressão`) antes de ser usada. Sem atribuição ela recebe o valor zero do
tipo: `0`, `""` ou `false`. Redeclarar uma variável, atribuir a uma variável
não declarada ou atribuir um valor de outro tipo é erro.

As operações seguem as regras do Go (sem conversão implícita):

| Operador | Operandos | Resultado |
| --- | --- | --- |
| `+` | `int` e `int` | `int` (soma) |
| `+` | `string` e `string` | `string` (concatenação) |
| `-` `*` `/` | `int` e `int` | `int` |
| `==` | dois operandos do mesmo tipo | `bool` |
| `>` `<` | `int` e `int`, ou `string` e `string` | `bool` |
| `&&` `\|\|` | `bool` e `bool` | `bool` |
| `!` | `bool` | `bool` |
| `+` `-` unários | `int` | `int` |

As condições de `if` e `for` precisam ser `bool`. `Scanln()` devolve `int`.
`Println` imprime booleanos como `true`/`false`.

## Como executar

```bash
python3 main.py testes/teste.go < testes/teste.in
```

## Testes

`testes/roteiro7.go` é o programa de testes do Roteiro 7. Ele declara e opera
variáveis de todos os tipos (com e sem valor inicial), concatena strings,
compara strings e booleanos, roda o fatorial do Roteiro 6 e usa strings para
controlar um `if` e um `for`. Entrada em `testes/roteiro7.in` e saída esperada
em `testes/roteiro7.out`:

```bash
python3 main.py testes/roteiro7.go < testes/roteiro7.in | diff - testes/roteiro7.out
```

`testes/erros/` tem um programa por erro de tipo (soma de `int` com `string`,
`bool` em operação aritmética, atribuição e declaração com tipo errado,
variável não declarada ou redeclarada, `&&` com `int`, `!` e `-` em string,
`==` entre tipos diferentes, `if`/`for` com condição que não é `bool` e string
sem fechar). Todos devem terminar com erro:

```bash
for f in testes/erros/*.go; do python3 main.py "$f" > /dev/null 2>&1 && echo "FALHOU: $f"; done
```

`testes/teste.go` (Roteiro 6) e `testes/roteiro6.go` (fatorial do enunciado)
continuam funcionando; só ganharam as declarações `var` que a v2.2 exige.
Entradas de `teste.go` em `testes/teste.in` e saída esperada em
`testes/teste.out`.
