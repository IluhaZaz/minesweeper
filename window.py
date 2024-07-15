from classes import Field, Mine
from PyQt5 import QtCore, QtGui, QtWidgets

from constants import *

class Ui_MainWindow(object):

    def __init__(self, size: int, mines_cnt: int):
        self.field = Field(size, mines_cnt)
        self.field.start_game()
        self.btn_cliked: int = 0

    def onclick_cell(self, cell_num: int):
        if self.btn_cliked%2 == 0:
            self.check_and_show(cell_num)
        else:
            self.set_flag(cell_num)
    
    def onclick_btn(self):
        self.btn_cliked += 1
        if self.btn_cliked%2 == 0:
            self.btn.setIcon(QtGui.QIcon("pictures\\shovel.png"))
            self.btn.setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
        else:
            self.btn.setIcon(QtGui.QIcon("pictures\\flag.png"))
            self.btn.setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
    
    def check_win(self) -> int:
        match(self.field.check_win()):
            case -1:
                self.field.end_game(False)
                return -1
            case 1:
                self.field.end_game(True)
                return 1
        return 0
            

    def check_and_show(self, cell_num: int):
        if not self.field.is_active:
            return
        if self.field.field[cell_num%self.field.size, 
                            cell_num//self.field.size].state.public == ' 🚩':
            return
        res = self.field.check(cell_num//self.field.size + 1, cell_num%self.field.size + 1)
        self.show_field()
        if res == -1:
            self.field.end_game(False)
            self.smile.setIcon(QtGui.QIcon("pictures\\sad.png"))
    
    def set_flag(self, cell_num: int):
        if not self.field.is_active:
            return        
        if self.field.field[cell_num%self.field.size, cell_num//self.field.size].is_shown:
            return
        if self.field.mark(cell_num//self.field.size + 1, cell_num%self.field.size + 1):
            self.cells[cell_num].setIcon(QtGui.QIcon("pictures\\flag.png"))
            self.cells[cell_num].setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
        else:
            self.cells[cell_num].setIcon(QtGui.QIcon())

        match(self.check_win()):
            case 1:
                self.smile.setIcon(QtGui.QIcon("pictures\\joy.png"))
                self.show_all()

    def show_all(self):
        size = self.field.size
        for cell_num in range(size**2):
            pos = (cell_num%self.field.size, cell_num//self.field.size)
            if type(self.field.field[pos]) == Mine:
                self.cells[cell_num].setIcon(QtGui.QIcon("pictures\\mine.png" 
                                                         if self.field.field[pos].state.hidden == '🧨' 
                                                         else "pictures\\boom.jpg"))
                self.cells[cell_num].setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
            else:
                self.cells[cell_num].setText(str(self.field.field[pos].near_cnt))

    def show_field(self):
        size = self.field.size
        for cell_num in range(size**2):
            pos = (cell_num%self.field.size, cell_num//self.field.size)
            if self.field.field[pos].is_shown:
                if type(self.field.field[pos]) == Mine:
                    self.cells[cell_num].setIcon(QtGui.QIcon("pictures\\mine.png" 
                                                         if self.field.field[pos].state.hidden == '🧨' 
                                                         else "pictures\\boom.jpg"))
                    self.cells[cell_num].setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
                else:
                    self.cells[cell_num].setText(str(self.field.field[pos].near_cnt))

    
    def restart(self, MainWindow: QtWidgets.QMainWindow):     

        self.field = Field(int(self.size_label.text()[6:]), 
                           int(self.mines_label.text()[13:]))
        self.field.start_game()
        
        self.btn_cliked = 0

        self.setupUi(MainWindow)
        self.mines_slider.setValue(self.field.mines_cnt)
        self.size_slider.setValue(self.field.size)

    def onchange_mines_slider(self, val:int):
        self.mines_label.setText(f"Mines count: {val}")

    def onchange_size_slider(self, val:int):
        self.size_label.setText(f"Size: {val}")

    def setupUi(self, MainWindow: QtWidgets.QMainWindow):

        size = self.field.size

        MainWindow.setObjectName("Minesweeper")
        MainWindow.resize(round(CELL_SIZE*(size + 3.5) + 2*HORIZONTAL_PADDING + BORDER_W*size), 
                          round(CELL_SIZE*(size + 2) + 2*VERTICAL_PADDING) + BORDER_W*size)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("Minesweeper")
        self.centralwidget.setStyleSheet("background: #b5b5b5;")
        
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(HORIZONTAL_PADDING, VERTICAL_PADDING,
                                CELL_SIZE*size + BORDER_W*size, CELL_SIZE*size + BORDER_W*size)
        self.widget.setObjectName("widget")

        self.smile = QtWidgets.QPushButton(self.centralwidget)
        self.smile.setIcon(QtGui.QIcon("pictures\\normal.png"))
        self.smile.setIconSize(QtCore.QSize(3*CELL_SIZE - 2*BORDER_W, 
                                            3*CELL_SIZE - 2*BORDER_W))
        self.smile.setGeometry(HORIZONTAL_PADDING + round(CELL_SIZE*(size + 0.5)) + BORDER_W*size, 
                               VERTICAL_PADDING + 10, 3*CELL_SIZE, 3*CELL_SIZE)
        self.smile.clicked.connect(lambda state, val = MainWindow: self.restart(val))
        self.smile.setStyleSheet(f"border :{BORDER_W}px solid;"
                                "border-top-color : #f0f0f0; "
                                "border-left-color :#f0f0f0;"
                                "border-right-color :gray;"
                                "border-bottom-color : gray;")

        self.mines_slider = QtWidgets.QSlider(self.centralwidget)
        self.mines_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.mines_slider.setRange(MIN_MINES_CNT, MAX_MINES_CNT)
        self.mines_slider.setValue(MINES_START_CNT)
        self.mines_slider.setFixedWidth(3*CELL_SIZE)
        self.mines_slider.move(HORIZONTAL_PADDING + round(CELL_SIZE*(size + 0.5)) + BORDER_W*size, 
                               VERTICAL_PADDING + 3*CELL_SIZE + 20)
        
        self.mines_label = QtWidgets.QLabel(self.centralwidget)
        self.mines_label.move(HORIZONTAL_PADDING + round(CELL_SIZE*(size + 0.5)) + BORDER_W*size, 
                              VERTICAL_PADDING + 3*CELL_SIZE + 40)
        self.mines_label.setText(f"Mines count: {self.field.mines_cnt}")
        self.mines_label.setFixedWidth(3*CELL_SIZE)

        self.mines_slider.valueChanged.connect(self.onchange_mines_slider)

        self.size_slider = QtWidgets.QSlider(self.centralwidget)
        self.size_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.size_slider.setRange(MIN_SIZE_CNT, MAX_SIZE_CNT)
        self.size_slider.setValue(SIZE_START_CNT)
        self.size_slider.setFixedWidth(3*CELL_SIZE)
        self.size_slider.move(HORIZONTAL_PADDING + round(CELL_SIZE*(size + 0.5)) + BORDER_W*size, 
                              VERTICAL_PADDING + 3*CELL_SIZE + 60)
        
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.move(HORIZONTAL_PADDING + round(CELL_SIZE*(size + 0.5)) + BORDER_W*size, 
                             VERTICAL_PADDING + 3*CELL_SIZE + 80)
        self.size_label.setText(f"Size: {self.field.size}")
        self.size_label.setFixedWidth(3*CELL_SIZE)

        self.size_slider.valueChanged.connect(self.onchange_size_slider)

        self.gridLayout = QtWidgets.QGridLayout(spacing = BORDER_W)
        self.gridLayout.setObjectName("gridLayout")

        self.widget.setLayout(self.gridLayout)

        self.cells: list[QtWidgets.QPushButton] = []
        for i in range(size**2):
            self.cells.append(QtWidgets.QPushButton(self.widget))
            self.cells[i].setObjectName(str(i))
            self.cells[i].setFixedSize(CELL_SIZE, CELL_SIZE)
            self.cells[i].setStyleSheet("background: #b5b5b5;"
                                        f"border :{BORDER_W}px solid;"
                                        "border-top-color : #f0f0f0; "
                                        "border-left-color :#f0f0f0;"
                                        "border-right-color :gray;"
                                        "border-bottom-color : gray;")
            self.gridLayout.addWidget(self.cells[i], i//size, i%size, 1, 1)
            self.cells[i].clicked.connect(lambda state, x = i: self.onclick_cell(x))
        
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setObjectName("check_btn")
        self.btn.setIcon(QtGui.QIcon("pictures\\shovel.png"))
        self.btn.setIconSize(QtCore.QSize(CELL_SIZE, CELL_SIZE))
        self.btn.setFixedSize(round(1.5*CELL_SIZE), round(1.5*CELL_SIZE))
        self.btn.setGeometry(HORIZONTAL_PADDING + round((size/2 - 0.75)*CELL_SIZE), 
                             round((size + 0.75)*CELL_SIZE + BORDER_W*(size - 1)), 
                             CELL_SIZE, CELL_SIZE)
        self.btn.clicked.connect(self.onclick_btn)
        self.btn.setStyleSheet("background: #b5b5b5;"
                                f"border :{BORDER_W}px solid;"
                                "border-top-color : #f0f0f0; "
                                "border-left-color :#f0f0f0;"
                                "border-right-color :gray;"
                                "border-bottom-color : gray;")
        
        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(SIZE_START_CNT, MINES_START_CNT)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
