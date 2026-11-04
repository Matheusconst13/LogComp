// Roteiro 8 - programa de testes (v3.0: geracao de codigo)
// Cobre todos os nos que geram assembly: VarDec, Assignment, UnOp, BinOp,
// If (com e sem else, aninhado), For, Println e Scanln

{ // Teste geral (adaptado do teste do servidor, sem strings)
  var x_1 int
  x_1 = Scanln()

  Println(x_1)

  if (x_1 > 1 && !!!(x_1 < 1)) || x_1 == 3 {
    x_1 = 2
  }

  var x int = 3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2))
  var y_1 int = 3
  y_1 = y_1 + x_1
  var z__ int
  z__ = x + y_1

  if x_1 == 3 {
    x_1 = 2
  } else {
    x_1 = 3
  }

  x_1 = 0
  for x_1 < 1 || x == 2 {
    Println(x_1)
    x_1 = x_1 + 1
  }

  {
    {
    }
  }

  Println(x_1)
  Println(x)
  Println(z__+1)

  // Todas as operacoes com int
  var y int = 2
  var z int
  z = (y - 1)
  Println(y+z)
  Println(y-z)
  Println(y*z)
  Println(y/z)
  Println(y == z)
  Println(y < z)
  Println(y > z)
}

// Divisao e unarios com negativos (divisao trunca em direcao ao zero)
Println(-7 / 2)
Println(7 / -2)
Println(-(3 - 10))

// Booleanos (impressos como 1/0)
var ok bool = true
var flag bool
Println(ok)
Println(flag)
flag = !ok || 3 > 2 && !(1 == 2)
Println(flag)
Println(ok == flag)

// if aninhado dentro de for: soma dos pares de 1 a 10
var i int = 1
var pares int = 0
for i < 11 {
  if i / 2 * 2 == i {
    pares = pares + i
  }
  i = i + 1
}
Println(pares)

// Fatorial (exemplo do enunciado)
var n int = 5
var f int = 1
i = 2
for i < n + 1 {
  f = f * i
  i = i + 1
}
Println(f)
