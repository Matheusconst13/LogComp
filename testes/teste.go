// Roteiro 6 - programa de testes
// Cobre: leitura do terminal, condicionais e lacos com &&, || e !
// (a partir da v2.2 as variaveis precisam ser declaradas com var)

// --- Leitura do terminal ---
var a int = Scanln()
var b int = Scanln()

Println(a)
Println(b)

// --- Condicional com AND ---
if a > 0 && b > 0 {
    Println(1)
} else {
    Println(0)
}

// --- Condicional com OR ---
if a == 0 || b == 0 {
    Println(10)
} else {
    Println(20)
}

// --- Condicional com NOT (e if/else aninhado) ---
if !(a > b) {
    if a == b {
        Println(100)
    } else {
        Println(200)
    }
} else {
    Println(300)
}

// --- Condicional sem else ---
if a + b > 4 && !(a == b) {
    Println(42)
}

// --- Laco com OR: fatorial de b ---
var i int = 1
var f int = 1
if b < 2 {
    f = 1
} else {
    for i < b || i == b {
        f = f * i
        i = i + 1
    }
}
Println(f)

// --- Laco com AND: soma de a ate b-1, com guarda de seguranca ---
var s int = 0
var k int = a
for k < b && s < 1000 {
    s = s + k
    k = k + 1
}
Println(s)

// --- Laco com NOT: contagem regressiva a partir de b ---
var c int = 0
var m int = b
for !(m == 0) {
    c = c + 1
    m = m - 1
}
Println(c)

// --- Expressoes booleanas fora de condicionais ---
var t bool = a < b && b > 0
Println(t)
Println(!t)
Println(a == a || a > b)
