class Grid:
    """n×n 크기의 2차원 데이터를 저장하고, 좌표로 읽고 쓰는 자료구조."""

    def __init__(self, n, fill=0.0):
        self.n = n
        self._cells = [[fill] * n for _ in range(n)]

    @classmethod
    def from_rows(cls, rows):
        n = len(rows)
        grid = cls(n)
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                grid.set(r, c, value)
        return grid

    def get(self, row, col):
        return self._cells[row][col]

    def set(self, row, col, value):
        self._cells[row][col] = value

    def size(self):
        return self.n
