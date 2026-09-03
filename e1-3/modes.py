from console_io import ConsoleIO
from judge import Judge
from mac_unit import MacUnit
from pattern_analyzer import PatternAnalyzer
from performance import PerformanceBenchmark

PERF_SIZES = [3, 5, 13, 25]


class Mode1App:
    """사용자 입력(3×3) 모드: 필터 A/B, 패턴 입력 → MAC 연산 → 판정 → 성능 분석."""

    def run(self):
        print("-" * 40)
        print("# [1] 필터 입력")
        print("-" * 40)
        filter_a = ConsoleIO.read_grid(3, "필터 A")
        filter_b = ConsoleIO.read_grid(3, "필터 B")
        print("✓ 필터 A, B 저장 완료")
        print()

        print("-" * 40)
        print("# [2] 패턴 입력")
        print("-" * 40)
        pattern = ConsoleIO.read_grid(3, "패턴")

        print("-" * 40)
        print("# [3] MAC 결과")
        print("-" * 40)
        score_a = MacUnit.compute(pattern, filter_a)
        score_b = MacUnit.compute(pattern, filter_b)
        verdict = Judge.decide("A", score_a, "B", score_b)
        avg_ms = PerformanceBenchmark.measure_avg_ms(
            lambda: (MacUnit.compute(pattern, filter_a), MacUnit.compute(pattern, filter_b))
        )

        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/{PerformanceBenchmark.REPEATS}회): {avg_ms:.3f} ms")
        if verdict == "UNDECIDED":
            print(f"판정: 판정 불가 (|A-B| < {Judge.EPSILON_DISPLAY})")
        else:
            print(f"판정: {verdict}")

        print()
        print("-" * 40)
        print("# [4] 성능 분석 (3×3)")
        print("-" * 40)
        print(f"크기: 3×3 | 평균 시간({PerformanceBenchmark.REPEATS}회): {avg_ms:.3f} ms | 연산 횟수: {3 * 3}")


class Mode2App:
    """data.json 분석 모드: 필터 로드 → 패턴 분석/판정 → 성능 분석 → 결과 요약."""

    def __init__(self, data_file):
        self.analyzer = PatternAnalyzer(data_file)

    def run(self):
        data = self.analyzer.load()
        if data is None:
            print("data.json을 불러오지 못해 분석을 진행할 수 없습니다.")
            return

        filters = data.get("filters", {})
        patterns = data.get("patterns", {})

        self._print_filter_load_status(filters)

        print()
        print("-" * 40)
        print("# [2] 패턴 분석 (라벨 정규화 적용)")
        print("-" * 40)

        results = []
        for case_id in sorted(patterns.keys(), key=self.analyzer.sort_key):
            case = patterns[case_id]
            result = self.analyzer.analyze(case_id, case, filters)
            self._print_case_result(case_id, result)
            results.append((case_id, result["passed"], result["reason"]))

        print()
        self._print_performance_table()

        print()
        self._print_summary(results)

    def _print_filter_load_status(self, filters):
        print("-" * 40)
        print("# [1] 필터 로드")
        print("-" * 40)
        for key in ("size_5", "size_13", "size_25"):
            filter_set = filters.get(key)
            if self.analyzer.has_filter_pair(filter_set):
                print(f"✓ {key} 필터 로드 완료 (Cross, X)")
            else:
                print(f"✗ {key} 필터 없음")

    @staticmethod
    def _print_case_result(case_id, result):
        print(f"--- {case_id} ---")
        if result["verdict"] is None:
            print(f"⚠ FAIL: {result['reason']}")
            return
        print(f"Cross 점수: {result['cross_score']}")
        print(f"X 점수: {result['x_score']}")
        status = "PASS" if result["passed"] else "FAIL"
        suffix = f" ({result['reason']})" if result["reason"] else ""
        expected_text = result["expected"] if result["expected"] else "알 수 없음"
        print(f"판정: {result['verdict']} | expected: {expected_text} | {status}{suffix}")

    @staticmethod
    def _print_performance_table():
        print("-" * 40)
        print("# [3] 성능 분석 (평균/10회)")
        print("-" * 40)
        print(f"{'크기':<10}{'평균 시간(ms)':<18}{'연산 횟수'}")
        print("-" * 40)
        for n, avg_ms in PerformanceBenchmark.benchmark_sizes(PERF_SIZES):
            print(f"{f'{n}×{n}':<10}{avg_ms:<18.4f}{n * n}")

    @staticmethod
    def _print_summary(results):
        print("-" * 40)
        print("# [4] 결과 요약")
        print("-" * 40)
        total = len(results)
        passed_count = sum(1 for _, p, _ in results if p)
        failed_count = total - passed_count
        print(f"총 테스트: {total}개")
        print(f"통과: {passed_count}개")
        print(f"실패: {failed_count}개")

        if failed_count:
            print("\n실패 케이스:")
            for case_id, passed, reason in results:
                if not passed:
                    print(f"- {case_id}: {reason}")
