# BAEKJOON

[기본입출력](https://www.notion.so/d67a9c625689412cbcc890877e7bfff5)

### 별찍기

```python
N = int(input())
for i in range(1, N+1):
    print(" "*(N -i)+'*'*i)
```





[문자열](https://www.notion.so/4bf0b545508d486b9268520b7e4ee390)



### 팰린드롬인지 확인하기

```python
# 1. 반복문만 사용하여 풀이
P = input()
P_reverse = ""
P_lis = []

for i in P:
    P_lis.append(i)

P_lis.reverse()

for i in P_lis:
    P_reverse +=i
if P==P_reverse:
    print(1)
else:
    print(0)
```

```python
# 2. 문자열 슬라이싱을 사용하여 풀이
P = input()
if P == P[::-1]:
    print(1)
else:
    print(0)
```



### 오타맨 고창영

```python
W = int(input())
for i in range(W):
    n, w = input().split()
    n= int(n)
    print(w[:n-1],w[n:],sep="")
```



### 태보태보 총난타

```python
l, r = input().split('(^0^)')
print(l.count('@'), r.count('@'))
```

### 유학금지

```python
W = "CAMBRIDGE"
inp=input()

for w in W:
    inp=inp.replace(w,'')
print(inp)
```

