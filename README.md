# 개발 워크스테이션 구축 미션

> 터미널(CLI), Docker, Git/GitHub를 활용해 재현 가능한 개발 환경을 구축하고, 수행 과정을 증거와 함께 문서화한 저장소입니다.

## 1) 프로젝트 개요

<!-- 미션 목표 2~3문장으로 요약해서 작성 -->

## 2) 실행 환경

- OS: macOS <!-- ProductName:		macOS
ProductVersion:		26.5.1
BuildVersion:		25F80 -->
- Shell: zsh
- Terminal: macOS 기본 터미널
- Docker: 29.4.2 (Docker Desktop)
- Git: <!-- git version 2.50.1 -->

## 3) 수행 체크리스트

- [ ] 터미널 기본 조작 (pwd/ls/cd/mkdir/touch/cat/cp/mv/rm)
- [ ] 권한 변경 실습 (파일 1개 + 디렉토리 1개, 전/후 비교)
- [ ] Docker 설치/데몬 점검 (`docker --version`, `docker info`)
- [ ] hello-world 실행
- [ ] ubuntu 컨테이너 진입 및 내부 명령 실행
- [ ] 컨테이너 종료/유지(run·exit vs exec) 차이 관찰
- [ ] Docker 운영 명령 (`images`, `ps -a`, `logs`, `stats`)
- [ ] Dockerfile 작성 및 커스텀 이미지 빌드
- [ ] 포트 매핑 접속 확인 (2개 포트)
- [ ] 바인드 마운트 변경 반영 확인
- [ ] Docker 볼륨 영속성 검증 (컨테이너 삭제 전/후)
- [ ] Git 설정 (`git config --list`)
- [ ] VSCode GitHub 로그인 및 저장소 연동

## 4) 수행 로그

### 4-1. 터미널 기본 조작

```bash
<!-- $ pwd
/Users/junghyun
 -->
```

### 4-2. 권한 실습

파일 권한 변경 (644 → 600 → 644):

```
<!-- memo.txt chmod 전/후 로그 붙여넣기 -->
```

디렉토리 권한 변경 (755 → 700):

```
<!-- secret2 chmod 전/후 로그 붙여넣기 -->
```

### 4-3. Docker 설치 점검

```
<!-- docker --version 출력 붙여넣기 -->
```

```
<!-- docker info 발췌 (Client 요약 + Server 섹션) 붙여넣기 -->
```

### 4-4. 컨테이너 기본 실습

hello-world:

```
<!-- docker run hello-world 출력 붙여넣기 -->
```

ubuntu 진입 및 내부 명령:

```
<!-- docker run -it --name ubt ubuntu bash 및 내부 ls / echo / cat /etc/os-release 로그 붙여넣기 -->
```

컨테이너 종료/유지 관찰 (run·exit vs exec):

```
<!-- docker ps / ps -a / exec 진입·exit 후 ps 로그 붙여넣기 -->
```

관찰 정리:

<!-- run -it bash 후 exit하면 왜 종료되는지, exec 후 exit하면 왜 유지되는지 2~3문장 작성 -->

운영 명령:

```
<!-- docker images / docker logs / docker stats --no-stream 출력 붙여넣기 -->
```

### 4-5. 커스텀 이미지 빌드 (Dockerfile)

선택한 베이스: `nginx:alpine` (방식 A — 웹 서버 베이스 + 정적 콘텐츠 교체)

커스텀 포인트와 목적:

| 항목 | 목적 |
|---|---|
| `FROM nginx:alpine` | <!-- 작성 --> |
| `LABEL` | <!-- 작성 --> |
| `ENV APP_ENV=dev` | <!-- 작성 --> |
| `COPY app/ ...` | <!-- 작성 --> |
| `HEALTHCHECK` | <!-- 작성 --> |

빌드/실행:

```
<!-- docker build -t my-web:1.0 . 출력 붙여넣기 -->
```

```
<!-- docker images | grep my-web 출력 붙여넣기 -->
```

### 4-6. 포트 매핑

```
<!-- docker run -d -p 8080:80 ... / -p 8081:80 ... / curl 두 번 출력 붙여넣기 -->
```

브라우저 접속 증거 (주소창 포함):

![8080 접속](screenshots/port-8080.png)
![8081 접속](screenshots/port-8081.png)

포트 매핑이 필요한 이유:

<!-- 2~3문장 작성 -->

### 4-7. 바인드 마운트

```
<!-- 마운트 실행 명령 + 변경 전 curl + 파일 수정 + 변경 후 curl 로그 붙여넣기 -->
```

### 4-8. Docker 볼륨 영속성

```
<!-- volume create ~ 컨테이너 삭제 ~ 재생성 후 cat 로그 붙여넣기 -->
```

검증 결과:

<!-- 컨테이너를 삭제해도 데이터가 유지된 이유 1~2문장 작성 -->

### 4-9. Git 설정 및 GitHub 연동

```
<!-- git config --list 출력 붙여넣기 (토큰/비밀번호 없는지 확인) -->
```

VSCode GitHub 연동 증거:

![VSCode GitHub 연동](screenshots/vscode-github.png)

## 5) 검증 방법 요약

| 검증 항목 | 사용 명령 | 결과 위치 |
|---|---|---|
| Docker 데몬 동작 | `docker info` | 4-3 |
| 컨테이너 실행 | `docker run`, `docker ps` | 4-4 |
| 이미지 빌드 | `docker build`, `docker images` | 4-5 |
| 포트 접속 | `curl`, 브라우저 | 4-6, screenshots/ |
| 마운트 반영 | 파일 수정 후 `curl` 비교 | 4-7 |
| 볼륨 영속성 | 컨테이너 삭제 전/후 `cat` | 4-8 |
| Git 설정 | `git config --list` | 4-9 |

## 6) 트러블슈팅

### 사례 1: docker info 데몬 연결 실패

- 문제: `docker info` 실행 시 `failed to connect to the docker API ... check if the daemon is running`
- 원인 가설: <!-- 작성 -->
- 확인: <!-- 작성 -->
- 해결: <!-- 작성 -->

### 사례 2: <!-- 제목 작성 (예: mkdir File exists / nvm 경고 / 포트 충돌 등 실제 겪은 것) -->

- 문제: <!-- 작성 -->
- 원인 가설: <!-- 작성 -->
- 확인: <!-- 작성 -->
- 해결: <!-- 작성 -->

## 7) 개념 정리

### 절대 경로 vs 상대 경로

<!-- 작성 -->

### 파일 권한 (r/w/x, 755/644)

<!-- 작성 -->

### 이미지 vs 컨테이너, 커스텀 이미지

<!-- 작성 -->

### 포트 매핑이 필요한 이유

<!-- 작성 -->

### Docker 볼륨 (데이터 영속성)

<!-- 작성 -->

### Git vs GitHub

<!-- 작성 -->

## 8) 재현 방법

이 저장소를 클론한 뒤 아래 명령으로 동일한 결과를 재현할 수 있습니다.

```bash
git clone <저장소 URL>
cd dev-workstation
docker build -t my-web:1.0 .
docker run -d -p 8080:80 --name web-8080 my-web:1.0
curl http://localhost:8080
```
