# 🗂️ Codyssey All-in-One

![Python](https://img.shields.io/badge/Python%203.11-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

> **코디세이 올인원 과정에서 수행한 미션들을 한 저장소에 모아둔 공간입니다.**
> 미션별로 폴더를 나눠 두었고, 각 폴더 안에 해당 미션의 README와 산출물이 들어 있습니다.

---

## 📚 미션 목록

| 미션 | 프로젝트 | 한 줄 소개 |
| --- | --- | --- |
| **[e1-1](e1-1/README.md)** | 개발 워크스테이션 구축 | 터미널(CLI)·Docker·Git/GitHub로 재현 가능한 개발 환경을 만들고, 모든 과정을 명령어와 출력으로 증거화 |
| **[e1-2](e1-2/README.md)** | 나만의 퀴즈 게임 | `Quiz`/`QuizGame` 클래스와 JSON 파일 저장으로 만든 터미널 퀴즈 게임 (주제: IT/컴퓨터 상식) |
| **[e1-3](e1-3/README.md)** | Mini NPU 시뮬레이터 | MAC(Multiply-Accumulate) 연산을 반복문으로 직접 구현한 패턴 판별 시뮬레이터 |

---

## 🔍 미션별 상세

### [e1-1 · 개발 워크스테이션 구축](e1-1/README.md)

터미널로 작업 디렉토리와 권한을 정리하고, Dockerfile로 웹 서버를 컨테이너화한 뒤 **포트 매핑 · 바인드 마운트 · 볼륨**으로 접속·변경 반영·데이터 영속성을 직접 검증했습니다. 트러블슈팅 3건과 개념 정리 문서를 함께 담았습니다.

`터미널` `권한` `Docker` `Dockerfile` `포트 매핑` `볼륨` `Git/GitHub` `Docker Compose(보너스)`

### [e1-2 · 나만의 퀴즈 게임](e1-2/README.md)

Python 기본 문법과 클래스, JSON 파일 입출력을 사용해 처음부터 끝까지 구현한 콘솔 퀴즈 게임입니다. 사용자가 추가한 퀴즈와 최고 점수는 `state.json`에 저장되어 재실행해도 유지됩니다. 힌트·랜덤 출제·문제 수 선택·삭제·기록 히스토리 등 보너스 기능을 포함합니다.

`클래스` `JSON 입출력` `상태 영속화` `콘솔 UI` `보너스 기능`

### [e1-3 · Mini NPU 시뮬레이터](e1-3/README.md)

외부 라이브러리 없이 표준 라이브러리만으로 MAC 연산을 구현해, 입력 패턴이 십자가(Cross)인지 X인지 판별합니다. 3×3 사용자 입력 모드와 `data.json` 배치 분석 모드(5×5/13×13/25×25)를 제공하며, 허용오차(epsilon) 기반 동점 처리와 크기별 O(N²) 성능 분석을 포함합니다. 역할별 클래스로 파일을 분리해 구성했습니다.

`MAC 연산` `라벨 정규화` `부동소수점/epsilon` `O(N²) 성능 분석` `클래스 분리 설계`

---

## 📁 저장소 구조

```
codyssey-all-in-one/
├── README.md          # 현재 문서 (미션 목록)
├── e1-1/              # 개발 워크스테이션 구축
│   ├── README.md
│   ├── dev-workstation/   # Dockerfile, 정적 웹 콘텐츠
│   ├── md/                # 수행 로그 상세 문서 (01~07)
│   └── screenshots/       # 접속/연동 증거 스크린샷
├── e1-2/              # 나만의 퀴즈 게임
│   ├── README.md
│   ├── main.py, quiz.py, quiz_game.py, data.py
│   └── docs/
├── e1-3/              # Mini NPU 시뮬레이터
│   ├── README.md
│   ├── main.py + 역할별 모듈 (grid, mac_unit, labels, judge 등)
│   ├── data.json
│   └── screenshots/       # 기능 검증 스크린샷
└── practice/          # 개인 연습용 메모
```

---

## 🚀 시작하기

```bash
git clone https://github.com/NamJungHyeon/codyssey-all-in-one.git
cd codyssey-all-in-one
```

각 미션의 실행 방법은 해당 폴더의 README를 참고하세요.

| 미션 | 실행 |
| --- | --- |
| e1-1 | `cd e1-1/dev-workstation && docker build -t my-web:1.0 .` |
| e1-2 | `cd e1-2 && python3 main.py` |
| e1-3 | `cd e1-3 && python3 main.py` |
