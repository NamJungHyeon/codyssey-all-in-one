import json
import os
import re
import time

EPSILON = 1e-9
EPSILON_DISPLAY = "1e-9"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
PERF_SIZES = [3, 5, 13, 25]
PERF_REPEATS = 10


# ---------- 데이터 구조: n×n 그리드 저장/조회 ----------
def make_grid(n, fill=0.0):
    return [[fill] * n for _ in range(n)]


def get_value(grid, row, col):
    return grid[row][col]


def set_value(grid, row, col, value):
    grid[row][col] = value


# ---------- 패턴 생성기 (성능 측정용 3×3 벤치마크 및 예시 생성에 사용) ----------
def generate_cross(n):
    grid = make_grid(n)
    mid = n // 2
    for r in range(n):
        for c in range(n):
            if r == mid or c == mid:
                set_value(grid, r, c, 1.0)
    return grid


def generate_x(n):
    grid = make_grid(n)
    for r in range(n):
        for c in range(n):
            if r == c or r + c == n - 1:
                set_value(grid, r, c, 1.0)
    return grid


# ---------- MAC(Multiply-Accumulate) 연산 ----------
def compute_mac(pattern, filt):
    total = 0.0
    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            total += get_value(pattern, r, c) * get_value(filt, r, c)
    return total


# ---------- 라벨 정규화 ----------
def normalize_label(raw):
    text = str(raw).strip().lower()
    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"
    return None


# ---------- 판정 (허용오차 기반 동점 처리) ----------
def decide(label_a, score_a, label_b, score_b, epsilon=EPSILON):
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    return label_a if score_a > score_b else label_b


# ---------- 시간 측정 ----------
def measure_avg_ms(func, repeats=PERF_REPEATS):
    start = time.perf_counter()
    for _ in range(repeats):
        func()
    end = time.perf_counter()
    return (end - start) / repeats * 1000.0


# ---------- 공통 입력 처리 ----------
def read_menu_choice(prompt, choices):
    while True:
        raw = input(prompt)
        text = raw.strip()
        if text in choices:
            return text
        print(f"⚠️ 잘못된 입력입니다. {'/'.join(sorted(choices))} 중 하나를 입력하세요.")


def read_grid(n, label):
    while True:
        print(f"{label} ({n}줄 입력, 공백 구분)")
        grid = make_grid(n)
        ok = True
        for r in range(n):
            tokens = input().strip().split()
            if len(tokens) != n:
                print(f"⚠️ 입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                ok = False
                break
            try:
                values = [float(t) for t in tokens]
            except ValueError:
                print(f"⚠️ 입력 형식 오류: 숫자로 변환할 수 없는 값이 있습니다. 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                ok = False
                break
            for c, v in enumerate(values):
                set_value(grid, r, c, v)
        if ok:
            print()
            return grid
        print()


# ---------- 모드 1: 사용자 입력 (3×3) ----------
def run_mode1():
    print("-" * 40)
    print("# [1] 필터 입력")
    print("-" * 40)
    filter_a = read_grid(3, "필터 A")
    filter_b = read_grid(3, "필터 B")

    print("-" * 40)
    print("# [2] 패턴 입력")
    print("-" * 40)
    pattern = read_grid(3, "패턴")

    print("-" * 40)
    print("# [3] MAC 결과")
    print("-" * 40)
    score_a = compute_mac(pattern, filter_a)
    score_b = compute_mac(pattern, filter_b)
    verdict = decide("A", score_a, "B", score_b)
    avg_ms = measure_avg_ms(lambda: (compute_mac(pattern, filter_a), compute_mac(pattern, filter_b)))

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{PERF_REPEATS}회): {avg_ms:.3f} ms")
    if verdict == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON_DISPLAY})")
    else:
        print(f"판정: {verdict}")

    print()
    print("-" * 40)
    print("# [4] 성능 분석 (3×3)")
    print("-" * 40)
    print(f"크기: 3×3 | 평균 시간(10회): {avg_ms:.3f} ms | 연산 횟수: {3 * 3}")


# ---------- 모드 2: data.json 분석 ----------
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ {DATA_FILE} 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError as error:
        print(f"⚠️ data.json 파일이 손상되었습니다: {error}")
        return None


def natural_sort_key(key):
    parts = [int(p) for p in re.findall(r"\d+", key)]
    return parts if parts else [key]


def get_benchmark_pair(n, filters, patterns):
    key = f"size_{n}"
    filt = filters[key]["cross"] if key in filters and "cross" in filters[key] else generate_cross(n)
    for pattern_id in sorted(patterns.keys(), key=natural_sort_key):
        if pattern_id.startswith(f"size_{n}_"):
            return filt, patterns[pattern_id]["input"]
    return filt, generate_cross(n)


def analyze_pattern(case_id, case, filters):
    match = re.match(r"size_(\d+)_", case_id)
    if not match:
        return None, False, "케이스 이름에서 크기(N)를 추출할 수 없음"

    n = int(match.group(1))
    filter_key = f"size_{n}"
    filt_set = filters.get(filter_key)
    if filt_set is None:
        return None, False, f"{filter_key} 필터를 찾을 수 없음"

    pattern_input = case.get("input")
    if pattern_input is None or len(pattern_input) != n or any(len(row) != n for row in pattern_input):
        return None, False, f"패턴 크기가 {filter_key}(과)와 일치하지 않음"

    cross_filter = filt_set.get("cross")
    x_filter = filt_set.get("x")
    if cross_filter is None or x_filter is None:
        return None, False, f"{filter_key}에 cross/x 필터가 모두 존재하지 않음"

    cross_score = compute_mac(pattern_input, cross_filter)
    x_score = compute_mac(pattern_input, x_filter)
    verdict = decide("Cross", cross_score, "X", x_score)

    expected_label = normalize_label(case.get("expected"))
    if expected_label is None:
        return (verdict, cross_score, x_score), False, f"expected 값 '{case.get('expected')}'을(를) 정규화할 수 없음"

    passed = verdict == expected_label
    if passed:
        reason = None
    elif verdict == "UNDECIDED":
        reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    else:
        reason = f"판정({verdict})이 expected({expected_label})와 다름"

    return (verdict, cross_score, x_score, expected_label), passed, reason


def run_mode2():
    data = load_data()
    if data is None:
        print("data.json을 불러오지 못해 분석을 진행할 수 없습니다.")
        return

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    print("-" * 40)
    print("# [1] 필터 로드")
    print("-" * 40)
    for key in ("size_5", "size_13", "size_25"):
        if key in filters:
            print(f"✓ {key} 필터 로드 완료 (Cross, X)")
        else:
            print(f"✗ {key} 필터 없음")

    print()
    print("-" * 40)
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("-" * 40)

    results = []
    for case_id in sorted(patterns.keys(), key=natural_sort_key):
        case = patterns[case_id]
        detail, passed, reason = analyze_pattern(case_id, case, filters)
        print(f"--- {case_id} ---")
        if detail is None:
            print(f"⚠ FAIL: {reason}")
        elif len(detail) == 3:
            verdict, cross_score, x_score = detail
            print(f"Cross 점수: {cross_score}")
            print(f"X 점수: {x_score}")
            print(f"판정: {verdict} | expected: 알 수 없음 | FAIL ({reason})")
        else:
            verdict, cross_score, x_score, expected_label = detail
            print(f"Cross 점수: {cross_score}")
            print(f"X 점수: {x_score}")
            status = "PASS" if passed else "FAIL"
            suffix = f" ({reason})" if reason else ""
            print(f"판정: {verdict} | expected: {expected_label} | {status}{suffix}")
        results.append((case_id, passed, reason))

    print()
    print("-" * 40)
    print("# [3] 성능 분석 (평균/10회)")
    print("-" * 40)
    print(f"{'크기':<10}{'평균 시간(ms)':<18}{'연산 횟수'}")
    print("-" * 40)
    for n in PERF_SIZES:
        filt, patt = get_benchmark_pair(n, filters, patterns)
        avg_ms = measure_avg_ms(lambda filt=filt, patt=patt: compute_mac(patt, filt))
        label = f"{n}×{n}"
        print(f"{label:<10}{avg_ms:<18.4f}{n * n}")

    print()
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


def main():
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = read_menu_choice("선택: ", {"1", "2"})
    print()
    if choice == "1":
        run_mode1()
    else:
        run_mode2()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
