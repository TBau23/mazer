from tkinter import Tk, BOTH, Canvas
import time
import random

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
    def __init__(self, x, y, cell_size_x, cell_size_y, window=None):
        self.upper_left_x = x
        self.upper_left_y = y
        self.lower_right_x = x + cell_size_x
        self.lower_right_y = y + cell_size_y
        self.right_wall = True
        self.left_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self._window = window
        self.visited = False

    def draw(self):
        if self._window is None:
            return

        def color_wall(wall):
            return "black" if wall else "white"
        
        left_wall_line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.upper_left_x, self.lower_right_y))
        self._window.draw_line(left_wall_line, color_wall(self.left_wall))       

        right_wall_line = Line(Point(self.lower_right_x, self.upper_left_y), Point(self.lower_right_x, self.lower_right_y))
        self._window.draw_line(right_wall_line, color_wall(self.right_wall))
 
        top_wall_line = Line(Point(self.upper_left_x, self.upper_left_y), Point(self.lower_right_x, self.upper_left_y))
        self._window.draw_line(top_wall_line, color_wall(self.top_wall))

        bottom_wall_line = Line(Point(self.upper_left_x, self.lower_right_y), Point(self.lower_right_x, self.lower_right_y))
        self._window.draw_line(bottom_wall_line, color_wall(self.bottom_wall))


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
            win=None,
            seed=None
            ):
        self._x_origin = x_origin
        self._y_origin = y_origin
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = None if seed is None else random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

        # move cell size out of cell class and into maze class?
    
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                new_cell = Cell(j*self._cell_size_x + self._x_origin , i*self._cell_size_y + self._y_origin, self._cell_size_x, self._cell_size_y, self._win)
                row.append(new_cell)
                new_cell.draw()
                self._animate()
            self._cells.append(row)

        
    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.02)
    
    def _break_entrance_and_exit(self):
        if self._cells:
            self._cells[0][0].top_wall = False
            self._cells[0][0].draw()
            self._cells[self._num_rows-1][self._num_cols-1].bottom_wall = False
            self._cells[self._num_rows-1][self._num_cols-1].draw()
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_options = []
            # above
            if i > 0 and not self._cells[i - 1][j].visited:
                next_options.append((i - 1, j, 'top'))
            # below
            if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:
                next_options.append((i + 1, j, 'bottom'))
            # left
            if j > 0 and not self._cells[i][j - 1].visited:
                next_options.append((i, j - 1, 'left'))
            # right
            if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:
                next_options.append((i, j + 1, 'right'))
            
            if len(next_options) == 0:
                self._cells[i][j].draw()
                self._animate()
                return
            
            inverse_direction = {
                'top': 'bottom',
                'bottom': 'top',
                'left': 'right',
                'right': 'left'
            }
            choice = random.choice(next_options)
            setattr(self._cells[i][j], f'{choice[2]}_wall', False)
            setattr(self._cells[choice[0]][choice[1]], f'{inverse_direction[choice[2]]}_wall', False)
            self._break_walls_r(choice[0], choice[1])

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def solve_bfs(self):
        to_visit = [(0, 0)]
        path = { (0,0) : None}
        end_coords = (self._num_rows - 1, self._num_cols - 1)
        end_goal = self._cells[end_coords[0]][end_coords[1]]
        found_end = False
        while to_visit:
            curr_coords = to_visit.pop(0)
            curr_cell = self._cells[curr_coords[0]][curr_coords[1]]
            curr_cell.visited = True
            if curr_cell == end_goal:
                found_end = True
                break
            
            # above
            if not curr_cell.top_wall and curr_coords[0] > 0 and not self._cells[curr_coords[0] - 1][curr_coords[1]].visited:
                to_visit.append((curr_coords[0] - 1, curr_coords[1]))
                path[(curr_coords[0] - 1, curr_coords[1])] = curr_coords
                curr_cell.draw_move(self._cells[curr_coords[0] - 1][curr_coords[1]], True)
                self._animate()
            # below
            if not curr_cell.bottom_wall and curr_coords[0] < self._num_rows - 1 and not self._cells[curr_coords[0] + 1][curr_coords[1]].visited:
                to_visit.append((curr_coords[0] + 1, curr_coords[1]))
                path[(curr_coords[0] + 1, curr_coords[1])] = curr_coords
                curr_cell.draw_move(self._cells[curr_coords[0] + 1][curr_coords[1]], True)
                self._animate()
            # left
            if not curr_cell.left_wall and curr_coords[1] > 0 and not self._cells[curr_coords[0]][curr_coords[1] - 1].visited:
                to_visit.append((curr_coords[0], curr_coords[1] - 1))
                path[(curr_coords[0], curr_coords[1] - 1)] = curr_coords
                curr_cell.draw_move(self._cells[curr_coords[0]][curr_coords[1] - 1], True)
                self._animate()
            # right
            if not curr_cell.right_wall and curr_coords[1] < self._num_cols - 1 and not self._cells[curr_coords[0]][curr_coords[1] + 1].visited:
                to_visit.append((curr_coords[0], curr_coords[1] + 1))
                path[(curr_coords[0], curr_coords[1] + 1)] = curr_coords
                curr_cell.draw_move(self._cells[curr_coords[0]][curr_coords[1] + 1], True)
                self._animate()

        path_reversed = []
        curr_coords = end_coords
        while curr_coords:
            path_reversed.append(curr_coords)
            curr_coords = path[curr_coords]
        path_reversed.reverse()

        for i in range(1, len(path_reversed)):
            from_coords = path_reversed[i - 1]
            to_coords = path_reversed[i]
            self._cells[from_coords[0]][from_coords[1]].draw_move(self._cells[to_coords[0]][to_coords[1]])
            self._animate()
        

        return found_end

    def _solve_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

        end_goal = self._cells[self._num_rows - 1][self._num_cols - 1]
        if current == end_goal:
            return True
        
        next_options = []
        # above
        if not current.top_wall and i > 0 and not self._cells[i - 1][j].visited:
            next_options.append((i - 1, j, 'top'))
        # below
        if not current.bottom_wall and i < self._num_rows - 1 and not self._cells[i + 1][j].visited:
            next_options.append((i + 1, j, 'bottom'))
        # left
        if not current.left_wall and j > 0 and not self._cells[i][j - 1].visited:
            next_options.append((i, j - 1, 'left'))
        # right
        if not current.right_wall and j < self._num_cols - 1 and not self._cells[i][j + 1].visited:
            next_options.append((i, j + 1, 'right'))

        for n in next_options:
            next = self._cells[n[0]][n[1]]
            current.draw_move(next)
            self._animate()
            success = self._solve_r(n[0], n[1])
            if success:
                return True
            current.draw_move(next, True)
            self._animate()
                    
        return False

def main():
    win = Window(1000, 800)
    maze = Maze(200, 200, 10, 10, 30, 30, win)
    maze.solve()
    win.wait_for_close()
        
main()


# next steps
# a*, djikstras
# improve visuals
# 3d maze?
# time all different algos and compare for given maze
