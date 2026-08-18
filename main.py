import sys

def main():
    text = sys.argv[1]
    i = 0
    total = 0
    op = 1
    espera_numero = True

    while i < len(text):
        if text[i] == " ":
            i += 1
        elif espera_numero:
            if not text[i].isdigit():
                raise Exception()
            
            num = 0
            while i < len(text) and text[i].isdigit():
                num = (num * 10) + int(text[i])
                i += 1
            
            total += op * num
            espera_numero = False
        else:
            if text[i] == "+":
                op = 1
            elif text[i] == "-":
                op = -1
            else:
                raise Exception()
            
            espera_numero = True
            i += 1

    if espera_numero:
        raise Exception()

    print(total)

if __name__ == "__main__":
    main()