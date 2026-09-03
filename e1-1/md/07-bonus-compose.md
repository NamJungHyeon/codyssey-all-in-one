# 07. 보너스 — Docker Compose

[← README로 돌아가기](../README.md)

## 1) Compose 기초 — 단일 서비스

### docker-compose.yml

```yaml
services:
  web:
    build: .
    image: my-web:1.0
    ports:
      - "8080:80"
```

### 실행

```
<!-- docker compose up -d / docker compose ps / curl 출력 붙여넣기 -->
```

**배움 포인트**: 지금까지는 `docker run -d -p 8080:80 --name ... my-web:1.0`처럼 실행 옵션을 매번 명령어로 쳐야 했고, 옵션이 사람의 기억에 의존했다. Compose는 이 실행 설정(이미지, 포트, 볼륨 등)을 `docker-compose.yml`이라는 문서로 고정하므로, 누구든 `docker compose up` 한 번으로 동일한 구성을 재현할 수 있다. 실행 명령이 "문서화된 실행 설정"으로 바뀌는 것이다.

## 2) 멀티 컨테이너 + 네트워크 통신

<!-- 진행 시 작성: web + redis 구성, ping/통신 확인 로그 -->

## 3) Compose 운영 명령어

<!-- 진행 시 작성: up / down / ps / logs 로그 -->

## 4) 환경 변수 활용

<!-- 진행 시 작성 -->

## 5) GitHub SSH 키 설정

<!-- 진행 시 작성: ssh-keygen ~ ssh -T git@github.com 로그 (개인키·키 지문 마스킹) -->
