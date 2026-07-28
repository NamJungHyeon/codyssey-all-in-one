## 1. 터미널 기본 조작

[← README로 돌아가기](../README.md)

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

## 2. 권한 실습

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