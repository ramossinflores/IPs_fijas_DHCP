import re

def validar_nota(nota):
    regex = r"^(?:NA|\d+(\.\d{1,2})?)$"
    match = re.search(regex, nota)
    if match:
        if nota != "NA":
            nota = float(nota)
            if 0 <= nota <= 10:
                return nota
            else:
                print("La nota debe estar entre 0 y 10")
        else:
            return 0
    else:
        print("Valor inválido. Introduce un número entre 0 y 10 o NA.")
    return None

while True:
    sri = validar_nota(input("SRI: "))
    if sri != None:
        break


while True:
    aso = validar_nota(input("ASO: "))
    if aso != None:
        break

while True:
    iaw = validar_nota(input("IAW: "))
    if iaw != None:
        break

media = (sri + aso + iaw)/3

if media < 5:
    print("Estás rsuspenso.")
elif 5 <= media > 6:
    print("Suficiente")
elif 6 <= media > 7:
    print("Bien")
elif 7 <= media > 9:
    print("Suficiente")
elif 9 <= media > 10:
    print("Suficiente")
else:
    print("Bien hecho. Tienes  matrícula.")