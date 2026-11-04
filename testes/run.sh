#!/bin/sh
# Compila um programa .go para assembly, monta, linka e executa.
# Uso: testes/run.sh programa.go [arquivo_de_entrada]
set -e

prefix="${1%.go}"
python3 "$(dirname "$0")/../main.py" "$1"
nasm -f elf32 -o "$prefix.o" "$prefix.asm"
gcc -m32 -no-pie -nostartfiles -o "$prefix" "$prefix.o" -e _start

if [ -n "$2" ]; then
    "$prefix" < "$2"
else
    "$prefix"
fi
