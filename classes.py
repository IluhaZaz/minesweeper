from random import randint

from constants import SIZE_START_CNT, MINES_START_CNT


class Cell:
    def __init__(self):
        self.is_shown = False


class MineStates:
    def __init__(self) -> None:
        self.states = [f'|💥|', '🧨', ' 🚩']
        self.hidden = '🧨'
        self.public = '| |'


class Mine(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.state = MineStates()
    
    def show(self) -> None:
        self.is_shown = True

    def boom(self) -> None:
        self.state.hidden = f'|💥|'
    
    def mark(self) -> None:
        self.state.public = ' 🚩'

    def unmark(self) -> None:
        self.state.public = '| |'
    
    def __str__(self) -> str:
        if self.is_shown:
            return self.state.hidden
        else:
            return self.state.public
        

class EmptyStates:
    def __init__(self) -> None:
        self.states = ['?', ' 🚩']
        self.hidden = '?'
        self.public = '| |'


class Empty(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.near_cnt = 0
        self.state = EmptyStates()
    
    def show(self) -> None:
        self.is_shown = True
    
    def mark(self) -> None:
        self.state.public = ' 🚩'

    def unmark(self) -> None:
        self.state.public = '| |'
        

class Field:
    def __init__(self, size: int, mines_cnt: int) -> None:
        if size**2 < mines_cnt:
            size = SIZE_START_CNT
            mines_cnt = MINES_START_CNT
        self.size = size
        self.mines_cnt = mines_cnt
        self.is_active = False
        self.field: dict[tuple[int], Cell] = dict()
        self.f_remain = self.mines_cnt
        self.fake_flag = 0

    def have_mine_at(self, x: int, y: int) -> bool:
        if type(self.field[(x, y)]) == Mine:
            return True
        return False

    def count_near_mines(self) -> None:
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
        
    def start_game(self) -> None:
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
    
    def show_field(self) -> None:
        cnt = 0
        for pos, obj in self.field.items():
            print(obj, sep = '', end = '')
            cnt += 1
            if cnt% self.size == 0:
                print()
    
    def end_game(self, is_win: bool) -> None:
        if is_win:
            print('Victory')
        else:
            print('Lose')
        for obj in self.field.values():
            obj.is_shown = True
        self.is_active = False
    
    def show_near_zeros(self, pos: tuple[int], visited: list):
        if self.field.get(pos, None) is None:
            return
        self.field[pos].show()
        if pos in visited:
            return
        visited.append(pos)
        if self.field[pos].near_cnt == 0:
            around = []
            x, y = pos
            for i in range(-1, 2):
                for j in range(-1, 2):
                    around.append((x + i, y + j))
            around.remove((x, y))
            for neighbour in around:
                self.show_near_zeros(neighbour, visited)
    
    def check(self, x: int, y: int) -> int:
        pos = (y - 1, x - 1)
        self.field[pos].is_shown = True
        if type(self.field[pos]) == Mine:
            self.field[pos].boom()
            self.end_game(False)
            return -1
        
        if self.field[pos].near_cnt == 0:
            self.show_near_zeros(pos, [])
        self.show_field()
        return self.field[pos].near_cnt
    
    def mark(self, x: int, y: int) -> bool:
        pos = (y - 1, x - 1)

        if self.field[pos].state.public == '| |':

            if type(self.field[pos]) == Mine:
                self.f_remain -= 1
            else:
                self.fake_flag += 1

            self.field[pos].mark()
            return True
        
        if type(self.field[pos]) == Mine:
            self.f_remain += 1
        else:
            self.fake_flag -=1

        self.field[pos].unmark()
        self.show_field()
        return False

    def check_win(self) -> int:
        if not self.is_active:
            return -1
        if(self.f_remain == 0 and self.fake_flag == 0):
            return 1
        return 0