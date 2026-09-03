class MacUnit:
    """입력 패턴과 필터를 위치별로 곱하고 누적하는 MAC(Multiply-Accumulate) 연산 담당."""

    @staticmethod
    def compute(pattern, filt):
        total = 0.0
        n = pattern.size()
        for r in range(n):
            for c in range(n):
                total += pattern.get(r, c) * filt.get(r, c)
        return total
