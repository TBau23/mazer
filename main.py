from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        # double underscore to mangle 
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, x, y, cell_size_x, cell_size_y, window):
        self.upper_left_x = x
        self.upper_left_y = y
        self.lower_right_x = x + cell_size_x
        self.lower_right_y = y + cell_size_y
        self.right_wall = True
        self.left_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self._window = window

    def draw(self):
        print('DRAWING CELL', self.upper_left_x, self.upper_left_y, self.lower_right_x, self.lower_right_y)
        if self.left_wall:
            line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.upper_left_x, self.lower_right_y))
            self._window.draw_line(line)
        if self.right_wall:
            line = Line(Point(self.lower_right_x, self.upper_left_y), Point(self.lower_right_x, self.lower_right_y))
            self._window.draw_line(line)
        if self.top_wall:
            line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.lower_right_x, self.upper_left_y))
            self._window.draw_line(line)
        if self.bottom_wall:
            line = Line(Point(self.upper_left_x, self.lower_right_y), Point(self.lower_right_x, self.lower_right_y))
            self._window.draw_line(line)
    def draw_move(self, to_cell, undo=False):
        x_from_cell = (self.upper_left_x + self.lower_right_x) / 2
        y_from_cell = (self.upper_left_y + self.lower_right_y) / 2
        x_to_cell = (to_cell.upper_left_x + to_cell.lower_right_x) / 2
        y_to_cell = (to_cell.upper_left_y + to_cell.lower_right_y) / 2
        color = "gray" if undo else "red"
        line = Line(Point(x_from_cell, y_from_cell), Point(x_to_cell, y_to_cell))
        self._window.draw_line(line, color)

class Maze:
    def __init__(
            self,
            x_origin,
            y_origin,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed=None
            ):
        self._x_origin = x_origin
        self._y_origin = y_origin
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        self._create_cells()

        # move cell size out of cell class and into maze class
    
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                row.append(Cell(j*self._cell_size_x + self._x_origin , i*self._cell_size_y + self._y_origin, self._cell_size_x, self._cell_size_y, self._win))
            self._cells.append(row)
        for row in self._cells:
            for cell in row:
                cell.draw()
        
    
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
        
        
def main():
    win = Window(800, 600)
    l1 = Line(Point(0, 100), Point(100, 100))
    l2 = Line(Point(100, 0 ), Point(100, 100))

    maze = Maze(100, 100, 10, 7, 25, 25, win)

    maze._cells[0][0].draw_move(maze._cells[4][2])
    win.draw_line(l1, fill_color="red")
    win.draw_line(l2, fill_color="red")



    win.wait_for_close()
        
main()