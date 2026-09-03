# 05. 트러블슈팅

[← README로 돌아가기](../README.md)

## 사례 1: `docker info` 데몬 연결 실패

- **문제**: `docker info` 실행 시 Client 정보는 출력되지만 Server 섹션에서 에러 발생
    
    ```
    Server:
    failed to connect to the docker API at unix:///Users/junghyun/.docker/run/docker.sock;
    check if the path is correct and if the daemon is running: ... no such file or directory
    ```
    
- **원인 가설**: Docker CLI는 설치되어 있으나 데몬(Docker Desktop)이 실행되지 않아 소켓 파일이 존재하지 않는 것으로 추정
- **확인**: Docker Desktop 앱이 실행 중이지 않은 상태였음을 확인. 앱 실행 후 메뉴바 아이콘이 안정될 때까지 대기
- **해결**: Docker Desktop 실행 후 `docker info` 재시도 → Server 섹션에 `Server Version: 29.4.2` 등 정상 출력 확인 (02 문서 참조)

## 사례 2: `mkdir: File exists`로 권한 변경 전/후 비교 불가

- **문제**: 권한 실습 중 `mkdir secret2` 실행 시 `mkdir: secret2: File exists` 에러가 발생하고, 변경 전(755) 상태를 기록할 수 없었음
- **원인 가설**: 이전 실습에서 동일한 이름의 디렉토리를 이미 생성했고, 그 시점에 chmod 700까지 적용되어 있었던 것으로 추정
- **확인**: `ls -ld secret2` 결과 이미 `drwx------`(700) 상태로 존재함을 확인
- **해결**: `rm -rf secret2`로 기존 디렉토리를 삭제한 뒤 재생성하여, 기본 권한 755(변경 전) → chmod 700(변경 후) 비교 증거를 정상 확보 (01 문서 참조)

## 사례 3: 빌드 성공·HTTP 200인데 브라우저에 빈 페이지 표시

- **문제**: `docker build`는 성공하고 `curl -i http://localhost:8080`도 200 OK를 반환하는데, 응답 본문이 비어 있어 브라우저에 빈 화면이 표시됨
- **원인 가설**: 빌드 로그의 `transferring context: 60B`가 비정상적으로 작아, heredoc 입력이 꼬이면서 `app/index.html`이 빈 파일로 생성됐고 그 상태로 이미지에 COPY된 것으로 추정
- **확인**: `curl -i` 응답 헤더에서 `Content-Length: 0` 확인. 호스트의 index.html을 재작성했지만 여전히 빈 응답 → COPY는 빌드 시점 스냅샷이므로 호스트 파일 수정만으로는 반영되지 않음을 확인
- **해결**: index.html 재작성 후 이미지 재빌드 및 컨테이너 재생성 → 정상 응답 확인
- **교훈**: 이미지는 빌드 시점의 스냅샷이다. 호스트 파일 변경을 즉시 반영하려면 바인드 마운트를 사용해야 한다 (03 문서 참조)
