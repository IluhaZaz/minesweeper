from random import randint

class Cell:
    def __init__(self):
        self.is_shown = False

class Mine(Cell):
    def __init__(self):
        super().__init__()
    
    def show(self):
        self.is_shown = True
    
    def __str__(self) -> str:
        return '💣' if self.is_shown else '⬜'

class Empty(Cell):
    def __init__(self):
        super().__init__()
        self.near_cnt = 0
    
    def show(self):
        self.is_shown = True
    
    def __str__(self) -> str:
        return '⬜'

class Field:
    def __init__(self, size: int, mines_cnt: int):
        self.size = size
        self.mines_cnt = mines_cnt
        self.is_active = False
        self.field: list[list[Cell]] = None

    def have_mine_at(self, x: int, y: int) -> bool:
        if type(self.field[y][x]) == Mine:
            return True
        return False

    def count_near_mines(self, x: int, y: int):
        pass

    def start_game(self):
        self.field = [[Empty() for _ in range(self.size)] for _ in range(self.size)]
        for _ in range(self.mines_cnt):
            pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            while self.have_mine_at(*pos):
                pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            self.field[pos[1]][pos[0]] = Mine()
        
        self.is_active = True
    
    def show_field(self):
        for row in self.field:
            for obj in row:
                print(obj, sep = '', end = '')
            print()

f = Field(5, 4)
f.start_game()
f.show_field()
pass