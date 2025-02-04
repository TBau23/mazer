from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, x, y, window, walls={"left": True, "right": True, "up": True, "down": True},):
        self.upper_left_x = x
        self.upper_left_y = y
        self.lower_right_x = x + 25
        self.lower_right_y = y + 25
        self.walls = walls
        self._window = window

    def draw(self):
        if self.walls["left"]:
            line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.upper_left_x, self.lower_right_y))
            self._window.draw_line(line)
        if self.walls["right"]:
            line = Line(Point(self.lower_right_x, self.upper_left_y), Point(self.lower_right_x, self.lower_right_y))
            self._window.draw_line(line)
        if self.walls["up"]:
            line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.lower_right_x, self.upper_left_y))
            self._window.draw_line(line)
        if self.walls["down"]:
            line = Line(Point(self.upper_left_x, self.lower_right_y), Point(self.lower_right_x, self.lower_right_y))
            self._window.draw_line(line)

def main():
    win = Window(800, 600)
    l1 = Line(Point(100, 100), Point(500, 100))
    l2 = Line(Point(100,100), Point(500, 300))
    l3 = Line(Point(500,100), Point(500, 300))
    cells = []
    for i in range(10):
        row = []
        for j in range(7):
            row.append(Cell(j*25, i*25, win, walls={"left": True, "right": False, "up": True, "down": True}))
        cells.append(row)
    for row in cells:
        for cell in row:
            cell.draw()


    win.wait_for_close()
        
main()