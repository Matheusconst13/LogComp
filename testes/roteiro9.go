// Roteiro 9 - programa de testes (v2.3: funcoes e escopo)

// --- Exemplo do enunciado ---
var b int = 5 // Variavel Global

func soma(x int, y int) int {
  var a int // Variavel Local
  a = x + y
  Println(a) // Imprime 7
  return a
}

// --- Recursao ---
func fatorial(n int) int {
  if n < 2 {
    return 1
  }
  return n * fatorial(n - 1)
}

func fibonacci(n int) int {
  if n < 2 {
    return n
  } else {
    return fibonacci(n - 1) + fibonacci(n - 2)
  }
}

// --- Funcao chamada antes de ser declarada no arquivo, com bool e string ---
func eh_par(n int) bool {
  return n / 2 * 2 == n
}

func repete(s string, vezes int) string {
  var resultado string = ""
  var i int = 0
  for i < vezes {
    resultado = resultado + s
    i = i + 1
  }
  return resultado
}

// --- return de dentro de um for: primeiro divisor maior que 1 ---
func menor_divisor(n int) int {
  var d int = 2
  for d < n {
    if n / d * d == n {
      return d
    }
    d = d + 1
  }
  return n
}

// --- Funcao sem tipo de retorno que altera uma global ---
var contador int = 0

func incrementa() {
  contador = contador + 1
}

// --- Funcao que chama outra funcao ---
func soma_tres(x int, y int, z int) int {
  return soma(soma(x, y), z)
}

func main()  {
  var a int
  {
    var b int
    a = 3
    b = soma(a, 4)
    Println(b) // Imprime 7
  }
  Println(a) // Imprime 3
  Println(b) // Imprime 5

  Println(fatorial(5))
  Println(fibonacci(10))
  Println(eh_par(4))
  Println(eh_par(7))
  Println(repete("ab", 3))
  Println(menor_divisor(91))
  Println(menor_divisor(13))

  incrementa()
  incrementa()
  Println(contador)

  Println(soma_tres(1, 2, 3))

  // Argumento lido do terminal e expressao como argumento
  var n int = Scanln()
  Println(fatorial(n) + fatorial(n - 1))

  // Sombreamento: x local dentro do if nao altera o x de fora
  var x int = 1
  if x == 1 {
    var x int = 100
    Println(x)
  }
  Println(x)

  // var dentro de for (escopo novo a cada iteracao)
  var i int = 0
  for i < 2 {
    var dentro int = i * 10
    Println(dentro)
    i = i + 1
  }
}
