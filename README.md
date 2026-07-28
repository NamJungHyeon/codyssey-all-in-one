# 개발 워크스테이션 구축 미션

> 터미널(CLI), Docker, Git/GitHub를 활용해 재현 가능한 개발 환경을 구축하고, 수행 과정을 증거와 함께 문서화한 저장소입니다.
> 

## 1) 프로젝트 개요

개발 환경 구축의 핵심 도구인 리눅스 CLI, Docker, Git/GitHub를 직접 다루며 "내 컴퓨터에서만 돌아가는" 문제를 줄이는 재현 가능한 실행 환경을 만드는 것이 목표다. 터미널로 작업 디렉토리와 권한을 정리하고, Dockerfile로 웹 서버를 컨테이너화한 뒤 포트 매핑·바인드 마운트·볼륨으로 접속, 변경 반영, 데이터 영속성을 직접 검증했다. 모든 수행 과정은 명령어와 출력 결과를 증거로 이 문서에 기록했다.

## 2) 실행 환경

- OS: macOS
- Shell: terminal
- Terminal: macOS 기본 터미널
- Docker: 29.4.2 (Docker Desktop)
- Git: git version 2.50.1

## 3) 수행 체크리스트

- [ ]  터미널 기본 조작 (pwd/ls/cd/mkdir/touch/cat/cp/mv/rm)
- [ ]  권한 변경 실습 (파일 1개 + 디렉토리 1개, 전/후 비교)
- [ ]  Docker 설치/데몬 점검 (`docker --version`, `docker info`)
- [ ]  hello-world 실행
- [ ]  ubuntu 컨테이너 진입 및 내부 명령 실행
- [ ]  컨테이너 종료/유지(run·exit vs exec) 차이 관찰
- [ ]  Docker 운영 명령 (`images`, `ps -a`, `logs`, `stats`)
- [ ]  Dockerfile 작성 및 커스텀 이미지 빌드
- [ ]  포트 매핑 접속 확인 (2개 포트)
- [ ]  바인드 마운트 변경 반영 확인
- [ ]  Docker 볼륨 영속성 검증 (컨테이너 삭제 전/후)
- [ ]  Git 설정 (`git config --list`)
- [ ]  VSCode GitHub 로그인 및 저장소 연동

## 4) 수행 로그

### 4-1. 터미널 기본 조작

```bash
nam94903505@c5r4s5 ~ % pwd
/Users/nam94903505
nam94903505@c5r4s5 ~ % mkdir -p ~/codyssey/practice
nam94903505@c5r4s5 ~ % cd ~/codyssey/practice
nam94903505@c5r4s5 practice % ls -la
total 0
drwxr-xr-x  2 nam94903505  nam94903505  64 Jul 28 15:26 .
drwxr-xr-x  3 nam94903505  nam94903505  96 Jul 28 15:26 ..
nam94903505@c5r4s5 practice % touch memo.txt
nam94903505@c5r4s5 practice % echo "hello codyssey" > memo.txt
nam94903505@c5r4s5 practice % cat memo.txt
hello codyssey
```

### 4-2. 권한 실습

파일 권한 변경 (644 → 600 → 644):

```
nam94903505@c5r4s5 practice % ls -l memo.txt
-rw-r--r--  1 nam94903505  nam94903505  15 Jul 28 15:27 memo.txt

nam94903505@c5r4s5 practice % chmod 600 memo.txt
nam94903505@c5r4s5 practice % ls -l memo.txt
-rw-------  1 nam94903505  nam94903505  15 Jul 28 15:27 memo.txt

nam94903505@c5r4s5 practice % chmod 644 memo.txt
nam94903505@c5r4s5 practice % ls -l memo.txt
-rw-r--r--  1 nam94903505  nam94903505  15 Jul 28 15:27 memo.txt
```

디렉토리 권한 변경 (755 → 700):

```
nam94903505@c5r4s5 practice % mkdir secret
nam94903505@c5r4s5 practice % ls -ld secret
drwxr-xr-x  2 nam94903505  nam94903505  64 Jul 28 15:31 secret

nam94903505@c5r4s5 practice % chmod 700 secret
nam94903505@c5r4s5 practice % ls -ld secret
drwx------  2 nam94903505  nam94903505  64 Jul 28 15:31 secret
```

### 4-3. Docker 설치 점검

```
nam94903505@c5r4s5 ~ % docker --version
Docker version 28.5.2, build ecc6942
```

```
$nam94903505@c5r4s5 ~ % docker info
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /Users/nam94903505/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /Users/nam94903505/.docker/cli-plugins/docker-compose

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 28.5.2
 Storage Driver: overlay2
  Backing Filesystem: btrfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 1c4457e00facac03ce1d75f7b6777a7a851e5c41
 runc version: d842d7719497cc3b774fd71620278ac9e17710e0
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
 Operating System: OrbStack
 OSType: linux
 Architecture: x86_64
 CPUs: 6
 Total Memory: 15.67GiB
 Name: orbstack
 ID: 1016f4bf-cc28-4168-a868-90b818c9132a
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
 Default Address Pools:
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set
```

### 4-4. 컨테이너 기본 실습

hello-world:

```
nam94903505@c5r4s5 practice % docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:c3cbe1cc1aa588a64951ac6286e0df7b27fe2e6324b1001c619bb358770c0178
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 <https://hub.docker.com/>

For more examples and ideas, visit:
 <https://docs.docker.com/get-started/>
```

ubuntu 진입 및 내부 명령:

```
nam94903505@c5r4s5 practice % docker run -it --name ubuntu bash
Unable to find image 'bash:latest' locally
latest: Pulling from library/bash
55afa1ecc21d: Pull complete
3aa13943dde2: Pull complete
67a7137023b6: Pull complete
Digest: sha256:a19c811ee9e97fa8a080001d82b8e0ded303f0795cffdb1cbd162731bc8ce208
Status: Downloaded newer image for bash:latest

bash-5.3# ls /
bin    etc    lib    mnt    proc   run    srv    tmp    var
dev    home   media  opt    root   sbin   sys    usr

bash-5.3# echo "inside container"
inside container

bash-5.3# cat /etc/os-release
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.24.1
PRETTY_NAME="Alpine Linux v3.24"
HOME_URL="<https://alpinelinux.org/>"
BUG_REPORT_URL="<https://gitlab.alpinelinux.org/alpine/aports/-/issues>"

bash-5.3# exit
exit
```

컨테이너 종료/유지 관찰 (run·exit vs exec):

```
nam94903505@c5r4s5 practice % docker images
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
bash          latest    bc60f054756d   6 weeks ago    15.6MB
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB

nam94903505@c5r4s5 practice % docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

nam94903505@c5r4s5 practice % docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS                          PORTS     NAMES
cacbfe723a5d   bash          "docker-entrypoint.s…"   2 minutes ago   Exited (0) About a minute ago             ubuntu
ea59025312ef   hello-world   "/hello"                 4 minutes ago   Exited (0) 4 minutes ago                  jolly_stonebraker

nam94903505@c5r4s5 practice % docker run -d --name ubt2 ubuntu sleep infinity
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
ed819469700f: Pull complete
a3679419df18: Pull complete
Digest: sha256:3131b4cc82a783df6c9df078f86e01819a13594b865c2cad47bd1bca2b7063bb
Status: Downloaded newer image for ubuntu:latest
06c9300be44d1622bd87ac4a8bfd5e245f9e8f41fed2bc9e6c96a9b14eb94412

nam94903505@c5r4s5 practice % docker exec -it ubt2 bash
root@06c9300be44d:/# exit
exit

nam94903505@c5r4s5 practice % docker ps
CONTAINER ID   IMAGE     COMMAND            CREATED          STATUS          PORTS     NAMES
06c9300be44d   ubuntu    "sleep infinity"   33 seconds ago   Up 33 seconds             ubt2

nam94903505@c5r4s5 practice % docker logs ubt22
Error response from daemon: No such container: ubt22

nam94903505@c5r4s5 practice % docker stats --no-stream
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT    MEM %     NET I/O         BLOCK I/O        PIDS
06c9300be44d   ubt2      0.00%     2.41MiB / 15.67GiB   0.02%     1.13kB / 126B   13.9MB / 4.1kB   1

nam94903505@c5r4s5 practice % docker stop ubt2
ubt2
```

관찰 정리:

docker run -it ubuntu bash로 실행하면 bash가 컨테이너의 메인 프로세스(PID 1)가 되므로, exit로 bash를 종료하면 컨테이너 자체가 함께 종료된다. 반면 sleep infinity로 띄운 컨테이너에 docker exec로 진입하면 bash는 별도의 추가 프로세스로 실행되기 때문에, exit 해도 메인 프로세스인 sleep이 살아 있어 컨테이너는 Up 상태로 유지된다. 실제로 ubt는 exit 직후 docker ps -a에서 Exited(0)로, ubt2는 exec 종료 후에도 docker ps에서 Up으로 확인됐다.

운영 명령:

```
nam94903505@c5r4s5 practice % docker images
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
bash          latest    bc60f054756d   6 weeks ago    15.6MB
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB<img width="1059" height="487" alt="Screenshot 2026-07-28 at 4 51 28 PM" src="<https://github.com/user-attachments/assets/9460a749-e8e9-4e2e-81a6-d7604c436d6b>" />
```

### 4-5. 커스텀 이미지 빌드 (Dockerfile)

선택한 베이스: `nginx:alpine` (방식 A — 웹 서버 베이스 + 정적 콘텐츠 교체)

커스텀 포인트와 목적:

| 항목 | 목적 |
| --- | --- |
| `FROM nginx:alpine` | 검증된 경량 웹 서버를 베이스로 재사용해 설치 과정 없이 서빙 환경 확보 |
| `LABEL` | 이미지 제목·관리자 메타데이터를 남겨 이미지 식별성 확보 |
| `ENV APP_ENV=dev` | 실행 환경 설정을 코드와 분리해 환경 변수로 주입 |
| `COPY app/ ...` | NGINX 기본 페이지를 직접 작성한 정적 콘텐츠로 교체 |
| `HEALTHCHECK` | 컨테이너가 실제로 응답 가능한 상태인지 주기적으로 자동 점검 |

빌드/실행:

```
nam94903505@c5r4s5 dev-workstation % docker build -t my-web:1.0 .
[+] Building 6.8s (7/7) FINISHED                                                        docker:orbstack
 => [internal] load build definition from Dockerfile                                               0.2s
 => => transferring dockerfile: 292B                                                               0.0s
 => [internal] load metadata for docker.io/library/nginx:alpine                                    2.5s
 => [internal] load .dockerignore                                                                  0.2s
 => => transferring context: 2B                                                                    0.0s
 => [internal] load build context                                                                  0.2s
 => => transferring context: 389B                                                                  0.0s
 => [1/2] FROM docker.io/library/nginx:alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c  3.1s
 => => resolve docker.io/library/nginx:alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c  0.2s
 => => sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752 10.33kB / 10.33kB   0.0s
 => => sha256:1d40e3eb3bf4f138de1d67193f2aa5309fcaf343eb5ffadbf5e9439de1eb1ebb 2.50kB / 2.50kB     0.0s
 => => sha256:f0ba77f796e57c6fa89ae7f4fdad1665d6fcbd8e3f211535120542b337f9959e 12.32kB / 12.32kB   0.0s
 => => sha256:1223f016b4e4a2c21f7c49d4837fbfd47a9da6436b511690ca1e582fc2810d59 627B / 627B         0.5s
 => => sha256:62bec68d7c31c4c8a19d812d84da5f7748e54690c037979945b6c5b6c924b142 957B / 957B         0.7s
 => => sha256:3cd534fe98c64d68a1f4f1c83abb8d5cba7ecfd7be88e592389929d12e6253da 1.89MB / 1.89MB     0.3s
 => => extracting sha256:3cd534fe98c64d68a1f4f1c83abb8d5cba7ecfd7be88e592389929d12e6253da          0.1s
 => => sha256:46f977ee452f4399c208714afa034868d6056864f8a0cf3c643ab143dd802c80 404B / 404B         0.7s
 => => sha256:d0008c891db48b5f526d914bce9e8d889fe1a9d1f08291ae03fe97f871726f38 1.21kB / 1.21kB     0.8s
 => => extracting sha256:1223f016b4e4a2c21f7c49d4837fbfd47a9da6436b511690ca1e582fc2810d59          0.0s
 => => extracting sha256:62bec68d7c31c4c8a19d812d84da5f7748e54690c037979945b6c5b6c924b142          0.0s
 => => sha256:390dc935348d8070e695fbaae2a4bb114fb9e69c59f628e7576036ee9d5244c9 1.40kB / 1.40kB     1.0s
 => => extracting sha256:46f977ee452f4399c208714afa034868d6056864f8a0cf3c643ab143dd802c80          0.0s
 => => sha256:46519e7231d2eb5604df229beb44d59719a489eaa7aca52982535a010b07a9ed 20.31MB / 20.31MB   1.5s
 => => extracting sha256:d0008c891db48b5f526d914bce9e8d889fe1a9d1f08291ae03fe97f871726f38          0.0s
 => => extracting sha256:390dc935348d8070e695fbaae2a4bb114fb9e69c59f628e7576036ee9d5244c9          0.0s
 => => extracting sha256:46519e7231d2eb5604df229beb44d59719a489eaa7aca52982535a010b07a9ed          0.4s
 => [2/2] COPY app/ /usr/share/nginx/html/                                                         0.2s
 => exporting to image                                                                             0.2s
 => => exporting layers                                                                            0.1s
 => => writing image sha256:1729ef88194a2b5cc9eb7898fa6b370d4dd29322401bc5f931e08467b399e780       0.0s
 => => naming to docker.io/library/my-web:1.0
```

```
nam94903505@c5r4s5 dev-workstation % docker images
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
my-web        1.0       1729ef88194a   15 seconds ago   62.4MB
ubuntu        latest    de7345b16e94   2 weeks ago      100MB
bash          latest    bc60f054756d   6 weeks ago      15.6MB
hello-world   latest    e2ac70e7319a   4 months ago     10.1kB
```

### 4-6. 포트 매핑

```
nam94903505@c5r4s5 dev-workstation % docker run -d -p 8080:80 --name web-8080 my-web:1.0
docker run -d -p 8081:80 --name web-8081 my-web:1.0
docker ps
90bcc474d1b089e8f2b1708c49853b3047d4741e1c0349ab76495a195c00bb54
00d147e009f43ec5e84a56cd3b519cb23eb65097f2a029ec087b008c13d64b07
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS                                     PORTS                                     NAMES
00d147e009f4   my-web:1.0   "/docker-entrypoint.…"   1 second ago   Up Less than a second (health: starting)   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   web-8081
90bcc474d1b0   my-web:1.0   "/docker-entrypoint.…"   1 second ago   Up Less than a second (health: starting)   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   web-8080
```

브라우저 접속 증거 (주소창 포함):

!8080 접속

!8081 접속

포트 매핑이 필요한 이유:

컨테이너는 호스트와 격리된 자체 네트워크 공간을 가지므로, 컨테이너 내부의 80 포트는 기본적으로 호스트에서 접근할 수 없다. -p <호스트포트>:<컨테이너포트>로 두 포트를 연결해야 외부에서 접속이 가능하다. 같은 이미지를 8080, 8081 두 포트로 동시에 실행해도 충돌 없이 각각 접속되는 것으로 격리와 재현성을 확인했다.

### 4-7. 바인드 마운트

```
nam94903505@c5r4s5 dev-workstation % docker rm -f web-8080
docker run -d -p 8080:80 --name web-bind \
  -v "$(pwd)/app:/usr/share/nginx/html" my-web:1.0
web-8080
d51a0e0bbd49c90fb2666c4de67edb6edd48752c655f98fc546edb397b99e7c4
nam94903505@c5r4s5 dev-workstation % curl <http://localhost:8080>
<!DOCTYPE html>
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codyssey</title>
</head>
<body>
    <h1>개발 워크스테이션 미션 - 남정현</h1>
    <p>Docker 커스텀 NGINX 이미지에서 서빙 중</p>
</body>
</html>%                                                                                                nam94903505@c5r4s5 dev-workstation % echo "<p>bind mount 수정 반영 테스트</p>" >> app/index.html
nam94903505@c5r4s5 dev-workstation % curl <http://localhost:8080>
<!DOCTYPE html>
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codyssey</title>
</head>
<body>
    <h1>개발 워크스테이션 미션 - 남정현</h1>
    <p>Docker 커스텀 NGINX 이미지에서 서빙 중</p>
</body>
</html><p>bind mount 수정 반영 테스트</p>
```

### 4-8. Docker 볼륨 영속성

```
nam94903505@c5r4s5 dev-workstation % docker volume create mydata
mydata
nam94903505@c5r4s5 dev-workstation % docker volume ls
DRIVER    VOLUME NAME
local     mydata
nam94903505@c5r4s5 dev-workstation % docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity

bba26d65e01e6a54a64342f0baa696f4f263996548f564da66d038d7acf5c7d1
nam94903505@c5r4s5 dev-workstation % docker exec vol-test bash -c "echo persist-test > /data/hello.txt && cat /data/hello.txt"
persist-test
nam94903505@c5r4s5 dev-workstation % docker rm -f vol-test
vol-test
nam94903505@c5r4s5 dev-workstation % docker ps -a | grep vol-test
nam94903505@c5r4s5 dev-workstation % docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
b5654eca24d7fa8b23d60022ec76ecaf4c801f03e5cfb0988209f553240e241c
nam94903505@c5r4s5 dev-workstation % docker exec vol-test2 cat /data/hello.txt
persist-test
nam94903505@c5r4s5 dev-workstation % docker rm -f vol-test2
vol-test2
```

검증 결과:

컨테이너의 쓰기 레이어는 컨테이너 삭제와 함께 사라지지만, 볼륨은 Docker가 컨테이너와 독립적으로 관리하는 저장 공간이므로 데이터가 유지된다. 실제로 컨테이너를 삭제하고 새 컨테이너에 같은 볼륨을 연결했을 때 이전에 기록한 파일이 그대로 남아 있음을 확인했다.

### 4-9. Git 설정 및 GitHub 연동

```
nam94903505@c5r4s5 dev-workstation % git config --global user.name "남정현"
nam94903505@c5r4s5 dev-workstation % git config --global user.email "nam9490@gmail.com"
nam94903505@c5r4s5 dev-workstation % git config --global init.defaultBranch main
nam94903505@c5r4s5 dev-workstation % git config --list
credential.helper=osxkeychain
user.name=남정현
user.email=nam9490@gmail.com
init.defaultbranch=main
```

VSCode GitHub 연동 증거:

!VSCode GitHub 연동

## 5) 검증 방법 요약

| 검증 항목 | 사용 명령 | 결과 위치 |
| --- | --- | --- |
| Docker 데몬 동작 | `docker info` | 4-3 |
| 컨테이너 실행 | `docker run`, `docker ps` | 4-4 |
| 이미지 빌드 | `docker build`, `docker images` | 4-5 |
| 포트 접속 | `curl`, 브라우저 | 4-6, screenshots/ |
| 마운트 반영 | 파일 수정 후 `curl` 비교 | 4-7 |
| 볼륨 영속성 | 컨테이너 삭제 전/후 `cat` | 4-8 |
| Git 설정 | `git config --list` | 4-9 |

## 6) 트러블슈팅

`### 사례 1: docker info 데몬 연결 실패`

- `문제:` docker info`실행 시 Client 정보는 출력되지만 Server 섹션에서`failed to connect to the docker API at unix:///Users/junghyun/.docker/run/docker.sock ... check if the daemon is running `에러 발생`
- `원인 가설: Docker CLI는 설치되어 있으나 데몬(Docker Desktop)이 실행되지 않아 소켓 파일이 존재하지 않는 것으로 추정`
- `확인: Docker Desktop 앱이 실행 중이지 않은 상태였음을 확인. 앱 실행 후 메뉴바 아이콘이 안정될 때까지 대기`
- `해결: Docker Desktop 실행 후` docker info `재시도 → Server 섹션에 Server Version 29.4.2 등 정상 출력 확인`

`### 사례 2: mkdir 실행 시 File exists 에러`

- `문제: 권한 실습 중` mkdir secret2`실행 시`mkdir: secret2: File exists `에러가 발생하고, 변경 전(755) 상태를 기록할 수 없었음`
- `원인 가설: 이전 실습에서 동일한 이름의 디렉토리를 이미 생성했고, 그 시점에 chmod 700까지 적용되어 있었던 것으로 추정`
- `확인:` ls -ld secret2`로 확인 결과 이미` drwx------`(700) 상태로 존재`
- `해결:` rm -rf secret2`로 기존 디렉토리를 삭제한 뒤 다시 생성하여, 기본 권한 755(변경 전) → chmod 700(변경 후) 비교 증거를 정상적으로 확보`

## 7) 개념 정리

### 절대 경로 vs 상대 경로

절대 경로는 루트(/)부터 시작하는 전체 주소로, 현재 위치와 무관하게 항상 같은 대상을 가리킨다(예: /Users/junghyun/codyssey/practice/memo.txt). 상대 경로는 현재 작업 디렉토리 기준의 주소다(예: memo.txt, ../practice/memo.txt). 같은 cat memo.txt라도 다른 디렉토리에서 실행하면 No such file or directory가 나는 것으로 차이를 확인했다.

### 파일 권한 (r/w/x, 755/644)

ls -l 출력의 권한 표기는 [파일종류][소유자 rwx][그룹 rwx][기타 rwx]로 읽는다. r=읽기(4), w=쓰기(2), x=실행(1)이며 세 값의 합으로 숫자 한 자리를 만든다. 755는 rwxr-xr-x(소유자 전부, 그룹/기타는 읽기+실행), 644는 rw-r--r--(소유자 읽기+쓰기, 그룹/기타는 읽기만)이다. 디렉토리에서 x는 실행이 아니라 진입(cd) 가능 여부를 의미한다. 실습에서 memo.txt를 644→600으로, secret2를 755→700으로 변경하며 전/후를 비교했다.

### 이미지 vs 컨테이너, 커스텀 이미지

이미지는 실행 환경의 읽기 전용 템플릿(설계도)이고, 컨테이너는 이미지로부터 만들어진 격리된 실행 인스턴스다. 하나의 my-web:1.0 이미지로 여러 컨테이너를 동시에 띄울 수 있다는 것이 분리의 이유이며, 이것이 "몇 번을 실행해도 같은 환경"이라는 재현성의 기반이다. 커스텀 이미지는 기존 베이스 이미지 위에 변경사항을 레이어로 얹어 만든다. 이번 실습에서는 nginx:alpine을 베이스로 정적 콘텐츠를 교체하고 LABEL/ENV/HEALTHCHECK를 추가했다.

### 포트 매핑이 필요한 이유

컨테이너는 호스트와 격리된 자체 네트워크를 가지므로 내부 포트는 기본적으로 외부에서 접근할 수 없다. -p <호스트포트>:<컨테이너포트>로 연결 통로를 만들어야 브라우저나 curl로 접속할 수 있다. 내부적으로는 모두 80 포트를 쓰는 두 컨테이너를 호스트에서 8080/8081로 나눠 충돌 없이 동시 운영할 수 있는 것도 이 격리 덕분이다.

### Docker 볼륨 (데이터 영속성)

컨테이너 내부에 기록한 데이터는 컨테이너 삭제와 함께 사라진다. 볼륨은 Docker가 컨테이너와 독립적으로 관리하는 저장 공간으로, 컨테이너에 연결해 사용하면 컨테이너를 삭제·재생성해도 데이터가 유지된다. 컨테이너는 일회용으로 취급하고 남겨야 할 데이터는 볼륨에 두는 것이 원칙이다. 호스트 디렉토리를 직접 연결하는 바인드 마운트는 개발 중 변경 반영에, 볼륨은 DB 데이터처럼 영속성이 필요한 곳에 적합하다.

### Git vs GitHub

Git은 내 컴퓨터에서 동작하는 분산 버전관리 도구로, 인터넷 없이도 git init, git commit으로 이력을 관리할 수 있다. GitHub는 Git 저장소를 호스팅하는 원격 협업 플랫폼으로, git push로 로컬 이력을 공유하고 PR·이슈 등으로 협업한다. 즉 버전관리는 Git이 하고, 공유·협업·제출은 GitHub가 담당한다.

## 8) 재현 방법

이 저장소를 클론한 뒤 아래 명령으로 동일한 결과를 재현할 수 있습니다.

```bash
git clone <저장소 URL>
cd dev-workstation
docker build -t my-web:1.0 .
docker run -d -p 8080:80 --name web-8080 my-web:1.0
curl <http://localhost:8080>
```
