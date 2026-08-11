import os

from console_io import ConsoleIO
from modes import Mode1App, Mode2App

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def main():
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = ConsoleIO.read_menu_choice("선택: ", {"1", "2"})
    print()
    if choice == "1":
        Mode1App().run()
    else:
        Mode2App(DATA_FILE).run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
