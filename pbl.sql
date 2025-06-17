USE db20230B234;

-- 1. 학과 테이블 생성
CREATE TABLE IF NOT EXISTS 학과_2번 (
    학과ID INT AUTO_INCREMENT PRIMARY KEY,
    학과명 VARCHAR(50) NOT NULL
);

-- 2. 직원 테이블 생성
CREATE TABLE IF NOT EXISTS 직원_2번 (
    직원ID INT AUTO_INCREMENT PRIMARY KEY,
    이름 VARCHAR(50) NOT NULL
);

-- 3. 학생 테이블 생성 (학과 참조)
CREATE TABLE IF NOT EXISTS 학생_2번 (
    학생ID INT AUTO_INCREMENT PRIMARY KEY,
    이름 VARCHAR(50)  NOT NULL DEFAULT '이름없음',
    소속학과ID INT NOT NULL,
    FOREIGN KEY (소속학과ID) REFERENCES 학과_2번(학과ID) ON DELETE CASCADE
);


-- 4. 교수 테이블 생성 (학과 참조)
CREATE TABLE IF NOT EXISTS 교수_2번 (
    교수ID INT AUTO_INCREMENT PRIMARY KEY,
    교수명 VARCHAR(50) NOT NULL,
    소속학과ID INT NOT NULL,
    FOREIGN KEY (소속학과ID) REFERENCES 학과_2번(학과ID) ON DELETE CASCADE
);

-- 5. 강의실 테이블 생성
CREATE TABLE IF NOT EXISTS 강의실_2번 (
    강의실ID INT AUTO_INCREMENT PRIMARY KEY,
    호실명 VARCHAR(50) NOT NULL,
    호실 VARCHAR(50) NOT NULL,
    건물명 VARCHAR(50) NOT NULL
);

-- 6. 과목 테이블 생성 (교수 및 강의실 참조) - 학점 컬럼 추가
CREATE TABLE IF NOT EXISTS 과목_2번 (
    과목ID INT AUTO_INCREMENT PRIMARY KEY,
    과목명 VARCHAR(50) NOT NULL,
    학점 INT NOT NULL DEFAULT 3,
    교수ID INT NOT NULL,
    강의실ID INT,
    FOREIGN KEY (교수ID) REFERENCES 교수_2번(교수ID) ON DELETE CASCADE,
    FOREIGN KEY (강의실ID) REFERENCES 강의실_2번(강의실ID) ON DELETE SET NULL
);

-- 7. 학생_로그인 테이블 생성 (학생 및 학과 참조)
CREATE TABLE IF NOT EXISTS 학생_로그인 (
    로그인ID INT AUTO_INCREMENT PRIMARY KEY,
    학생ID INT NOT NULL,
    아이디 VARCHAR(50) NOT NULL UNIQUE,
    비밀번호 VARCHAR(255) NOT NULL,
    이름 VARCHAR(50) NOT NULL,
    소속학과ID INT NOT NULL,
    FOREIGN KEY (학생ID) REFERENCES 학생_2번(학생ID) ON DELETE CASCADE,
    FOREIGN KEY (소속학과ID) REFERENCES 학과_2번(학과ID) ON DELETE CASCADE
);

-- 8. 교수_로그인 테이블 생성 (교수 참조)
CREATE TABLE IF NOT EXISTS 교수_로그인 (
    로그인ID INT AUTO_INCREMENT PRIMARY KEY,
    교수ID INT NOT NULL,
    아이디 VARCHAR(50) NOT NULL UNIQUE,
    비밀번호 VARCHAR(255) NOT NULL,
    FOREIGN KEY (교수ID) REFERENCES 교수_2번(교수ID) ON DELETE CASCADE
);

-- 9. 직원_로그인 테이블 생성 (직원 참조)
CREATE TABLE IF NOT EXISTS 직원_로그인 (
    로그인ID INT AUTO_INCREMENT PRIMARY KEY,
    직원ID INT NOT NULL,
    아이디 VARCHAR(50) NOT NULL UNIQUE,
    비밀번호 VARCHAR(255) NOT NULL,
    FOREIGN KEY (직원ID) REFERENCES 직원_2번(직원ID) ON DELETE CASCADE
);

-- 10. 과목 시간 테이블 생성 (과목 참조)
CREATE TABLE IF NOT EXISTS 과목_시간_2번 (
    시간ID INT AUTO_INCREMENT PRIMARY KEY,
    과목ID INT NOT NULL,
    요일 VARCHAR(10) NOT NULL,
    시작교시 INT NOT NULL,
    종료교시 INT NOT NULL,
    FOREIGN KEY (과목ID) REFERENCES 과목_2번(과목ID) ON DELETE CASCADE
);

-- 11. 수강신청 테이블 생성 (학생 및 과목 참조)
CREATE TABLE IF NOT EXISTS 수강신청_2번 (
    신청ID INT AUTO_INCREMENT PRIMARY KEY,
    학생ID INT NOT NULL,
    과목ID INT NOT NULL,
    요일 VARCHAR(10) NOT NULL,       -- 수업 요일 추가
    시작교시 INT NOT NULL,           -- 수업 시작 교시 추가
    종료교시 INT NOT NULL,           -- 수업 종료 교시 추가
    FOREIGN KEY (학생ID) REFERENCES 학생_2번(학생ID) ON DELETE CASCADE,
    FOREIGN KEY (과목ID) REFERENCES 과목_2번(과목ID) ON DELETE CASCADE,
    UNIQUE (학생ID, 과목ID)
);



-- 뷰
-- 학과별 교수 목록
-- 학과별 교수 목록
CREATE OR REPLACE VIEW 학과별_교수목록 AS
SELECT
    g.교수ID,       -- 교수의 고유 식별자
    g.교수명,       -- 교수 이름
    d.학과명        -- 교수의 소속 학과 이름
FROM 교수_2번 g
JOIN 학과_2번 d ON g.소속학과ID = d.학과ID; -- 교수의 소속 학과ID를 학과 테이블의 학과ID와 매칭

-- 강의실 목록
CREATE OR REPLACE VIEW 강의실목록 AS
SELECT
    강의실ID,      -- 강의실의 고유 식별자
    호실명,         -- 강의실 이름
    호실,          -- 강의실 번호
    건물명          -- 강의실이 위치한 건물 이름
FROM 강의실_2번;

-- 학과별 교과목 목록
CREATE OR REPLACE VIEW 학과별_교과목목록 AS
SELECT
    c.과목ID,       -- 과목의 고유 식별자
    c.과목명,       -- 과목 이름
    c.학점,         -- 과목 학점
    p.교수명,       -- 과목을 담당하는 교수 이름
    d.학과명        -- 과목이 속한 학과 이름
FROM 과목_2번 c
JOIN 교수_2번 p ON c.교수ID = p.교수ID          -- 과목의 교수ID와 교수 테이블의 교수ID를 매칭
JOIN 학과_2번 d ON p.소속학과ID = d.학과ID;     -- 교수의 소속 학과ID와 학과 테이블의 학과ID를 매칭

-- 학생별 신청 과목 목록
CREATE OR REPLACE VIEW 학생별_신청과목목록 AS
SELECT
    s.학생ID,       -- 학생의 고유 식별자
    st.이름 AS 학생명,  -- 학생 이름
    c.과목ID,       -- 과목의 고유 식별자
    c.과목명,       -- 과목 이름
    c.학점,         -- 과목 학점
    p.교수명,       -- 과목 담당 교수 이름
    r.건물명,       -- 수업이 이루어지는 건물 이름
    r.호실명,       -- 수업이 이루어지는 강의실 이름
    s.요일,         -- 수업 요일
    s.시작교시,     -- 수업 시작 교시
    s.종료교시      -- 수업 종료 교시
FROM 수강신청_2번 s
JOIN 학생_2번 st ON s.학생ID = st.학생ID       -- 수강 신청의 학생ID와 학생 테이블의 학생ID를 매칭
JOIN 과목_2번 c ON s.과목ID = c.과목ID         -- 수강 신청의 과목ID와 과목 테이블의 과목ID를 매칭
JOIN 교수_2번 p ON c.교수ID = p.교수ID         -- 과목의 교수ID와 교수 테이블의 교수ID를 매칭
JOIN 강의실_2번 r ON c.강의실ID = r.강의실ID;  -- 과목의 강의실ID와 강의실 테이블의 강의실ID를 매칭

-- 과목별 수강 학생 목록
CREATE OR REPLACE VIEW 과목별_수강학생목록 AS
SELECT
    c.과목ID,       -- 과목의 고유 식별자
    c.과목명,       -- 과목 이름
    s.학생ID,       -- 수강 신청한 학생의 고유 식별자
    st.이름 AS 학생명,  -- 학생 이름
    s.요일,         -- 수업 요일
    s.시작교시,     -- 수업 시작 교시
    s.종료교시      -- 수업 종료 교시
FROM 수강신청_2번 s
JOIN 과목_2번 c ON s.과목ID = c.과목ID         -- 수강 신청의 과목ID와 과목 테이블의 과목ID를 매칭
JOIN 학생_2번 st ON s.학생ID = st.학생ID;      -- 수강 신청의 학생ID와 학생 테이블의 학생ID를 매칭

-- 함수 / 프로시저 
-- 시간 중복 체크 함수
DELIMITER //

CREATE FUNCTION 시간중복체크(
    입력학생ID INT,
    입력요일 VARCHAR(10),
    입력시작교시 INT,
    입력종료교시 INT
)
RETURNS BOOLEAN
BEGIN
    DECLARE 중복횟수 INT;

    SELECT COUNT(*) INTO 중복횟수
    FROM 수강신청_2번
    WHERE 학생ID = 입력학생ID
      AND 요일 = 입력요일
      AND (시작교시 <= 입력종료교시 AND 종료교시 >= 입력시작교시);

    RETURN 중복횟수 > 0;
END;
DELIMITER //

-- 수강신청 프로시저
DELIMITER //

CREATE PROCEDURE 수강신청(
    IN 입력학생ID INT,        -- 수강신청을 하는 학생 ID
    IN 입력과목ID INT,        -- 수강신청 과목 ID
    IN 입력요일 VARCHAR(10),  -- 수강신청 요일
    IN 입력시작교시 INT,      -- 수업 시작 교시
    IN 입력종료교시 INT       -- 수업 종료 교시
)
BEGIN
    DECLARE 과목학점 INT;     -- 해당 과목의 총 학점
    DECLARE 남은학점 INT;     -- 남은 학점을 계산하기 위한 변수
    DECLARE 신청학점 INT;     -- 이번에 신청하는 학점을 계산하기 위한 변수
    DECLARE 중복여부 BOOLEAN; -- 시간 중복 여부를 확인하기 위한 변수

    -- 과목 학점 조회
    SELECT 학점 INTO 과목학점 FROM 과목_2번 WHERE 과목ID = 입력과목ID;

    -- 과목이 존재하지 않는 경우 오류 발생
    IF 과목학점 IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '해당 과목ID가 존재하지 않습니다.';
    END IF;

    -- 입력한 교시 구간의 학점을 계산
    SET 신청학점 = 입력종료교시 - 입력시작교시 + 1;

    -- 잘못된 교시 입력 확인 (시작 교시와 종료 교시가 올바르지 않으면 오류 발생)
    IF 신청학점 <= 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '잘못된 교시 입력입니다.';
    END IF;

    -- 해당 과목의 남은 학점 계산
    SELECT 과목학점 - IFNULL(SUM(종료교시 - 시작교시 + 1), 0)
    INTO 남은학점
    FROM 수강신청_2번
    WHERE 학생ID = 입력학생ID AND 과목ID = 입력과목ID;

    -- 신청 학점이 남은 학점을 초과하면 오류 발생
    IF 신청학점 > 남은학점 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '신청 학점 초과: 남은 학점을 초과했습니다.';
    END IF;

    -- 시간 중복 체크 함수 호출
    SET 중복여부 = 시간중복체크(입력학생ID, 입력요일, 입력시작교시, 입력종료교시);

    -- 시간 중복이 발생하면 오류 발생
    IF 중복여부 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '시간이 중복됩니다.';
    ELSE
        -- 중복이 없으면 수강 신청 등록
        INSERT INTO 수강신청_2번 (학생ID, 과목ID, 요일, 시작교시, 종료교시)
        VALUES (입력학생ID, 입력과목ID, 입력요일, 입력시작교시, 입력종료교시);
    END IF;
END //

DELIMITER ;

-- 뷰 삭제
DROP VIEW IF EXISTS 과목별_수강학생목록;
DROP VIEW IF EXISTS 학생별_신청과목목록;
DROP VIEW IF EXISTS 학과별_교과목목록;
DROP VIEW IF EXISTS 강의실목록;
DROP VIEW IF EXISTS 학과별_교수목록;

DROP PROCEDURE IF EXISTS 수강신청;
DROP FUNCTION IF EXISTS 시간중복체크;



-- 삭제할 때 쓸 명령어
DROP TABLE IF EXISTS 수강신청_2번;
DROP TABLE IF EXISTS 과목_시간_2번;
DROP TABLE IF EXISTS 직원_로그인;
DROP TABLE IF EXISTS 교수_로그인;
DROP TABLE IF EXISTS 학생_로그인;
DROP TABLE IF EXISTS 과목_2번;
DROP TABLE IF EXISTS 강의실_2번;
DROP TABLE IF EXISTS 교수_2번;
DROP TABLE IF EXISTS 학생_2번;
DROP TABLE IF EXISTS 직원_2번;
DROP TABLE IF EXISTS 학과_2번;

ALTER TABLE 학생_2번
MODIFY COLUMN 이름 VARCHAR(50) NOT NULL DEFAULT '이름없음';



select *
from 과목_2번;
-- 초기화
SET SQL_SAFE_UPDATES = 0;

DELETE FROM 강의실_2번;

SET SQL_SAFE_UPDATES = 1; -- 작업 후 다시 활성화

