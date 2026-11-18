# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Matheusconst13/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

## Diagrama Sintático

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.3)

## EBNF

```ebnf
PROGRAM        = { ( "var", IDENTIFIER, TYPE, ( ε | "=", BOOLEXPRESSION ) | FUNCDEC | ε ), "\n" } ;
FUNCDEC        = "func", IDENTIFIER, "(", ( ε | IDENTIFIER, TYPE, { ",", IDENTIFIER, TYPE } ), ")", ( ε | TYPE ), BLOCK ;
BLOCK          = "{", "\n", { STATEMENT }, "}" ;
STATEMENT      = ( "var", IDENTIFIER, TYPE, ( ε | "=", BOOLEXPRESSION ) | ( "Println", "(", BOOLEXPRESSION, ")" ) | ( "for", BOOLEXPRESSION, BLOCK ) | ( "if", BOOLEXPRESSION, BLOCK, ( ε | "else", BLOCK ) | ) | ( "return", BOOLEXPRESSION ) | BLOCK | IDENTIFIER, ( "=", BOOLEXPRESSION | "(", ( ε | BOOLEXPRESSION, { ",", BOOLEXPRESSION } ), ")" ) | ε ), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM       = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION  = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION     = TERM, { ("+" | "-"), TERM } ;
TERM           = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR         = NUMBER | BOOLEAN | STRING | IDENTIFIER, ( ε | "(", ( ε | BOOLEXPRESSION, { ",", BOOLEXPRESSION } ), ")" ) | ("!" | "+" | "-"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
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
| Separador | `,` `COMMA` |
| Agrupamento | `(` `OPEN_PAR`, `)` `CLOSE_PAR`, `{` `OPEN_BRA`, `}` `CLOSE_BRA` |
| Palavras reservadas | `if` `IF`, `else` `ELSE`, `for` `WHILE`, `Println` `PRINT`, `Scanln` `READ`, `var` `VAR`, `func` `FUNC`, `return` `RETURN` |
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

## Funções e escopo

Fora das funções só podem existir declarações de variáveis globais (`var`) e de
funções (`func`). A função `main` é obrigatória: depois de declarar tudo, o
programa começa chamando `main()`.

```go
func soma(x int, y int) int {
  return x + y
}
```

- O tipo de retorno é opcional. Uma função sem tipo de retorno não pode dar
  `return`, e uma função com tipo precisa retornar um valor desse tipo.
- Não é possível declarar uma função dentro de outra.
- Uma chamada precisa passar a quantidade certa de argumentos, cada um com o
  tipo do parâmetro correspondente.
- Cada bloco (`{ }`, corpo de `if` e de `for`) tem seu próprio escopo. Uma
  variável declarada dentro dele deixa de existir quando o bloco termina, e uma
  variável de mesmo nome em um escopo interno esconde a de fora.
- O corpo de uma função enxerga seus parâmetros, suas variáveis locais e as
  globais, mas não as variáveis de quem a chamou. Isso permite recursão.

A `SymbolTable` é uma lista ligada reversa: cada tabela aponta para a tabela do
escopo de fora (`parent`), e a busca por um nome sobe até o escopo global.

## Como executar

```bash
python3 main.py testes/roteiro9.go < testes/roteiro9.in
```

## Testes

`testes/roteiro9.go` é o programa de testes do Roteiro 9. Ele roda o exemplo do
enunciado (globais, locais e blocos aninhados) e também cobre:

- funções recursivas (`fatorial` e `fibonacci`);
- funções que retornam `bool` e `string`;
- `return` de dentro de um `for`;
- uma função sem retorno que altera uma global;
- uma função que chama outra;
- um argumento lido com `Scanln`;
- sombreamento de variável dentro de um `if`;
- `var` dentro de um `for`.

A entrada está em `testes/roteiro9.in` e a saída esperada em
`testes/roteiro9.out`:

```bash
python3 main.py testes/roteiro9.go < testes/roteiro9.in | diff - testes/roteiro9.out
```

`testes/erros/` tem um programa para cada erro. Os erros de função e escopo são:

- quantidade errada de argumentos;
- argumento de tipo errado;
- função inexistente;
- variável fora de escopo ou local de outra função;
- `return` em função sem tipo;
- função com tipo que termina sem `return`;
- `return` de tipo errado;
- programa sem `main`;
- função dentro de função;
- função sem retorno usada em expressão;
- função duplicada;
- atribuição a uma função;
- instrução fora de função.

Os erros de tipo das versões anteriores também estão lá. Todos devem terminar
com erro:

```bash
for f in testes/erros/*.go; do python3 main.py "$f" > /dev/null 2>&1 && echo "FALHOU: $f"; done
```

Os programas das versões anteriores (`testes/teste.go`, `testes/roteiro6.go` e
`testes/roteiro7.go`) continuam funcionando. Eles só passaram a ficar dentro de
um `func main()`. `testes/roteiro8.go` é o teste da geração de código (v3.0),
que fica nas tags `v3.0.x`.
