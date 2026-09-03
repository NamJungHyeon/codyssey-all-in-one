from grid import Grid


class ConsoleIO:
    """콘솔 입력을 검증하며 읽어들이는 담당."""

    @staticmethod
    def read_menu_choice(prompt, choices):
        while True:
            raw = input(prompt)
            text = raw.strip()
            if text in choices:
                return text
            print(f"⚠️ 잘못된 입력입니다. {'/'.join(sorted(choices))} 중 하나를 입력하세요.")

    @staticmethod
    def read_grid(n, label):
        while True:
            print(f"{label} ({n}줄 입력, 공백 구분)")
            rows = []
            ok = True
            for _ in range(n):
                tokens = input().strip().split()
                if len(tokens) != n:
                    print(f"⚠️ 입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    ok = False
                    break
                try:
                    rows.append([float(t) for t in tokens])
                except ValueError:
                    print(f"⚠️ 입력 형식 오류: 숫자로 변환할 수 없는 값이 있습니다. 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    ok = False
                    break
            if ok:
                print()
                return Grid.from_rows(rows)
            print()
