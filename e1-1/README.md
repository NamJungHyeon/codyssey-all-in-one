[← 저장소 메인으로](../README.md)

# 🖥️ 개발 워크스테이션 구축

![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Docker](https://img.shields.io/badge/Docker%2029.4.2-2496ED?style=flat&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git%202.50.1-F05032?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)

> **코디세이 올인원 과정 — 개발 워크스테이션 미션**
터미널(CLI), Docker, Git/GitHub를 활용해 "내 컴퓨터에서만 돌아가는" 문제를 줄이는 **재현 가능한 개발 환경**을 구축하고, 모든 수행 과정을 명령어와 출력 결과로 증거화한 저장소입니다.
> 

---

## 📦 이 저장소의 다른 미션

이 문서는 **e1-1 개발 워크스테이션** 미션입니다. 같은 저장소의 다른 미션은 아래에서 확인할 수 있습니다.

| 미션 | 프로젝트 | 설명 |
| --- | --- | --- |
| e1-2 | [python-quiz-game](../e1-2/README.md) | Python 클래스(`Quiz`/`QuizGame`)와 JSON 파일 저장(`state.json`)으로 만든 터미널 퀴즈 게임. 주제: IT/컴퓨터 상식. 힌트·랜덤 출제·기록 히스토리 등 보너스 기능 포함 |
| e1-3 | [mini-npu-simulator](../e1-3/README.md) | MAC(Multiply-Accumulate) 연산을 반복문으로 직접 구현한 Mini NPU 시뮬레이터. 3×3 사용자 입력과 5×5/13×13/25×25 `data.json` 배치 분석, 허용오차(epsilon) 기반 동점 처리, 크기별 성능(O(N²)) 분석 포함 |

---

## 📂 문서 바로가기
 
| 문서 | 내용 |
|---|---|
| [01. 터미널 & 권한](md/01-terminal.md) | 터미널 기본 조작 로그, 파일/디렉토리 권한 변경 전후 비교 |
| [02. Docker 기본](md/02-doccker-basic.md) | 설치/데몬 점검, hello-world, ubuntu 실습, run vs exec 관찰, 운영 명령 |
| [03. 커스텀 이미지 & 네트워크/스토리지](md/03-custom-image.md) | Dockerfile, 빌드, 포트 매핑, 바인드 마운트, 볼륨 영속성 |
| [04. Git & GitHub](md/04-git-github.md) | Git 설정, GitHub 푸시, VSCode 연동 증거 |
| [05. 트러블슈팅](md/05-troubleshooting.md) | 실제 겪은 문제 3건 (문제→가설→확인→해결) |
| [06. 개념 정리](md/06-concepts.md) | 경로/권한/이미지vs컨테이너/포트/볼륨/Git vs GitHub |
| [07. 보너스 — Compose](md/07-bonus-compose.md) | Docker Compose 실습 |

## 📋 미션 개요

터미널로 작업 디렉토리와 권한을 정리하고, Dockerfile로 웹 서버를 컨테이너화한 뒤 포트 매핑 · 바인드 마운트 · 볼륨으로 접속, 변경 반영, 데이터 영속성을 직접 검증했다. 단순히 명령을 따라 치는 것이 아니라, 실행 결과(로그/접속/데이터 유지)로 이미지-컨테이너 분리, 격리된 실행 환경, 포트·스토리지 연결이라는 구조적 원칙을 확인하는 것이 목표다.

## ⚙️ 실행 환경

| 항목 | 내용 |
| --- | --- |
| OS | macOS <!-- sw_vers 버전 기입 --> |
| Shell / Terminal | zsh / macOS 기본 터미널 |
| Docker | 29.4.2 (Docker Desktop) |
| Git | 2.50.1 (Apple Git-155) |

## ✅ 수행 체크리스트

| 구분 | 항목 | 상태 | 상세 문서 |
| --- | --- | --- | --- |
| 터미널 | 기본 조작 (pwd/ls/cd/mkdir/touch/cat/cp/mv/rm) | ✅ | 01. 터미널 & 권한 |
| 터미널 | 권한 변경 실습 (파일/디렉토리 전후 비교) | ✅ | 01. 터미널 & 권한 |
| Docker | 설치/데몬 점검 (`--version`, `info`) | ✅ | 02. Docker 기본 |
| Docker | hello-world / ubuntu 컨테이너 실습 | ✅ | 02. Docker 기본 |
| Docker | 운영 명령 (`images`/`ps`/`logs`/`stats`) | ✅ | 02. Docker 기본 |
| Docker | Dockerfile 커스텀 이미지 빌드 | ✅ | 03. 커스텀 이미지 & 네트워크/스토리지 |
| Docker | 포트 매핑 접속 (8080/8081) | ✅ | 03. 커스텀 이미지 & 네트워크/스토리지 |
| Docker | 바인드 마운트 변경 반영 | ✅ | 03. 커스텀 이미지 & 네트워크/스토리지 |
| Docker | 볼륨 영속성 검증 | ✅ | 03. 커스텀 이미지 & 네트워크/스토리지 |
| Git | 설정 + VSCode GitHub 연동 | ✅ | 04. Git & GitHub |
| 보너스 | Docker Compose | ✅ | 07. 보너스 — Compose |

## 📁 저장소 구조

```
e1-1/
├── README.md                   # 메인 문서 (현재 파일)
├── dev-workstation/
│   ├── Dockerfile              # 커스텀 NGINX 이미지 정의
│   └── app/
│       └── index.html          # 정적 웹 콘텐츠
├── md/                         # 수행 로그 상세 문서
│   ├── 01-terminal.md          # 터미널 조작 + 권한 실습
│   ├── 02-doccker-basic.md     # Docker 점검 + 컨테이너 실습
│   ├── 03-custom-image.md      # 빌드/포트/마운트/볼륨
│   ├── 04-git-github.md        # Git 설정 + GitHub 연동
│   ├── 05-troubleshooting.md   # 트러블슈팅 모음
│   ├── 06-concepts.md          # 개념 정리
│   └── 07-bonus-compose.md     # 보너스 과제
└── screenshots/                # 접속/연동 증거 스크린샷
```

## 🔍 검증 방법 요약

| 검증 항목 | 사용 명령 | 증거 위치 |
| --- | --- | --- |
| Docker 데몬 동작 | `docker info` | 02 |
| 컨테이너 실행/종료·유지 | `docker run` / `ps` / `exec` | 02 |
| 이미지 빌드 | `docker build` / `images` | 03 |
| 포트 접속 | `curl` + 브라우저 | 03, screenshots/ |
| 마운트 반영 | 파일 수정 전/후 `curl` 비교 | 03 |
| 볼륨 영속성 | 컨테이너 삭제 전/후 `cat` | 03 |
| Git 설정 | `git config --list` | 04 |

## 🔧 트러블슈팅
 
실습 중 실제로 겪은 문제와 해결 과정: **[05. 트러블슈팅](md/05-troubleshooting.md)**
 
1. `docker info` 데몬 연결 실패 → Docker Desktop 미실행이 원인
2. `mkdir: File exists`로 권한 변경 전/후 비교 불가 → 기존 디렉토리 삭제 후 재실험
3. 빌드 성공·응답 200인데 빈 페이지 → 빈 index.html이 이미지에 스냅샷된 것이 원인
## 📚 개념 정리
 
경로 / 권한 / 이미지 vs 컨테이너 / 포트 매핑 / 볼륨 / Git vs GitHub: **[06. 개념 정리](md/06-concepts.md)**
 
## 🚀 재현 방법
 
```bash
git clone https://github.com/NamJungHyeon/codyssey-all-in-one.git
cd codyssey-all-in-one/e1-1/dev-workstation
docker build -t my-web:1.0 .
docker run -d -p 8080:80 --name web-8080 my-web:1.0
curl http://localhost:8080
```
