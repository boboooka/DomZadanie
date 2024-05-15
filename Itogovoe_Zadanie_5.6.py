print(' -Начинаем игру КРЕСТИКИ-НОЛИКИ- ')
print(' Формат ввода - x (пробел) y ')
print(' x - номер строки ')
print(' у - номер столбца ')

igrovoe_pole = [[" "] * 3 for i in range(3) ] # создаём заготовку для игрового поля

def pokaz_polya():     # функция для вывода игрового поля в терминал
    print("  0 1 2")
    for i in range(3):
        print(f"{i} {igrovoe_pole[i][0]} {igrovoe_pole[i][1]} {igrovoe_pole[i][2]}")

def opros():           # функция для запроса координат от пользователя + проверка диапазона и пусто ли поле
    while True:
        koord = input(" Введите координаты поля : ").split() # проверка корректности координат по длинне
        if len(koord) != 2:
            print(" Введите координаты поля ЧЕРЕЗ ПРОБЕЛ! : ")
            continue
        x, y = koord

        if not(x.isdigit()) or not(y.isdigit()):    # проверка является ли координата числом
            print(" Введите координаты поля В ВИДЕ ЧИСЕЛ! : ")
            continue
        x, y = int(x), int(y)

        if 0 <= x <= 2 and 0 <= y <= 2: # проверка диапазона и занято ли поле
            if igrovoe_pole[x][y] == " ":
                return x, y
            else:
                print(" Поле занято символом! Введите другие координаты! ")
        else:
            print(" Координаты вне диапазона! ")

def pobed_komb():
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(igrovoe_pole[i][j]) # проверка строк
            if symbols == ["x", "x", "x"]:
                print(" Крестик победил! ")
                return True
            if symbols == ["o", "o", "o"]:
                print(" Нолик победил! ")
                return True
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(igrovoe_pole[j][i]) # проверка столбцов
            if symbols == ["x", "x", "x"]:
                print(" Крестик победил! ")
                return True
            if symbols == ["o", "o", "o"]:
                print(" Нолик победил! ")
                return True
    symbols = []
    for i in range(3):
        symbols.append(igrovoe_pole[i][i])  # проверка диагонали
        if symbols == ["x", "x", "x"]:
            print(" Крестик победил! ")
            return True
        if symbols == ["o", "o", "o"]:
            print(" Нолик победил! ")
            return True

    symbols = []
    for i in range(3):
        symbols.append(igrovoe_pole[i][2-i])  # проверка диагонали
        if symbols == ["x", "x", "x"]:
            print(" Крестик победил! ")
            return True
        if symbols == ["o", "o", "o"]:
            print(" Нолик победил! ")
            return True


hody = 0 # всего 9 ходов
while True:
    hody += 1

    pokaz_polya()

    if hody % 2 == 1:
        print(" Ход крестика ")
    else:
        print(" Ход нолика ")

    x, y = opros()

    if hody % 2 == 1:
        igrovoe_pole[x][y] = "x"
    else:
        igrovoe_pole[x][y] = "o"

    if pobed_komb():
      break

    if hody == 9:
        print(" Ничья! ")
        break







