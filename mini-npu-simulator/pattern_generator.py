from grid import Grid


class PatternGenerator:
    """성능 측정 및 예시용으로 십자가(Cross)·X 패턴을 자동 생성한다."""

    @staticmethod
    def cross(n):
        grid = Grid(n)
        mid = n // 2
        for r in range(n):
            for c in range(n):
                if r == mid or c == mid:
                    grid.set(r, c, 1.0)
        return grid

    @staticmethod
    def x(n):
        grid = Grid(n)
        for r in range(n):
            for c in range(n):
                if r == c or r + c == n - 1:
                    grid.set(r, c, 1.0)
        return grid
