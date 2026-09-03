import time

from mac_unit import MacUnit
from pattern_generator import PatternGenerator


class PerformanceBenchmark:
    """MAC 연산 시간을 반복 측정해 평균(ms)을 계산한다."""

    REPEATS = 10

    @classmethod
    def measure_avg_ms(cls, func, repeats=REPEATS):
        start = time.perf_counter()
        for _ in range(repeats):
            func()
        end = time.perf_counter()
        return (end - start) / repeats * 1000.0

    @classmethod
    def benchmark_sizes(cls, sizes):
        """크기별로 십자가 패턴을 자동 생성해 (크기, 평균 시간ms) 목록을 반환한다.

        연산 시간은 값의 내용이 아니라 크기(N)에만 좌우되므로,
        data.json에 해당 크기의 패턴이 있는지와 무관하게 항상 동일한 방식으로 측정한다.
        """
        results = []
        for n in sizes:
            pattern = PatternGenerator.cross(n)
            filt = PatternGenerator.cross(n)
            avg_ms = cls.measure_avg_ms(lambda p=pattern, f=filt: MacUnit.compute(p, f))
            results.append((n, avg_ms))
        return results
