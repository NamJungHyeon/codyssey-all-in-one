# 개발 워크스테이션 구축 미션

> 터미널(CLI), Docker, Git/GitHub를 활용해 재현 가능한 개발 환경을 구축하고, 수행 과정을 증거와 함께 문서화한 저장소입니다.

## 1) 프로젝트 개요

개발 환경 구축의 핵심 도구인 리눅스 CLI, Docker, Git/GitHub를 직접 다루며 "내 컴퓨터에서만 돌아가는" 문제를 줄이는 재현 가능한 실행 환경을 만드는 것이 목표다. 터미널로 작업 디렉토리와 권한을 정리하고, Dockerfile로 웹 서버를 컨테이너화한 뒤 포트 매핑·바인드 마운트·볼륨으로 접속, 변경 반영, 데이터 영속성을 직접 검증했다. 모든 수행 과정은 명령어와 출력 결과를 증거로 이 문서에 기록했다.

## 2) 실행 환경

- OS: macOS
ProductName:		macOS
ProductVersion:		26.5.1
BuildVersion:		25F80
- Shell: zsh
- Terminal: macOS 기본 터미널
- Docker: 29.4.2 (Docker Desktop)
- Git: git version 2.50.1

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
$ pwd
/Users/junghyun

$ mkdir -p ~/codyssey/practice
$ cd ~/codyssey/practice
$ ls -la
total 0
$ touch memo.txt
$ echo "hello codyssey" > memo.txt
$ cat memo.txt
hello codyssey
```

### 4-2. 권한 실습

파일 권한 변경 (644 → 600 → 644):

```
$ ls -l memo.txt
-rw-r--r--  1 junghyun  staff  15  7월 28 11:11 memo.txt    # 변경 전 644

$ chmod 600 memo.txt
$ ls -l memo.txt
-rw-------  1 junghyun  staff  15  7월 28 11:11 memo.txt    # 변경 후 600

$ chmod 644 memo.txt
$ ls -l memo.txt
-rw-r--r--  1 junghyun  staff  15  7월 28 11:11 memo.txt    # 644로 복원
```

디렉토리 권한 변경 (755 → 700):

```
$ mkdir secret2
$ ls -ld secret2
drwxr-xr-x  2 junghyun  staff  64  7월 28 11:36 secret2    # 변경 전 755 (rwxr-xr-x)

$ chmod 700 secret2
$ ls -ld secret2
drwx------  2 junghyun  staff  64  7월 28 11:36 secret2    # 변경 후 700 (rwx------)
```

### 4-3. Docker 설치 점검

```
$ docker --version
Docker version 29.4.2, build 055a478
```

```
$ docker info
Client:
 Version:    29.4.2
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
  compose: Docker Compose (Docker Inc.)
  ...(플러그인 목록 중략)...

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 2
 Server Version: 29.4.2
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Kernel Version: 6.12.76-linuxkit
 Operating System: Docker Desktop
 OSType: linux
 Architecture: aarch64
 CPUs: 10
 Total Memory: 7.75GiB
 Name: docker-desktop
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
```

### 4-4. 컨테이너 기본 실습

hello-world:

```
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
58dee6a49ef1: Pull complete
c3bdf82c34d1: Download complete
Digest: sha256:c3cbe1cc1aa588a64951ac6286e0df7b27fe2e6324b1001c619bb358770c0178
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

ubuntu 진입 및 내부 명령:

```
$ docker run -it --name ubt ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
693710ba2039: Pull complete
55237ac9880d: Pull complete
fdfb14aa961e: Download complete
Digest: sha256:3131b4cc82a783df6c9df078f86e01819a13594b865c2cad47bd1bca2b7063bb
Status: Downloaded newer image for ubuntu:latest

root@6004bd7d02ed:/# ls /
bin   dev  home  media  opt   root  sbin  sys  usr
boot  etc  lib   mnt    proc  run   srv   tmp  var

root@6004bd7d02ed:/# echo "inside container"
inside container

root@6004bd7d02ed:/# cat /etc/os-release
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo

root@6004bd7d02ed:/# exit
exit
```

컨테이너 종료/유지 관찰 (run·exit vs exec):

```
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                          PORTS     NAMES
6004bd7d02ed   ubuntu        "bash"     About a minute ago   Exited (0) 18 seconds ago                 ubt
6077e847ac7f   hello-world   "/hello"   About a minute ago   Exited (0) About a minute ago             beautiful_kirch

$ docker run -d --name ubt2 ubuntu sleep infinity
3e73abe7ad6442566f841a28e2ae9d44cd8dd735f9f5b230d651a966d81fd442

$ docker exec -it ubt2 bash
root@3e73abe7ad64:/# exit
exit

$ docker ps
CONTAINER ID   IMAGE     COMMAND            CREATED          STATUS          PORTS     NAMES
3e73abe7ad64   ubuntu    "sleep infinity"   13 seconds ago   Up 13 seconds             ubt2

$ docker logs ubt2
(출력 없음 — sleep infinity는 로그를 남기지 않음)

$ docker stats --no-stream
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT    MEM %     NET I/O         BLOCK I/O    PIDS
3e73abe7ad64   ubt2      0.00%     1.652MiB / 7.75GiB   0.02%     1.17kB / 126B   0B / 4.1kB   1

$ docker stop ubt2
ubt2
```

관찰 정리:

docker run -it ubuntu bash로 실행하면 bash가 컨테이너의 메인 프로세스(PID 1)가 되므로, exit로 bash를 종료하면 컨테이너 자체가 함께 종료된다. 반면 sleep infinity로 띄운 컨테이너에 docker exec로 진입하면 bash는 별도의 추가 프로세스로 실행되기 때문에, exit 해도 메인 프로세스인 sleep이 살아 있어 컨테이너는 Up 상태로 유지된다. 실제로 ubt는 exit 직후 docker ps -a에서 Exited(0)로, ubt2는 exec 종료 후에도 docker ps에서 Up으로 확인됐다.

운영 명령:

```
$ docker images
IMAGE                                      ID             DISK USAGE   CONTENT SIZE   EXTRA
aibe2_finalproject_compass_be-app:latest   f8e6ce4c74b8   903MB        346MB
hello-world:latest                         c3cbe1cc1aa5   22.6kB       10.3kB         U
redis:7-alpine                             bb186d083732   61.4MB       17.7MB
ubuntu:latest                              3131b4cc82a7   180MB        44.4MB         U
```

### 4-5. 커스텀 이미지 빌드 (Dockerfile)

선택한 베이스: `nginx:alpine` (방식 A — 웹 서버 베이스 + 정적 콘텐츠 교체)

커스텀 포인트와 목적:

| 항목 | 목적 |
|---|---|
| `FROM nginx:alpine` | 검증된 경량 웹 서버를 베이스로 재사용해 설치 과정 없이 서빙 환경 확보 |
| `LABEL` | 이미지 제목·관리자 메타데이터를 남겨 이미지 식별성 확보 |
| `ENV APP_ENV=dev` | 실행 환경 설정을 코드와 분리해 환경 변수로 주입 |
| `COPY app/ ...` | NGINX 기본 페이지를 직접 작성한 정적 콘텐츠로 교체 |
| `HEALTHCHECK` | 컨테이너가 실제로 응답 가능한 상태인지 주기적으로 자동 점검 |

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
