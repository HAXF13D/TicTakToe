from random import seed, randint


class TikTakToe:
    __modes__ = ["E", "M", "H"]
    __VOID_CHARACTER__ = '*'
    __SIGNS__ = {0: "x",
                 1: "o"}

    def __init__(self, user_sign):
        """
        :param user_sign: Знак игрока:
                                      0 -  "x"
                                      1 -  "o"
        """
        self.__make_field__(3, 3)
        self.__height__ = 3
        self.__width__ = 3
        self.__mode__ = "N"
        self.__ai_sign__ = self.__SIGNS__[1 - user_sign]
        self.__user_sign__ = self.__SIGNS__[user_sign]

    def status(self):
        """
        :return: True, если игра все еще идет
                 False, если игра закончилась или еще не началась
        """
        if self.__mode__ in self.__modes__:
            return True
        return False

    def get_field(self):
        """
        :return: Возвращает игровое поле (матрица 3х3)
        """
        return self.__field__

    def print_field(self):
        """
        :return: Выводит поле в консоль
        """
        for i in range(self.__height__):
            print(self.__field__[i])

    def start(self, mode):
        """
        :param mode: Сложность игры:
                                    "E" - простая
                                    "M" - средняя
                                    "H" - сложная
        :return: True, если сложность успешно установлена
        """
        if self.__mode__ not in self.__modes__:
            self.__mode__ = mode
            print("Запуск игры")
            return True
        return False

    def restart(self, user_sign, mode):
        """

        :param user_sign: Знак игрока:
                                      0 -  "x"
                                      1 -  "o"
        :param mode: Сложность игры:
                                    "E" - простая
                                    "M" - средняя
                                    "H" - сложная
        """
        print("Переапуск игры")
        self.__make_field__(3, 3)
        self.__height__ = 3
        self.__width__ = 3
        self.__mode__ = mode
        self.__ai_sign__ = self.__SIGNS__[1 - user_sign]
        self.__user_sign__ = self.__SIGNS__[user_sign]

    def move(self, x, y):
        """
        :param x: Номер строки в которую стваится символ
        :param y: Номер столбца в который ставится символ
        :return: True - если ход сделан успешно
        """
        if self.__mode__ in self.__modes__ and self.__field__[x][y] == self.__VOID_CHARACTER__:

            self.__field__[x][y] = self.__user_sign__  # Ход игрока

            if self.__win_check__(self.__field__) == "user":
                print("Вы победили")
                self.__mode__ = "N"
                return True

            if self.__win_check__(self.__field__) == "ai":
                print("Вы проиграли")
                self.__mode__ = "N"
                return True

            if self.__mode__ == "E":
                self.__easy_bot_move__()
            if self.__mode__ == "M":
                self.__med_bot_move__()
            if self.__mode__ == "H":
                self.__hard_bot_move__()

            if self.__win_check__(self.__field__) == "user":
                print("Вы победили")
                self.__mode__ = "N"
                return True

            if self.__win_check__(self.__field__) == "ai":
                print("Вы проиграли")
                self.__mode__ = "N"
                return True

            if self.__win_check__(self.__field__) == "draw":
                print("Ничья!")
                self.__mode__ = "N"
                return True

            return True

        return False

    def __easy_bot_move__(self):
        seed()
        x = randint(0, self.__height__ - 1)
        y = randint(0, self.__width__ - 1)
        while self.__field__[x][y] != self.__VOID_CHARACTER__:
            x = randint(0, self.__height__ - 1)
            y = randint(0, self.__width__ - 1)
        self.__field__[x][y] = self.__ai_sign__

    def __med_bot_move__(self):
        seed()
        choose = randint(0, 1)
        print(choose)
        if choose == 0:
            self.__easy_bot_move__()
        else:
            self.__hard_bot_move__()

    def __hard_bot_move__(self):
        best_score = -1000
        x_pos = None
        y_pos = None
        for i in range(self.__height__):
            for j in range(self.__height__):
                if self.__field__[i][j] == self.__VOID_CHARACTER__:
                    self.__field__[i][j] = self.__ai_sign__
                    score = self.__minimax__("user", self.__field__)
                    if score > best_score:
                        best_score = score
                        x_pos = i
                        y_pos = j
                    self.__field__[i][j] = self.__VOID_CHARACTER__
        if x_pos is not None and y_pos is not None:
            self.__field__[x_pos][y_pos] = self.__ai_sign__
            return True
        return False

    def __minimax__(self, current, temp_field):  # Дороботать
        if self.__win_check__(temp_field) == "ai":
            return 100
        if self.__win_check__(temp_field) == "user":
            return -100
        if self.__win_check__(temp_field) == "draw":
            return 0

        if current == "user":
            best_score = 1000
        else:
            best_score = -1000

        for i in range(self.__height__):
            for j in range(self.__width__):
                if temp_field[i][j] == self.__VOID_CHARACTER__:
                    if current == "user":
                        temp_field[i][j] = self.__user_sign__
                        score = self.__minimax__("ai", temp_field)
                        best_score = min(best_score, score)
                        temp_field[i][j] = self.__VOID_CHARACTER__
                    if current == "ai":
                        temp_field[i][j] = self.__ai_sign__
                        score = self.__minimax__("user", temp_field)
                        best_score = max(best_score, score)
                        temp_field[i][j] = self.__VOID_CHARACTER__
        return best_score

    def __make_field__(self, height, width):
        result = []
        for i in range(height):
            temp = []
            for j in range(width):
                temp.append(self.__VOID_CHARACTER__)
            result.append(temp)
        self.__field__ = result

    def __win_check__(self, field):

        if field[0][0] == self.__ai_sign__ and \
                field[1][1] == self.__ai_sign__ and \
                field[2][2] == self.__ai_sign__:
            return "ai"
        if field[0][2] == self.__ai_sign__ and \
                field[1][1] == self.__ai_sign__ and \
                field[2][0] == self.__ai_sign__:
            return "ai"
        if field[0][0] == self.__ai_sign__ and \
                field[0][1] == self.__ai_sign__ and \
                field[0][2] == self.__ai_sign__:
            return "ai"
        if field[1][0] == self.__ai_sign__ and \
                field[1][1] == self.__ai_sign__ and \
                field[1][2] == self.__ai_sign__:
            return "ai"
        if field[2][0] == self.__ai_sign__ and \
                field[2][1] == self.__ai_sign__ and \
                field[2][2] == self.__ai_sign__:
            return "ai"
        if field[0][0] == self.__ai_sign__ and \
                field[1][0] == self.__ai_sign__ and \
                field[2][0] == self.__ai_sign__:
            return "ai"
        if field[0][1] == self.__ai_sign__ and \
                field[1][1] == self.__ai_sign__ and \
                field[2][1] == self.__ai_sign__:
            return "ai"
        if field[0][2] == self.__ai_sign__ and \
                field[1][2] == self.__ai_sign__ and \
                field[2][2] == self.__ai_sign__:
            return "ai"

        if field[0][0] == self.__user_sign__ and \
                field[1][1] == self.__user_sign__ and \
                field[2][2] == self.__user_sign__:
            return "user"
        if field[0][2] == self.__user_sign__ and \
                field[1][1] == self.__user_sign__ and \
                field[2][0] == self.__user_sign__:
            return "user"
        if field[0][0] == self.__user_sign__ and \
                field[0][1] == self.__user_sign__ and \
                field[0][2] == self.__user_sign__:
            return "user"
        if field[1][0] == self.__user_sign__ and \
                field[1][1] == self.__user_sign__ and \
                field[1][2] == self.__user_sign__:
            return "user"
        if field[2][0] == self.__user_sign__ and \
                field[2][1] == self.__user_sign__ and \
                field[2][2] == self.__user_sign__:
            return "user"
        if field[0][0] == self.__user_sign__ and \
                field[1][0] == self.__user_sign__ and \
                field[2][0] == self.__user_sign__:
            return "user"
        if field[0][1] == self.__user_sign__ and \
                field[1][1] == self.__user_sign__ and \
                field[2][1] == self.__user_sign__:
            return "user"
        if field[0][2] == self.__user_sign__ and \
                field[1][2] == self.__user_sign__ and \
                field[2][2] == self.__user_sign__:
            return "user"

        count = True
        for i in range(self.__height__):
            for j in range(self.__width__):
                if field[i][j] == self.__VOID_CHARACTER__:
                    count = False
        if count:
            return "draw"

        return "nobody"
