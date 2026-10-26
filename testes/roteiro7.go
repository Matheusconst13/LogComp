// Roteiro 7 - programa de testes (v2.2: tipos e strings)
// Cobre: variaveis de todos os tipos, programa antigo ainda funcionando
// e if/for controlados por strings. Os erros de tipo ficam em testes/erros/

// --- Declaracoes de todos os tipos (com e sem atribuicao) ---
var n int = Scanln()
var x int
var nome string = "Log"
var vazio string
var ok bool = true
var flag bool

Println(n)
Println(x)
Println(nome)
Println(vazio)
Println(ok)
Println(flag)

// --- Operacoes com cada tipo ---
x = n * 2 + 1
nome = nome + "Comp"
flag = !ok || x > 10
Println(x)
Println(nome)
Println(flag)
Println("concat: " + "a" + "b")
Println("x = " + x)
Println(x + " e " + ok)
Println(nome + (x > 5))
Println(nome == "LogComp")
Println("abc" < "abd")
Println(ok == flag)

// --- Programa antigo (fatorial do Roteiro 6) ainda funciona ---
var i int = 1
var f int = 1
for i < n || i == n {
    f = f * i
    i = i + 1
}
Println(f)

// --- if com string ---
if nome == "LogComp" {
    Println("nome ok")
} else {
    Println("nome errado")
}

// --- for com string: monta uma string ate atingir o tamanho desejado ---
var s string = ""
var passos int = 0
for !(s == "*****") {
    s = s + "*"
    passos = passos + 1
}
Println(s)
Println(passos)

// --- Comentario dentro de string nao e removido ---
Println("http://insper.edu.br")
