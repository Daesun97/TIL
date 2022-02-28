# SQL

- 명령을 위한 예약어에 대소문자를 구분하지 않는다
- 문자열은 ' 작은따옴표 '
- 문장 맨 뒤에 ;를 붙여줘야함
- 예약어는 대문자로, 테이블이나 속성이름은 소문자로 적으면 편함



## 분류

- 데이터 정의어 : 테이블이나 관계의 구조를 생성하는 데 사용(CREATE, ALTER, DROP 등)
- 데이터조작어 :  테이블에 데이터를 검색, 삽입, 수정,삭제하는데 사용(SELECT, INSERT, DELETE, UPDATE 등)
  - SELECT는 질의어라고 부름
- 데이터 제어어 : 데이터의 사용권한을 관리하는데 사용 (GRANT, REVOKE 등)

### 데이터 조작어 (검색)



- SELECT [ALL|DISTINCT] 속성이름(들) : *는 모든열, DISTINCT은 중복제거
- FROM 테이블 이름(들)
  - [WHERE 조건]
  - [GROUP BY 속성이름]
  - [HAVING 검색조건]
  - [ORDER BY 속성이름[ACS|DESC]] (오름차순 내림차순)

- 처리순서

			1. FROM
			1. ON
			1. JOIN
			1. WHERE
			1. GROUP BY
			1. WITH CUBE, ROLLUP
			1. HAVING
			1. SELECT
			1. DISTINCT
			1. ORDER BY
			1. TOP







#### WHERE 조건 

| 술어     | 연산자         | 예                          |
| -------- | -------------- | --------------------------- |
| 비교     | =,<>,<,<=,>,>= | <>다름을 의미함             |
| 범위     | BETWEEN        | price BETWEEN 1000 AND 2000 |
| 집합     | IN, NOT IN     | price IN (1000,2000,3000)   |
| 패턴     | LIKE           | name LIKE '윤대선'          |
| NULL     | IS (NOT) NULL  | 어쩌고 IS NULL              |
| 복합조건 | AND, OR, NOT   | 위에서 했음                 |



#### 집계 함수

| 함수  | 문법                                  | 예            |
| ----- | ------------------------------------- | ------------- |
| SUM   | SUM([ALL\|DISTINCT]속성이름)          | SUM(속성이름) |
| AVG   | AVG([ALL\|DISTINCT]속성이름)          | AVG(속성이름) |
| COUNT | COUNT({[[ALL\|DISTINCT]속성이름]\|*}) | COUNT(*)      |
| MAX   | MAX([ALL\|DISTINCT]속성이름)          | MAX(속성이름) |
| MIN   | 맥스랑 같음                           | MIN(속성이름) |





GROUP BY를 사용한 SELECT절에서는 GROUP BY를 사용한 속성과 집계함수만 사용가능



HAVING절은 GROUP BY 절의 결과를 나타나는 그룹을 제한하는 역할을 한다. 또 GROUP BY절과 같이 작성해야 하고 WHERE절보다 뒤에 나와야 한다. 검색조건에는 집계함수가 와야함

```sql
#예시
SELECT custid, COUNT(*) AS 과자값
FROM Orders
WHERE saleprice >=2500
GROUP BY custid
HAVING count(*) >=2;
```

