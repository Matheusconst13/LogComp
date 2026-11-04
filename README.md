# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v3.0)

## EBNF

```ebnf
PROGRAM        = { STATEMENT } ;
BLOCK          = "{", "\n", { STATEMENT }, "}" ;
STATEMENT      = ( "var", IDENTIFIER, TYPE, ( ε | "=", BOOLEXPRESSION ) | ( "Println", "(", BOOLEXPRESSION, ")" ) | ( "for", BOOLEXPRESSION, BLOCK ) | ( "if", BOOLEXPRESSION, BLOCK, ( ε | "else", BLOCK ) | ) | BLOCK | IDENTIFIER, "=", BOOLEXPRESSION | ε ), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM       = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION  = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION     = TERM, { ("+" | "-"), TERM } ;
TERM           = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR         = NUMBER | BOOLEAN | STRING | IDENTIFIER | ("!" | "+" | "-"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE           = "string" | "int" | "bool" ;
BOOLEAN        = "true" | "false" ;
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

As operações e os tipos aceitos em cada uma:

| Operador | Operandos | Resultado |
| --- | --- | --- |
| `+` | `int` e `int` | `int` (soma) |
| `+` | `string` e qualquer tipo (em qualquer ordem) | `string` (concatenação; `1` vira `"1"` e `true` vira `"true"`) |
| `-` `*` `/` | `int` e `int` | `int` |
| `==` | dois operandos do mesmo tipo | `bool` |
| `>` `<` | `int` e `int`, ou `string` e `string` | `bool` |
| `&&` `\|\|` | `bool` e `bool` | `bool` |
| `!` | `bool` | `bool` |
| `+` `-` unários | `int` | `int` |

As condições de `if` e `for` precisam ser `bool`. `Scanln()` devolve `int`.
`Println` imprime booleanos como `true`/`false`. Somar `int` com `bool` é erro.

## Geração de código (v3.0)

O compilador não interpreta mais o programa: ele percorre a AST chamando
`generate()` em cada nó e escreve um arquivo NASM x86 (32 bits, Linux) com o
mesmo prefixo da entrada (`teste.go` gera `teste.asm`).

- A classe `Code` acumula as instruções (`append`) e escreve o arquivo com
  cabeçalho e rodapé (`dump`).
- Cada nó recebe um id único (`Node.newId()`), usado nos rótulos de `if`
  (`else_<id>`, `exit_<id>`) e `for` (`loop_<id>`, `exit_<id>`).
- Cada variável guarda em `shift` o deslocamento na pilha: a primeira fica em
  `[EBP-4]`, a segunda em `[EBP-8]` e assim por diante.
- O resultado de toda expressão fica em `EAX` e `ECX` é o registrador de apoio.
  Nas operações binárias o filho da direita é calculado primeiro e empilhado.
- Booleanos são `1`/`0`, e o `Println` imprime com `%d`.
- A checagem de tipos é feita durante a geração. Não é gerado código para
  strings: usar uma string é erro.

## Como executar

```bash
python3 main.py testes/roteiro8.go
```

```bash
nasm -f elf32 -o testes/roteiro8.o testes/roteiro8.asm
```

```bash
gcc -m32 -no-pie -nostartfiles -o testes/roteiro8 testes/roteiro8.o -e _start
```

```bash
./testes/roteiro8 < testes/roteiro8.in
```

O script `testes/run.sh` faz os quatro passos de uma vez:

```bash
testes/run.sh testes/roteiro8.go testes/roteiro8.in
```

## Testes

`testes/roteiro8.go` é o programa de testes do Roteiro 8. Ele passa por todos os
nós que geram código: declarações, atribuições, operadores unários e binários
(incluindo divisão com negativos), `if` com e sem `else`, `if` dentro de `for`,
`Println` e `Scanln`. Entrada em `testes/roteiro8.in` e saída esperada em
`testes/roteiro8.out`:

```bash
testes/run.sh testes/roteiro8.go testes/roteiro8.in | diff - testes/roteiro8.out
```

`testes/teste.go` (Roteiro 6) e `testes/roteiro6.go` (fatorial) também
compilam; na saída de `teste.go` os booleanos agora aparecem como `1`/`0`.

`testes/erros/` tem um programa por erro de tipo. Todos devem terminar com erro
na compilação, sem gerar `.asm`:

```bash
for f in testes/erros/*.go; do python3 main.py "$f" > /dev/null 2>&1 && echo "FALHOU: $f"; done
```

`testes/roteiro7.go` é o teste da v2.2. Ele usa strings, então só funciona até
a v2.2, quando o compilador ainda interpretava o programa.
