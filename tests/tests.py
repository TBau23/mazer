import unittest
from src.main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 15
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m._cells), num_rows)
        self.assertEqual(len(m._cells[0]), num_cols)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 15
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(m._cells[0][0].top_wall, False)
        self.assertEqual(m._cells[num_rows - 1][num_cols - 1].bottom_wall, False)

    def test_maze_reset_cells_visited(self):
        m = Maze(0, 0, 10, 10, 10, 10)
        for row in m._cells:
            for cell in row:
                cell.visited = True
        m._reset_cells_visited()
        for row in m._cells:
            for cell in row:
                self.assertEqual(cell.visited, False)


if __name__ == "__main__":
    unittest.main()
