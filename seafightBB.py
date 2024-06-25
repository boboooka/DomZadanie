from random import randint

class BoardException(Exception):
    pass
class BoardOutException(BoardException):
    pass
class BoardUsedException(BoardException):
    pass
class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow                         # Нос (начальная точка) корабля
        self.length = length
        self.orientation = orientation         # Ориентация корабля: 0 - горизонтально, 1 - вертикально
        self.lives = length

    @property
    def dots(self):                #   Описание точек корабля в зависимости от ориентации
        ship_dots = []
        for i in range(self.length):
            if self.orientation == 0:
                cur_dot = Dot(self.bow.x + i, self.bow.y)
            else:
                cur_dot = Dot(self.bow.x, self.bow.y + i)
            ship_dots.append(cur_dot)

        return ship_dots

    def shooten(self, shot):             #   Проверка на попадание по кораблю
        return shot in self.dots


class Board:
    def __init__(self, hide = False, size = 6):
        self.size = size
        self.hide = hide
        self.count = 0
        self.field = [["o"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        header = "   | " + " | ".join(map(str, range(1, 7))) + " |"
        rows = [f"{i + 1}  | " + " | ".join(row) + " |" for i, row in enumerate(self.field)]

        result = header + "\n" + "\n".join(rows)

        if self.hide:                 # Скрываем символы кораблей компьютера
            result = result.replace("X", "o")
        return result

    def out(self, d):            # Проверка находится ли точка за пределами доски
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb = False):   # Обводим уничтоженный корабль
        near = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "*"
                    self.busy.append(cur)

    def add_ship(self, ship):            # Проверяем, можно ли добавить корабль на доску
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException("Нужно разместить корабль в другом месте!")

        for dot in ship.dots:
            self.field[dot.x][dot.y] = "X"
            self.busy.append(dot)           # Добавляем точки корабля в список занятых точек

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException("Стреляем только по доске, будь внимательнее!")

        if dot in self.busy:
            raise BoardUsedException("Сюда мы уже шмаляли! Выбери другие координаты!")

        self.busy.append(dot)

        for ship in self.ships:         # Проверяем попадание по какому-нибудь кораблю
            if ship.shooten(dot):
                ship.lives -= 1
                self.field[dot.x][dot.y] = "■"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль пошёл ко дну!")
                    return False
                else:
                    print("Корабль подбит! Добивай!")
                    return True

        self.field[dot.x][dot.y] = "*"    # Если выстрел не попал по кораблю, отмечаем промах
        print("Ты промазал!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()               # Запрос координат для выстрела
                repeat = self.enemy.shot(target)  # Выстрел по полученным координатам
                return repeat
            except BoardException as e:
                print(e)
                continue

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ходит компьютер: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Твой ход: ").split()

            if len(cords) != 2:
                print("Введите две координаты через пробел! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):     # Генерируем случайную доску для игры
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("""
    --------------------------------
        Приветствую тебя
        в игре "Морской бой"!
    --------------------------------
        формат ввода для 
         выстрела: x y
        x - номер строки
        y - номер столбца
    --------------------------------
        условные обозначения:
        "X"- коробль на поле
        "*" - промах
        "■" - попадание по кораблю
    """)

    def print_boards(self):
        print("-" * 30)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 30)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-" * 30)

    def loop(self):
        num = 0
        while True:
            self.print_boards()

            if num % 2 == 0:
                print("\033[94m Время для твоего хода!\033[0m")
                repeat = self.us.move()
            else:
                print("\033[93m Ход компьютера!\033[0m")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 30)
                print("\033[96m✸✸✸ Поздравляю, ты победил(а)! ✸✸✸\033[0m")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 30)
                print("\033[91m✸✸✸ Компьютер тебя одолел! ✸✸✸\033[0m")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
