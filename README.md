# codyssey-all-in-one
코디세이 올인원 과정 레포
# 개념 정리

실습 과정에서 직접 확인한 내용을 기준으로 정리했다. (README의 "개념 정리" 섹션에 그대로 사용)

## 1. 절대 경로 vs 상대 경로

- **절대 경로**: 루트(`/`)부터 시작하는 전체 주소. 현재 위치와 무관하게 항상 같은 대상을 가리킨다.
- **상대 경로**: 현재 작업 디렉토리 기준의 주소.

실습 예시: `pwd`로 현재 위치가 `/Users/junghyun/codyssey/practice`일 때,

```bash
cat /Users/junghyun/codyssey/practice/memo.txt   # 절대 경로 — 어디서 실행해도 동일
cat memo.txt                                     # 상대 경로 — practice 안에서만 동작
cat ../practice/memo.txt                         # 상대 경로 — 상위(..)를 거쳐 접근
```

홈 디렉토리로 이동한 뒤 `cat memo.txt`를 실행하면 `No such file or directory`가 나온다. 같은 명령이라도 상대 경로는 현재 위치에 따라 결과가 달라진다는 것을 확인했다.

## 2. 파일 권한 (r/w/x, 755, 644)

`ls -l` 출력의 권한 10칸은 `[파일종류][소유자 rwx][그룹 rwx][기타 rwx]`로 읽는다.
r=읽기(4), w=쓰기(2), x=실행(1)이며, 세 값을 더해 숫자 한 자리로 표기한다.

- `755` = `rwxr-xr-x` : 소유자는 전부(7), 그룹/기타는 읽기+실행(5)
- `644` = `rw-r--r--` : 소유자는 읽기+쓰기(6), 그룹/기타는 읽기만(4)

실습에서 확인한 변경 전/후:

```bash
$ ls -l memo.txt
-rw-r--r--  memo.txt        # 644
$ chmod 600 memo.txt
$ ls -l memo.txt
-rw-------  memo.txt        # 600: 소유자 외 접근 차단

$ ls -ld secret
drwxr-xr-x  secret          # 755
$ chmod 700 secret
$ ls -ld secret
drwx------  secret          # 700
```

디렉토리에서 x는 "실행"이 아니라 **진입(cd) 가능** 여부를 뜻한다. x를 빼면 목록에 보여도 들어갈 수 없다.

## 3. 이미지와 컨테이너, 커스텀 이미지

- **이미지**: 실행 환경의 읽기 전용 템플릿(설계도).
- **컨테이너**: 이미지로부터 만들어진 격리된 실행 인스턴스(실체).

`docker images`에는 `my-web:1.0`이 1개지만, `docker ps`에는 그 이미지로 띄운 컨테이너(web-8080, web-8081)가 여러 개 존재했다. 하나의 설계도로 동일한 실행 환경을 몇 번이고 재현할 수 있다는 것이 분리의 이유다.

커스텀 이미지는 기존 베이스 이미지 위에 내 변경사항을 레이어로 얹어 만든다. 이번 실습에서는 `nginx:alpine`을 베이스로 정적 콘텐츠만 교체했다.

```dockerfile
FROM nginx:alpine          # 기존 베이스 재사용
COPY app/ /usr/share/nginx/html/   # 내 콘텐츠로 교체
```

`docker build -t my-web:1.0 .`로 빌드하면 NGINX 설치 과정 없이 내 페이지를 서빙하는 이미지가 완성된다.

## 4. 포트 매핑이 필요한 이유

컨테이너는 호스트와 격리된 자체 네트워크 공간을 가진다. 컨테이너 내부의 80 포트는 기본적으로 호스트에서 보이지 않으므로, `-p <호스트포트>:<컨테이너포트>`로 연결 통로를 만들어야 외부에서 접속할 수 있다.

```bash
docker run -d -p 8080:80 --name web-8080 my-web:1.0
docker run -d -p 8081:80 --name web-8081 my-web:1.0
```

두 컨테이너 모두 내부적으로는 80 포트를 쓰지만, 호스트에서는 8080/8081로 나뉘어 충돌 없이 동시에 접속됐다(`curl http://localhost:8080`, `:8081` 모두 응답). 격리 덕분에 같은 서비스를 포트만 바꿔 여러 개 실행할 수 있다는 점을 확인했다.

## 5. 바인드 마운트와 Docker 볼륨 (데이터 영속성)

컨테이너 내부에 쓴 데이터는 컨테이너 삭제와 함께 사라진다. 이를 해결하는 두 방식을 실습했다.

- **바인드 마운트**: 호스트의 실제 디렉토리를 컨테이너에 연결. 호스트에서 `app/index.html`을 수정하자 재빌드 없이 `curl` 응답에 즉시 반영됐다. → 개발 중 코드 반영에 유리
- **볼륨**: Docker가 관리하는 저장 공간. 컨테이너 수명과 독립적이다.

볼륨 영속성 검증 결과:

```bash
$ docker volume create mydata
$ docker exec vol-test bash -c "echo persist-test > /data/hello.txt"
$ docker rm -f vol-test              # 컨테이너 삭제
$ docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
$ docker exec vol-test2 cat /data/hello.txt
persist-test                         # 데이터 유지 확인
```

컨테이너를 삭제하고 새로 만들어도 볼륨의 데이터는 그대로였다. 컨테이너는 일회용으로 취급하고, 남겨야 할 데이터는 볼륨에 두는 이유다.

## 6. Git vs GitHub

- **Git**: 내 컴퓨터에서 동작하는 분산 버전관리 도구. 인터넷 없이도 `git init`, `git commit`으로 이력 관리가 가능하다.
- **GitHub**: Git 저장소를 호스팅하는 원격 협업 플랫폼. `git push`로 로컬 이력을 올리고, PR/이슈 등으로 협업한다.

실습에서 로컬 커밋까지는 GitHub 없이 완료했고, `git remote add origin` + `git push` 시점부터 GitHub가 개입했다. 즉 버전관리는 Git이 하고, 공유·협업·제출은 GitHub가 담당한다.

## 7. (추가 관찰) 컨테이너 종료/유지 — run·attach vs exec

- `docker run -it ubuntu bash` 후 `exit` → 컨테이너가 **종료**됐다. bash가 PID 1(메인 프로세스)이라 bash 종료 = 컨테이너 종료.
- `docker run -d ... sleep infinity`로 띄운 컨테이너에 `docker exec -it ubt2 bash`로 진입 후 `exit` → `docker ps`에서 여전히 **Up**. exec는 별도 프로세스를 추가로 띄우는 것이라 메인 프로세스(sleep)에 영향이 없다.
- attach는 PID 1의 입출력에 직접 붙는 방식이므로, 붙었다가 종료 시그널을 보내면 컨테이너까지 내려갈 수 있다. 조작용 진입은 exec가 안전하다.
