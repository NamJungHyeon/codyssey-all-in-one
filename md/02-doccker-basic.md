## 3. Docker 설치 점검

[← README로 돌아가기](../README.md)

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

## 4. 컨테이너 기본 실습

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
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
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
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

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
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB<img width="1059" height="487" alt="Screenshot 2026-07-28 at 4 51 28 PM" src="https://github.com/user-attachments/assets/9460a749-e8e9-4e2e-81a6-d7604c436d6b" />

```