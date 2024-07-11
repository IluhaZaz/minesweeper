from random import randint

class Cell:
    def __init__(self):
        self.is_shown = False

class MineStates:
    def __init__(self) -> None:
        self.states = [f'💥', '🧨', '🚩']
        self.hidden = '🧨'
        self.public = '| |'

class Mine(Cell):
    def __init__(self):
        super().__init__()
        self.state = MineStates()
    
    def show(self):
        self.is_shown = True

    def boom(self):
        self.state.hidden = f'💥'
    
    def mark(self):
        self.state.public = '🚩'

    def unmark(self):
        self.state.public = '| |'
    
    def __str__(self) -> str:
        if self.is_shown:
            return self.state.hidden
        else:
            return self.state.public

class EmptyStates:
    def __init__(self) -> None:
        self.states = ['?', '🚩']
        self.hidden = '?'
        self.public = '| |'

class Empty(Cell):
    def __init__(self):
        super().__init__()
        self.near_cnt = 0
        self.state = EmptyStates()
    
    def show(self):
        self.is_shown = True
    
    def mark(self):
        self.state.public = '🚩'

    def unmark(self):
        self.state.public = '| |'
    
    def __str__(self) -> str:
        if self.is_shown:
            return f"|{self.near_cnt}|"
        else:
            return self.state.public
        

class Field:
    def __init__(self, size: int, mines_cnt: int):
        self.size = size
        self.mines_cnt = mines_cnt
        self.is_active = False
        self.field: dict[tuple[int], Cell] = dict()

    def have_mine_at(self, x: int, y: int) -> bool:
        if type(self.field[(x, y)]) == Mine:
            return True
        return False

    def count_near_mines(self):
        for pos, obj in self.field.items():
            if type(obj) == Mine:
                around = []
                x, y = pos
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        around.append((x + i, y + j))
                around.remove((x, y))
                for neighbour in around:
                    if self.field.get(neighbour, None) is not None:
                        if type(self.field[neighbour]) == Empty:
                            self.field[neighbour].near_cnt += 1
        

    def start_game(self):
        for x in range(self.size):
            for y in range(self.size):
                self.field[(x, y)] = Empty()
        for _ in range(self.mines_cnt):
            pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            while self.have_mine_at(*pos):
                pos = (randint(0, self.size - 1), randint(0, self.size - 1))
            self.field[pos] = Mine()
        self.count_near_mines()
        self.is_active = True
    
    def show_field(self):
        cnt = 0
        for pos, obj in self.field.items():
            print(obj, sep = '', end = '')
            cnt += 1
            if cnt% self.size == 0:
                print()
    
    def end_game(self, is_win: bool):
        if is_win:
            print('Victory')
        else:
            print('Lose')
        for obj in self.field.values():
            obj.is_shown = True
        self.is_active = False
    
    def check(self, x: int, y: int):
        pos = (y - 1, x - 1)
        self.field[pos].is_shown = True
        if type(self.field[pos]) == Mine:
            self.field[pos].boom()
            self.end_game(False)
        else:
            self.field[pos].show()
    
    def mark(self, x: int, y: int):
        pos = (y - 1, x - 1)
        self.field[pos].mark()


f = Field(5, 15)
f.start_game()
f.check(4, 1)
f.show_field()
pass