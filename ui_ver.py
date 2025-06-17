from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QMessageBox, QComboBox, QInputDialog, QDialog, QTableWidget,QAbstractItemView,
    QTableWidgetItem, QFormLayout

)
from PyQt5.QtGui import QIntValidator

import pymysql

# 데이터베이스 연결
db = pymysql.connect(
    host="acclabs.iptime.org",
    user="st20230B234",
    password="1234",
    database="db20230B234",
    port=33066,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("수강 시스템 프로그램")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.title_label = QLabel("수강 시스템 프로그램", self)
        layout.addWidget(self.title_label)

        self.login_button = QPushButton("로그인", self)
        self.signup_button = QPushButton("회원가입", self)
        self.exit_button = QPushButton("종료", self)

        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.exit_button)

        self.login_button.clicked.connect(self.show_login)
        self.signup_button.clicked.connect(self.show_signup)
        self.exit_button.clicked.connect(self.close_application)

        self.central_widget.setLayout(layout)

    def show_login(self):
        try:
            login_window = LoginWindow()
            login_window.exec_()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"로그인 창을 여는 중 문제가 발생했습니다: {str(e)}")


    def show_signup(self):
        signup_window = SignupWindow()
        signup_window.exec_()

    def close_application(self):
        cursor.close()
        db.close()
        QApplication.quit()


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setGeometry(150, 150, 400, 300)
        self.layout = QVBoxLayout()

        self.user_type_label = QLabel("사용자 유형을 선택하세요:", self)
        self.layout.addWidget(self.user_type_label)

        self.user_type_combo = QComboBox(self)
        self.user_type_combo.addItems(["학생", "교수", "교직원"])
        self.layout.addWidget(self.user_type_combo)

        self.id_label = QLabel("아이디:", self)
        self.layout.addWidget(self.id_label)
        self.id_input = QLineEdit(self)
        self.layout.addWidget(self.id_input)

        self.password_label = QLabel("비밀번호:", self)
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("로그인", self)
        self.layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.handle_login)

        self.setLayout(self.layout)

    def handle_login(self):
        try:
            user_type = self.user_type_combo.currentText()
            user_id = self.id_input.text()
            password = self.password_input.text()

            if user_type == "학생":
                query = """
                SELECT s.학생ID, s.이름
                FROM 학생_로그인 l
                JOIN 학생_2번 s ON l.학생ID = s.학생ID
                WHERE l.아이디 = %s AND l.비밀번호 = %s
                """
                cursor.execute(query, (user_id, password))
                user = cursor.fetchone()
                if user:
                    QMessageBox.information(self, "성공", f"환영합니다, {user['이름']}님!")
                    self.close()
                    학생메뉴(user['학생ID'], user['이름']).exec_()
                else:
                    QMessageBox.warning(self, "오류", "아이디 또는 비밀번호가 올바르지 않습니다.")
            elif user_type == "교수":
                query = """
                SELECT l.교수ID, g.교수명
                FROM 교수_로그인 l
                JOIN 교수_2번 g ON l.교수ID = g.교수ID
                WHERE l.아이디 = %s AND l.비밀번호 = %s
                """
                cursor.execute(query, (user_id, password))
                user = cursor.fetchone()
                if user:
                    QMessageBox.information(self, "성공", f"환영합니다, {user['교수명']} 교수님!")
                    self.close()
                    교수메뉴(user['교수ID'], user['교수명']).exec_()
                else:
                    QMessageBox.warning(self, "오류", "아이디 또는 비밀번호가 올바르지 않습니다.")
            elif user_type == "교직원":
                query = """
                SELECT w.직원ID, s.이름
                FROM 직원_로그인 w
                JOIN 직원_2번 s ON w.직원ID = s.직원ID
                WHERE w.아이디 = %s AND w.비밀번호 = %s
                """
                cursor.execute(query, (user_id, password))
                user = cursor.fetchone()
                if user:
                    QMessageBox.information(self, "성공", f"환영합니다, {user['이름']}님!")
                    self.close()
                    직원메뉴(user['이름']).exec_()
                else:
                    QMessageBox.warning(self, "오류", "아이디 또는 비밀번호가 올바르지 않습니다.")
            else:
                QMessageBox.warning(self, "오류", "올바른 사용자 유형을 선택하세요.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"로그인 중 문제가 발생했습니다: {str(e)}")





class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원가입")
        self.setGeometry(150, 150, 400, 300)
        self.layout = QVBoxLayout()

        self.user_type_label = QLabel("회원가입 유형을 선택하세요:", self)
        self.layout.addWidget(self.user_type_label)

        self.user_type_combo = QComboBox(self)
        self.user_type_combo.addItems(["학생", "교수", "교직원"])
        self.layout.addWidget(self.user_type_combo)

        self.signup_button = QPushButton("회원가입 진행", self)
        self.layout.addWidget(self.signup_button)
        self.signup_button.clicked.connect(self.handle_signup)

        self.setLayout(self.layout)

    def handle_signup(self):
        user_type = self.user_type_combo.currentText()

        if user_type == "학생":
            학생_회원가입()
        elif user_type == "교수":
            교수_회원가입()
        elif user_type == "교직원":
            직원_회원가입()
        else:
            QMessageBox.warning(self, "오류", "올바른 사용자 유형을 선택하세요.")


# 학생 메뉴
class 학생메뉴(QDialog):
    def __init__(self, 학생ID, 이름):
        super().__init__()
        self.학생ID = 학생ID
        self.이름 = 이름
        self.setWindowTitle(f"{이름}님의 학생 메뉴")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        self.title_label = QLabel(f"환영합니다, {이름}님!", self)
        self.layout.addWidget(self.title_label)

        self.view_courses_button = QPushButton("수강 과목 조회", self)
        self.enroll_button = QPushButton("수강 신청", self)
        self.cancel_button = QPushButton("수강 취소", self)
        self.logout_button = QPushButton("로그아웃", self)

        self.layout.addWidget(self.view_courses_button)
        self.layout.addWidget(self.enroll_button)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.logout_button)

        # 버튼 클릭 이벤트 연결
        self.view_courses_button.clicked.connect(self.view_courses)
        self.enroll_button.clicked.connect(self.enroll_course)  # 연결 문제 수정
        self.cancel_button.clicked.connect(self.cancel_course)
        self.logout_button.clicked.connect(self.logout)

        self.setLayout(self.layout)

    def create_table_widget(self, data, headers):
        """
        Helper function to create and populate a QTableWidget for displaying data.
        """
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 행 선택 활성화
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        table.resizeColumnsToContents()
        return table
    def view_courses(self):
        """
        View currently enrolled courses.
        """
        try:
            query = """
            SELECT *
            FROM 학생별_신청과목목록
            WHERE 학생ID = %s
            ORDER BY 
                CASE
                    WHEN 요일 = '월요일' THEN 1
                    WHEN 요일 = '화요일' THEN 2
                    WHEN 요일 = '수요일' THEN 3
                    WHEN 요일 = '목요일' THEN 4
                    WHEN 요일 = '금요일' THEN 5
                    WHEN 요일 = '토요일' THEN 6
                    WHEN 요일 = '일요일' THEN 7
                    ELSE 8
                END,
                시작교시;
            """
            cursor.execute(query, (self.학생ID,))
            courses = cursor.fetchall()
            if courses:
                headers = ["과목명", "교수명", "건물명", "강의실명", "요일", "시작교시", "종료교시"]
                data = [
                    [
                        course["과목명"],
                        course["교수명"],
                        course["건물명"],
                        course["호실명"],
                        course["요일"],
                        course["시작교시"],
                        course["종료교시"],
                    ]
                    for course in courses
                ]
                table = self.create_table_widget(data, headers)
                dialog = QDialog(self)
                dialog.setWindowTitle("수강 과목 조회")
                dialog_layout = QVBoxLayout()
                dialog_layout.addWidget(table)
                dialog.setLayout(dialog_layout)
                dialog.exec()
            else:
                QMessageBox.information(self, "수강 과목 조회", "신청된 과목이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수강 과목 조회 실패: {str(e)}")
            
    def enroll_course(self):
        """
        Enroll in a course with support for specifying day and time, while only checking credit limits.
        """
        try:
            학과명, ok = QInputDialog.getText(self, "학과 선택", "수강할 과목의 학과명을 입력하세요:")
            if ok and 학과명:
                query = "SELECT 과목ID, 과목명, 교수명, 학점 FROM 학과별_교과목목록 WHERE 학과명 = %s"
                cursor.execute(query, (학과명,))
                courses = cursor.fetchall()

                if courses:
                    headers = ["과목ID", "과목명", "교수명", "학점"]
                    data = [
                        [course["과목ID"], course["과목명"], course["교수명"], course["학점"]]
                        for course in courses
                    ]
                    table = self.create_table_widget(data, headers)

                    dialog = QDialog(self)
                    dialog.setWindowTitle("수강 가능한 과목")
                    dialog_layout = QVBoxLayout()
                    dialog_layout.addWidget(QLabel(f"학과 '{학과명}'의 수강 가능한 과목 목록"))
                    dialog_layout.addWidget(table)

                    # 입력 필드 추가
                    input_layout = QFormLayout()
                    course_id_input = QLineEdit()
                    day_input = QLineEdit()
                    start_time_input = QLineEdit()
                    end_time_input = QLineEdit()

                    input_layout.addRow("과목 ID 입력:", course_id_input)
                    input_layout.addRow("요일 입력 (예: 월요일):", day_input)
                    input_layout.addRow("시작 교시 입력:", start_time_input)
                    input_layout.addRow("종료 교시 입력:", end_time_input)

                    enroll_button = QPushButton("신청")
                    input_layout.addWidget(enroll_button)

                    dialog_layout.addLayout(input_layout)
                    dialog.setLayout(dialog_layout)

                    def submit_enrollment():
                        try:
                            과목ID = course_id_input.text().strip()
                            요일 = day_input.text().strip()
                            시작교시 = int(start_time_input.text().strip())
                            종료교시 = int(end_time_input.text().strip())

                            if not (과목ID and 요일 and 시작교시 and 종료교시):
                                QMessageBox.warning(dialog, "오류", "모든 필드를 입력하세요.")
                                return

                            if 시작교시 > 종료교시:
                                QMessageBox.warning(dialog, "오류", "종료 교시는 시작 교시보다 커야 합니다.")
                                return

                            # 학점 초과 여부 확인
                            query = """
                            SELECT SUM(종료교시 - 시작교시 + 1) AS 신청된학점
                            FROM 수강신청_2번
                            WHERE 학생ID = %s AND 과목ID = %s
                            """
                            cursor.execute(query, (self.학생ID, 과목ID))
                            result = cursor.fetchone()
                            신청된학점 = result["신청된학점"] if result["신청된학점"] else 0

                            # 과목의 최대 학점 확인
                            query = "SELECT 학점 FROM 과목_2번 WHERE 과목ID = %s"
                            cursor.execute(query, (과목ID,))
                            max_credits = cursor.fetchone()["학점"]

                            if 신청된학점 + (종료교시 - 시작교시 + 1) > max_credits:
                                QMessageBox.warning(
                                    dialog,
                                    "오류",
                                    f"학점 초과: 최대 학점({max_credits})을 초과할 수 없습니다."
                                )
                                return

                            # 데이터 삽입 (시간대 중복은 무시)
                            query = """
                            INSERT INTO 수강신청_2번 (학생ID, 과목ID, 요일, 시작교시, 종료교시)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(query, (self.학생ID, 과목ID, 요일, 시작교시, 종료교시))
                            db.commit()

                            QMessageBox.information(
                                dialog,
                                "성공",
                                f"과목 {과목ID} 수강 신청 완료: {요일}, {시작교시}교시 ~ {종료교시}교시"
                            )
                            dialog.close()

                        except ValueError:
                            QMessageBox.warning(dialog, "오류", "교시 입력은 숫자로만 입력하세요.")
                        except Exception as e:
                            db.rollback()
                            QMessageBox.critical(dialog, "오류", f"수강 신청 실패: {str(e)}")

                    enroll_button.clicked.connect(submit_enrollment)
                    dialog.exec()

                else:
                    QMessageBox.information(self, "수강 신청", "선택한 학과에 수강 가능한 과목이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수강 신청 실패: {str(e)}")

    def cancel_course(self):
        """
        Cancel an enrolled course after displaying the currently enrolled course list.
        """
        try:
            query = """
            SELECT s.과목ID, c.과목명
            FROM 수강신청_2번 s
            JOIN 과목_2번 c ON s.과목ID = c.과목ID
            WHERE s.학생ID = %s
            """
            cursor.execute(query, (self.학생ID,))
            courses = cursor.fetchall()

            if courses:
                headers = ["과목ID", "과목명"]
                data = [[course["과목ID"], course["과목명"]] for course in courses]
                table = self.create_table_widget(data, headers)

                dialog = QDialog(self)
                dialog.setWindowTitle("신청한 과목")
                dialog_layout = QVBoxLayout()
                dialog_layout.addWidget(QLabel("신청한 과목 목록"))
                dialog_layout.addWidget(table)

                # 입력 필드
                input_label = QLabel("취소할 과목 ID 입력:")
                course_id_input = QLineEdit()
                cancel_button = QPushButton("취소")

                dialog_layout.addWidget(input_label)
                dialog_layout.addWidget(course_id_input)
                dialog_layout.addWidget(cancel_button)

                def submit_cancellation():
                    과목ID = course_id_input.text()
                    if not 과목ID:
                        QMessageBox.warning(dialog, "오류", "과목 ID를 입력하세요.")
                        return
                    try:
                        query = "DELETE FROM 수강신청_2번 WHERE 학생ID = %s AND 과목ID = %s"
                        cursor.execute(query, (self.학생ID, 과목ID))
                        db.commit()
                        QMessageBox.information(dialog, "성공", f"과목 {과목ID} 취소 완료!")
                        dialog.close()
                    except Exception as e:
                        QMessageBox.critical(dialog, "오류", f"수강 취소 실패: {str(e)}")

                cancel_button.clicked.connect(submit_cancellation)

                dialog.setLayout(dialog_layout)
                dialog.exec()
            else:
                QMessageBox.information(self, "수강 취소", "신청한 과목이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수강 취소 실패: {str(e)}")


    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃합니다.")
        self.close()

class 교수메뉴(QDialog):
    def __init__(self, 교수ID, 교수명):
        super().__init__()
        self.교수ID = 교수ID
        self.교수명 = 교수명
        self.setWindowTitle(f"{교수명} 교수님 - 교수 메뉴")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        self.title_label = QLabel(f"환영합니다, {교수명} 교수님!", self)
        self.layout.addWidget(self.title_label)

        self.view_courses_button = QPushButton("담당 과목 조회", self)
        self.view_students_button = QPushButton("수강 학생 조회", self)
        self.view_professors_button = QPushButton("교수 목록 조회", self)
        self.view_rooms_button = QPushButton("강의실 목록 조회", self)
        self.view_subjects_button = QPushButton("교과목 목록 조회", self)
        self.view_student_subjects_button = QPushButton("학생별 교과목 조회", self)
        self.logout_button = QPushButton("로그아웃", self)

        self.layout.addWidget(self.view_courses_button)
        self.layout.addWidget(self.view_students_button)
        self.layout.addWidget(self.view_professors_button)
        self.layout.addWidget(self.view_rooms_button)
        self.layout.addWidget(self.view_subjects_button)
        self.layout.addWidget(self.view_student_subjects_button)
        self.layout.addWidget(self.logout_button)

        # 버튼 클릭 이벤트 연결
        self.view_courses_button.clicked.connect(self.view_courses)
        self.view_students_button.clicked.connect(self.view_students)
        self.view_professors_button.clicked.connect(self.view_professors)
        self.view_rooms_button.clicked.connect(self.view_rooms)
        self.view_subjects_button.clicked.connect(self.view_subjects)
        self.view_student_subjects_button.clicked.connect(self.view_student_subjects)
        self.logout_button.clicked.connect(self.logout)

        self.setLayout(self.layout)

    def create_table_widget(self, data, headers):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        table.resizeColumnsToContents()
        return table
    def view_courses(self):
        """
        담당 교과목 조회 기능
        """
        try:
            # 교수ID와 소속학과ID를 로그인된 교수의 이름으로 가져오기
            query = """
            SELECT 교수ID, 소속학과ID
            FROM 교수_2번
            WHERE 교수ID = %s
            """
            cursor.execute(query, (self.교수ID,))  # 로그인된 교수 ID를 기준으로 조회
            professor = cursor.fetchone()

            if not professor:
                QMessageBox.warning(self, "오류", "로그인된 교수 정보가 없습니다.")
                return

            교수ID = professor["교수ID"]
            소속학과ID = professor["소속학과ID"]

            # 교수ID를 기준으로 담당 교과목 조회
            query = """
            SELECT c.과목ID, c.과목명, c.학점, r.호실명 AS 강의실명
            FROM 과목_2번 c
            JOIN 강의실_2번 r ON c.강의실ID = r.강의실ID
            WHERE c.교수ID = %s
            """
            cursor.execute(query, (교수ID,))
            courses = cursor.fetchall()

            if not courses:
                QMessageBox.information(self, "조회 결과", "담당 과목이 없습니다.")
                return

            # 데이터 테이블 생성
            headers = ["과목ID", "과목명", "학점", "강의실명"]
            data = [[course["과목ID"], course["과목명"], course["학점"], course["강의실명"]] for course in courses]
            table = self.create_table_widget(data, headers)

            # 테이블 표시용 다이얼로그 생성
            dialog = QDialog(self)
            dialog.setWindowTitle("담당 교과목 조회")
            layout = QVBoxLayout()
            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "오류", f"담당 교과목 조회 실패: {str(e)}")

    def view_students(self):
        try:
            query = """
            SELECT s.학생ID, s.이름, c.과목명
            FROM 수강신청_2번 e
            JOIN 학생_2번 s ON e.학생ID = s.학생ID
            JOIN 과목_2번 c ON e.과목ID = c.과목ID
            WHERE c.교수ID = %s
            """
            cursor.execute(query, (self.교수ID,))
            students = cursor.fetchall()
            if students:
                headers = ["학생ID", "이름", "과목명"]
                data = [[student["학생ID"], student["이름"], student["과목명"]] for student in students]
                table = self.create_table_widget(data, headers)
                dialog = QDialog(self)
                dialog.setWindowTitle("수강 학생 조회")
                layout = QVBoxLayout()
                layout.addWidget(table)
                dialog.setLayout(layout)
                dialog.exec()
            else:
                QMessageBox.information(self, "조회 결과", "수강 학생이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_professors(self):
        try:
            학과명, ok = QInputDialog.getText(self, "교수 목록 조회", "조회할 학과명을 입력하세요:")
            if ok and 학과명:
                query = "SELECT 교수ID, 교수명 FROM 학과별_교수목록 WHERE 학과명 = %s"
                cursor.execute(query, (학과명,))
                professors = cursor.fetchall()
                if professors:
                    headers = ["교수ID", "교수명"]
                    data = [[prof["교수ID"], prof["교수명"]] for prof in professors]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("교수 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 학과에 등록된 교수가 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_rooms(self):
        try:
            건물명, ok = QInputDialog.getText(self, "강의실 목록 조회", "조회할 건물명을 입력하세요:")
            if ok and 건물명:
                query = "SELECT 강의실ID, 호실명 FROM 강의실목록 WHERE 건물명 = %s"
                cursor.execute(query, (건물명,))
                rooms = cursor.fetchall()
                if rooms:
                    headers = ["강의실ID", "호실명"]
                    data = [[room["강의실ID"], room["호실명"]] for room in rooms]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("강의실 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 건물에 등록된 강의실이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_subjects(self):
        try:
            학과명, ok = QInputDialog.getText(self, "교과목 목록 조회", "조회할 학과명을 입력하세요:")
            if ok and 학과명:
                query = "SELECT 과목ID, 과목명 FROM 학과별_교과목목록 WHERE 학과명 = %s"
                cursor.execute(query, (학과명,))
                subjects = cursor.fetchall()
                if subjects:
                    headers = ["과목ID", "과목명"]
                    data = [[subj["과목ID"], subj["과목명"]] for subj in subjects]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("교과목 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 학과에 등록된 교과목이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_student_subjects(self):
        try:
            학과명, ok = QInputDialog.getText(self, "학생 교과목 조회", "조회할 학과명을 입력하세요:")
            if ok and 학과명:
                query = """
                SELECT s.학생ID, s.이름
                FROM 학생_2번 s
                JOIN 학과_2번 d ON s.소속학과ID = d.학과ID
                WHERE d.학과명 = %s
                """
                cursor.execute(query, (학과명,))
                students = cursor.fetchall()
                if students:
                    headers = ["학생ID", "이름"]
                    data = [[student["학생ID"], student["이름"]] for student in students]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("학생 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)

                    input_label = QLabel("학생 ID 입력:")
                    student_id_input = QLineEdit()
                    detail_button = QPushButton("상세 정보 조회")

                    layout.addWidget(input_label)
                    layout.addWidget(student_id_input)
                    layout.addWidget(detail_button)

                    def fetch_details():
                        student_id = student_id_input.text()
                        if student_id:
                            detail_query = "SELECT * FROM 학생별_신청과목목록 WHERE 학생ID = %s"
                            cursor.execute(detail_query, (student_id,))
                            subjects = cursor.fetchall()
                            if subjects:
                                headers = ["과목명", "교수명", "건물", "강의실", "요일", "시작교시", "종료교시"]
                                data = [
                                    [
                                        subj["과목명"],
                                        subj["교수명"],
                                        subj["건물명"],
                                        subj["호실명"],
                                        subj["요일"],
                                        subj["시작교시"],
                                        subj["종료교시"],
                                    ]
                                    for subj in subjects
                                ]
                                detail_table = self.create_table_widget(data, headers)
                                detail_dialog = QDialog(self)
                                detail_dialog.setWindowTitle("학생 상세 정보 조회")
                                detail_layout = QVBoxLayout()
                                detail_layout.addWidget(detail_table)
                                detail_dialog.setLayout(detail_layout)
                                detail_dialog.exec()
                            else:
                                QMessageBox.information(self, "조회 결과", "해당 학생의 신청된 과목이 없습니다.")
                        else:
                            QMessageBox.warning(self, "오류", "학생 ID를 입력하세요.")

                    detail_button.clicked.connect(fetch_details)

                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 학과의 학생이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")


    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃합니다.")
        self.close()

class 직원메뉴(QDialog):
    def __init__(self, 이름):
        super().__init__()
        self.이름 = 이름
        self.setWindowTitle(f"{이름}님 - 교무처 직원 메뉴")
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()

        self.title_label = QLabel(f"환영합니다, {이름}님!", self)
        self.layout.addWidget(self.title_label)

        # 버튼 정의
        self.view_students_button = QPushButton("학생 목록 조회", self)
        self.view_rooms_button = QPushButton("강의실 목록 조회", self)
        self.view_subjects_button = QPushButton("교과목 목록 조회", self)
        self.manage_courses_button = QPushButton("교과목 관리", self)
        self.manage_professors_button = QPushButton("교수 관리", self)
        self.manage_rooms_button = QPushButton("강의실 관리", self)
        self.logout_button = QPushButton("로그아웃", self)

        # 버튼 추가
        self.layout.addWidget(self.view_students_button)
        self.layout.addWidget(self.view_rooms_button)
        self.layout.addWidget(self.view_subjects_button)
        self.layout.addWidget(self.manage_courses_button)
        self.layout.addWidget(self.manage_professors_button)
        self.layout.addWidget(self.manage_rooms_button)
        self.layout.addWidget(self.logout_button)

        # 버튼 클릭 이벤트 연결
        self.view_students_button.clicked.connect(self.view_students)
        self.view_rooms_button.clicked.connect(self.view_rooms)
        self.view_subjects_button.clicked.connect(self.view_subjects)
        self.manage_courses_button.clicked.connect(self.manage_courses)
        self.manage_professors_button.clicked.connect(self.manage_professors)
        self.manage_rooms_button.clicked.connect(self.manage_rooms)  # 클래스 내부 메서드 호출
        self.logout_button.clicked.connect(self.logout)

        self.setLayout(self.layout)

    # 기존 create_table_widget 함수
    def create_table_widget(self, data, headers):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        table.resizeColumnsToContents()
        return table

    # 기존 create_table_with_controls 함수
    def create_table_with_controls(self, data, headers, inputs=None, on_add=None, on_edit=None, on_delete=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("관리 인터페이스")
        dialog.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        table.resizeColumnsToContents()

        layout.addWidget(table)

        input_fields = {}
        if inputs:
            for label_text, input_type in inputs.items():
                label = QLabel(label_text, dialog)
                layout.addWidget(label)
                if input_type == "text":
                    input_field = QLineEdit(dialog)
                elif input_type == "number":
                    input_field = QLineEdit(dialog)
                    input_field.setValidator(QIntValidator())
                input_fields[label_text] = input_field
                layout.addWidget(input_field)

        add_button = QPushButton("추가", dialog)
        edit_button = QPushButton("수정", dialog)
        delete_button = QPushButton("삭제", dialog)
        close_button = QPushButton("닫기", dialog)

        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addWidget(close_button)

        if on_add:
            add_button.clicked.connect(lambda: on_add(input_fields, table))
        if on_edit:
            edit_button.clicked.connect(lambda: on_edit(input_fields, table))
        if on_delete:
            delete_button.clicked.connect(lambda: on_delete(table))
        close_button.clicked.connect(dialog.close)

        dialog.setLayout(layout)
        return dialog, table, input_fields
    
    def view_students(self):
        try:
            query = "SELECT 학생ID, 이름 FROM 학생_2번"
            cursor.execute(query)
            students = cursor.fetchall()

            if students:
                headers = ["학생ID", "이름"]
                data = [[student["학생ID"], student["이름"]] for student in students]
                table = self.create_table_widget(data, headers)

                dialog = QDialog(self)
                dialog.setWindowTitle("학생 목록 조회")
                layout = QVBoxLayout()
                layout.addWidget(table)

                input_label = QLabel("학생 ID 입력:")
                student_id_input = QLineEdit()
                detail_button = QPushButton("상세 정보 조회")

                layout.addWidget(input_label)
                layout.addWidget(student_id_input)
                layout.addWidget(detail_button)

                def fetch_details():
                    student_id = student_id_input.text()
                    if student_id:
                        detail_query = "SELECT * FROM 학생별_신청과목목록 WHERE 학생ID = %s"
                        cursor.execute(detail_query, (student_id,))
                        subjects = cursor.fetchall()
                        if subjects:
                            headers = ["과목명", "교수명", "건물", "강의실", "요일", "시작교시", "종료교시"]
                            data = [
                                [
                                    subj["과목명"],
                                    subj["교수명"],
                                    subj["건물명"],
                                    subj["호실명"],
                                    subj["요일"],
                                    subj["시작교시"],
                                    subj["종료교시"],
                                ]
                                for subj in subjects
                            ]
                            detail_table = self.create_table_widget(data, headers)
                            detail_dialog = QDialog(self)
                            detail_dialog.setWindowTitle("학생 상세 정보 조회")
                            detail_layout = QVBoxLayout()
                            detail_layout.addWidget(detail_table)
                            detail_dialog.setLayout(detail_layout)
                            detail_dialog.exec()
                        else:
                            QMessageBox.information(self, "조회 결과", "해당 학생의 신청된 과목이 없습니다.")
                    else:
                        QMessageBox.warning(self, "오류", "학생 ID를 입력하세요.")

                detail_button.clicked.connect(fetch_details)

                dialog.setLayout(layout)
                dialog.exec()
            else:
                QMessageBox.information(self, "조회 결과", "학생 목록이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_rooms(self):
        try:
            건물명, ok = QInputDialog.getText(self, "강의실 목록 조회", "조회할 건물명을 입력하세요:")
            if ok and 건물명:
                query = "SELECT 강의실ID, 호실명 FROM 강의실목록 WHERE 건물명 = %s"
                cursor.execute(query, (건물명,))
                rooms = cursor.fetchall()
                if rooms:
                    headers = ["강의실ID", "호실명"]
                    data = [[room["강의실ID"], room["호실명"]] for room in rooms]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("강의실 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 건물에 등록된 강의실이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")

    def view_subjects(self):
        try:
            학과명, ok = QInputDialog.getText(self, "교과목 목록 조회", "조회할 학과명을 입력하세요:")
            if ok and 학과명:
                query = "SELECT 과목ID, 과목명 FROM 학과별_교과목목록 WHERE 학과명 = %s"
                cursor.execute(query, (학과명,))
                subjects = cursor.fetchall()
                if subjects:
                    headers = ["과목ID", "과목명"]
                    data = [[subj["과목ID"], subj["과목명"]] for subj in subjects]
                    table = self.create_table_widget(data, headers)
                    dialog = QDialog(self)
                    dialog.setWindowTitle("교과목 목록 조회")
                    layout = QVBoxLayout()
                    layout.addWidget(table)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "조회 결과", "해당 학과에 등록된 교과목이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"조회 실패: {str(e)}")
            
    def manage_professors(self):
        """
        교수 관리 로직
        """
        try:
            # 교수 데이터 조회 쿼리
            query = """
            SELECT 교수ID, 교수명, 교수_2번.소속학과ID, 학과_2번.학과명
            FROM 교수_2번
            JOIN 학과_2번 ON 교수_2번.소속학과ID = 학과_2번.학과ID
            """
            cursor.execute(query)
            professors = cursor.fetchall()

            # 테이블 헤더 정의
            headers = ["교수ID", "교수명", "소속학과ID", "학과명"]

            # 교수 추가 함수
            def add_professor(inputs, table):
                try:
                    교수명 = inputs["교수명"].text()
                    학과명 = inputs["소속학과명"].text()

                    if not (교수명 and 학과명):  # 모든 필드 입력 확인
                        QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
                        return

                    # 학과명을 기반으로 학과ID 조회, 존재하지 않으면 학과 추가
                    query = "SELECT 학과ID FROM 학과_2번 WHERE 학과명 = %s"
                    cursor.execute(query, (학과명,))
                    result = cursor.fetchone()

                    if not result:
                        # 학과가 존재하지 않으면 학과 추가
                        insert_query = "INSERT INTO 학과_2번 (학과명) VALUES (%s)"
                        cursor.execute(insert_query, (학과명,))
                        db.commit()

                        # 추가된 학과ID 다시 조회
                        cursor.execute(query, (학과명,))
                        result = cursor.fetchone()

                    소속학과ID = result["학과ID"]

                    # 교수 추가 쿼리 실행
                    query = "INSERT INTO 교수_2번 (교수명, 소속학과ID) VALUES (%s, %s)"
                    cursor.execute(query, (교수명, 소속학과ID))
                    db.commit()
                    QMessageBox.information(self, "성공", "교수가 추가되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"교수 추가 실패: {str(e)}")

            # 교수 수정 함수
            def edit_professor(inputs, table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:  # 선택된 행이 없을 때
                        QMessageBox.warning(self, "오류", "수정할 항목을 선택하세요.")
                        return

                    교수ID = table.item(selected_row, 0).text()
                    교수명 = inputs["교수명"].text()
                    학과명 = inputs["소속학과명"].text()

                    if not (교수명 and 학과명):  # 모든 필드 입력 확인
                        QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
                        return

                    # 학과명을 기반으로 학과ID 조회, 존재하지 않으면 학과 추가
                    query = "SELECT 학과ID FROM 학과_2번 WHERE 학과명 = %s"
                    cursor.execute(query, (학과명,))
                    result = cursor.fetchone()

                    if not result:
                        # 학과가 존재하지 않으면 학과 추가
                        insert_query = "INSERT INTO 학과_2번 (학과명) VALUES (%s)"
                        cursor.execute(insert_query, (학과명,))
                        db.commit()

                        # 추가된 학과ID 다시 조회
                        cursor.execute(query, (학과명,))
                        result = cursor.fetchone()

                    소속학과ID = result["학과ID"]

                    # 교수 수정 쿼리 실행
                    query = "UPDATE 교수_2번 SET 교수명 = %s, 소속학과ID = %s WHERE 교수ID = %s"
                    cursor.execute(query, (교수명, 소속학과ID, 교수ID))
                    db.commit()
                    QMessageBox.information(self, "성공", "교수가 수정되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"교수 수정 실패: {str(e)}")

            # 교수 삭제 함수
            def delete_professor(table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:  # 선택된 행이 없을 때
                        QMessageBox.warning(self, "오류", "삭제할 항목을 선택하세요.")
                        return

                    교수ID = table.item(selected_row, 0).text()

                    # 교수 삭제 쿼리 실행
                    query = "DELETE FROM 교수_2번 WHERE 교수ID = %s"
                    cursor.execute(query, (교수ID,))
                    db.commit()
                    QMessageBox.information(self, "성공", "교수가 삭제되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"교수 삭제 실패: {str(e)}")

            # 테이블 새로고침 함수
            def refresh_table():
                try:
                    cursor.execute(query)
                    updated_data = cursor.fetchall()
                    table.setRowCount(0)  # 기존 테이블 데이터 초기화
                    for row_idx, row_data in enumerate(updated_data):
                        table.insertRow(row_idx)
                        for col_idx, col_data in enumerate(row_data.values()):
                            table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"테이블 새로고침 실패: {str(e)}")

            # 관리 인터페이스 생성
            dialog, table, inputs = self.create_table_with_controls(
                data=[[prof[col] for col in headers] for prof in professors],
                headers=headers,
                inputs={
                    "교수명": "text",
                    "소속학과명": "text",  # 소속 학과명을 입력받도록 필드 변경
                },
                on_add=add_professor,
                on_edit=edit_professor,
                on_delete=delete_professor,
            )

            # 다이얼로그 실행
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"교수 관리 실행 실패: {str(e)}")

    def manage_courses(self):
        """
        교과목 관리 로직
        """
        try:
            # 교과목 데이터 조회 쿼리
            query = """
            SELECT c.과목ID, c.과목명, p.교수명, r.호실명 AS 강의실명, c.학점
            FROM 과목_2번 c
            JOIN 교수_2번 p ON c.교수ID = p.교수ID
            JOIN 강의실_2번 r ON c.강의실ID = r.강의실ID
            """
            cursor.execute(query)
            courses = cursor.fetchall()

            # 테이블 헤더 정의
            headers = ["과목ID", "과목명", "교수명", "강의실명", "학점"]

            def refresh_table():
                """
                Refresh the table with the latest data.
                """
                cursor.execute(query)
                updated_data = cursor.fetchall()
                table.setRowCount(0)
                for row_idx, row_data in enumerate(updated_data):
                    table.insertRow(row_idx)
                    for col_idx, col_data in enumerate(row_data.values()):
                        table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            def add_course(inputs, table):
                """
                교과목 추가 함수
                """
                try:
                    # 학과명을 입력받아 학과 확인
                    학과명, ok = QInputDialog.getText(self, "학과 입력", "과목을 등록할 학과명을 입력하세요:")
                    if not ok or not 학과명:
                        QMessageBox.warning(self, "오류", "학과명을 입력하세요.")
                        return

                    # 학과 확인 쿼리
                    query = "SELECT 학과ID FROM 학과_2번 WHERE 학과명 = %s"
                    cursor.execute(query, (학과명,))
                    학과 = cursor.fetchone()
                    if not 학과:
                        QMessageBox.warning(self, "오류", f"학과명 '{학과명}'이(가) 존재하지 않습니다.")
                        return

                    학과ID = 학과["학과ID"]

                    # 학과별 교수 목록 출력
                    query = "SELECT 교수ID, 교수명 FROM 교수_2번 WHERE 소속학과ID = %s"
                    cursor.execute(query, (학과ID,))
                    professors = cursor.fetchall()
                    if not professors:
                        QMessageBox.warning(self, "오류", f"학과 '{학과명}'에 등록된 교수가 없습니다.")
                        return

                    # 교수 선택 다이얼로그
                    교수ID = None  # 교수ID 초기화
                    professor_dialog = QDialog(self)
                    professor_dialog.setWindowTitle("교수 선택")
                    professor_layout = QVBoxLayout(professor_dialog)
                    professor_table = QTableWidget()
                    professor_table.setRowCount(len(professors))
                    professor_table.setColumnCount(2)
                    professor_table.setHorizontalHeaderLabels(["교수ID", "교수명"])
                    for row_idx, prof in enumerate(professors):
                        professor_table.setItem(row_idx, 0, QTableWidgetItem(str(prof["교수ID"])))
                        professor_table.setItem(row_idx, 1, QTableWidgetItem(prof["교수명"]))
                    professor_table.resizeColumnsToContents()
                    professor_layout.addWidget(professor_table)

                    select_professor_button = QPushButton("선택")
                    professor_layout.addWidget(select_professor_button)

                    def select_professor():
                        nonlocal 교수ID
                        selected_row = professor_table.currentRow()
                        if selected_row < 0:
                            QMessageBox.warning(self, "오류", "교수를 선택하세요.")
                            return
                        교수ID = professor_table.item(selected_row, 0).text()
                        professor_dialog.accept()

                    select_professor_button.clicked.connect(select_professor)
                    professor_dialog.exec()
                    if not 교수ID:
                        QMessageBox.warning(self, "오류", "교수를 선택하지 않았습니다.")
                        return

                    # 강의실 목록 출력
                    query = "SELECT 강의실ID, 호실명 FROM 강의실_2번"
                    cursor.execute(query)
                    rooms = cursor.fetchall()
                    if not rooms:
                        QMessageBox.warning(self, "오류", "등록된 강의실이 없습니다.")
                        return

                    # 강의실 선택 다이얼로그
                    강의실ID = None  # 강의실ID 초기화
                    room_dialog = QDialog(self)
                    room_dialog.setWindowTitle("강의실 선택")
                    room_layout = QVBoxLayout(room_dialog)
                    room_table = QTableWidget()
                    room_table.setRowCount(len(rooms))
                    room_table.setColumnCount(2)
                    room_table.setHorizontalHeaderLabels(["강의실ID", "호실명"])
                    for row_idx, room in enumerate(rooms):
                        room_table.setItem(row_idx, 0, QTableWidgetItem(str(room["강의실ID"])))
                        room_table.setItem(row_idx, 1, QTableWidgetItem(room["호실명"]))
                    room_table.resizeColumnsToContents()
                    room_layout.addWidget(room_table)

                    select_room_button = QPushButton("선택")
                    room_layout.addWidget(select_room_button)

                    def select_room():
                        nonlocal 강의실ID
                        selected_row = room_table.currentRow()
                        if selected_row < 0:
                            QMessageBox.warning(self, "오류", "강의실을 선택하세요.")
                            return
                        강의실ID = room_table.item(selected_row, 0).text()
                        room_dialog.accept()

                    select_room_button.clicked.connect(select_room)
                    room_dialog.exec()
                    if not 강의실ID:
                        QMessageBox.warning(self, "오류", "강의실을 선택하지 않았습니다.")
                        return

                    # 과목명과 학점을 입력받기
                    inputs, ok = QInputDialog.getText(
                        self,
                        "교과목 추가",
                        "추가할 과목명과 학점을 입력하세요 (쉼표로 구분): 과목명, 학점",
                    )
                    if not ok or not inputs:
                        QMessageBox.warning(self, "오류", "입력을 취소했습니다.")
                        return

                    try:
                        과목명, 학점 = [val.strip() for val in inputs.split(",")]
                        학점 = int(학점)
                    except ValueError:
                        QMessageBox.warning(self, "오류", "입력이 올바르지 않습니다. 쉼표로 구분하고 학점은 숫자로 입력하세요.")
                        return

                    # 교과목 추가 쿼리 실행
                    query = """
                    INSERT INTO 과목_2번 (과목명, 교수ID, 강의실ID, 학점)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (과목명, 교수ID, 강의실ID, 학점))
                    db.commit()
                    QMessageBox.information(self, "성공", "교과목이 추가되었습니다.")
                    refresh_table()  # 테이블 새로고침

                except Exception as e:
                    QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")

            def edit_course(inputs, table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:
                        QMessageBox.warning(self, "오류", "수정할 항목을 선택하세요.")
                        return

                    # 선택된 행에서 데이터 가져오기
                    과목ID = table.item(selected_row, 0).text()
                    기존_과목명 = table.item(selected_row, 1).text()
                    기존_학점 = table.item(selected_row, 4).text()

                    # 수정 양식 생성
                    dialog = QDialog(self)
                    dialog.setWindowTitle("교과목 수정")
                    dialog_layout = QVBoxLayout(dialog)

                    # 기존 데이터를 기본값으로 표시
                    과목명_label = QLabel("과목명:")
                    과목명_input = QLineEdit(기존_과목명)
                    학점_label = QLabel("학점:")
                    학점_input = QLineEdit(기존_학점)
                    학점_input.setValidator(QIntValidator())  # 학점은 숫자로 제한

                    save_button = QPushButton("저장")
                    cancel_button = QPushButton("취소")

                    dialog_layout.addWidget(과목명_label)
                    dialog_layout.addWidget(과목명_input)
                    dialog_layout.addWidget(학점_label)
                    dialog_layout.addWidget(학점_input)
                    dialog_layout.addWidget(save_button)
                    dialog_layout.addWidget(cancel_button)

                    dialog.setLayout(dialog_layout)

                    def save_changes():
                        과목명 = 과목명_input.text().strip()
                        학점 = 학점_input.text().strip()

                        if not (과목명 and 학점):  # 모든 필드가 입력되었는지 확인
                            QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
                            return

                        try:
                            학점 = int(학점)  # 학점을 정수로 변환
                        except ValueError:
                            QMessageBox.warning(self, "오류", "학점은 숫자로 입력해야 합니다.")
                            return

                        # 교과목 수정 쿼리 실행
                        query = """
                        UPDATE 과목_2번
                        SET 과목명 = %s, 학점 = %s
                        WHERE 과목ID = %s
                        """
                        cursor.execute(query, (과목명, 학점, 과목ID))
                        db.commit()
                        QMessageBox.information(self, "성공", "교과목이 수정되었습니다.")
                        refresh_table()  # 테이블 새로고침
                        dialog.close()

                    save_button.clicked.connect(save_changes)
                    cancel_button.clicked.connect(dialog.close)

                    dialog.exec()
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")



            def delete_course(table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:
                        QMessageBox.warning(self, "오류", "삭제할 항목을 선택하세요.")
                        return

                    과목ID = table.item(selected_row, 0).text()

                    query = "DELETE FROM 과목_2번 WHERE 과목ID = %s"
                    cursor.execute(query, (과목ID,))
                    db.commit()
                    QMessageBox.information(self, "성공", "교과목이 삭제되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")

            # 관리 인터페이스 생성
            dialog, table, inputs = self.create_table_with_controls(
                data=[[course[col] for col in headers] for course in courses],
                headers=headers,
                on_add=add_course,
                on_edit=edit_course,
                on_delete=delete_course,
            )

            # 다이얼로그 실행
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"교과목 관리 실행 실패: {str(e)}")


    def manage_rooms(self):
        """
        강의실 관리 로직
        """
        try:
            # 강의실 데이터 조회
            query = "SELECT 강의실ID, 호실명, 호실, 건물명 FROM 강의실_2번"
            cursor.execute(query)
            rooms = cursor.fetchall()

            # 테이블 헤더 정의
            headers = ["강의실ID", "호실명", "호실", "건물명"]

            # 강의실 추가 함수
            def add_room(inputs, table):
                try:
                    호실명 = inputs["호실명"].text()
                    호실 = inputs["호실"].text()
                    건물명 = inputs["건물명"].text()

                    if not (호실명 and 호실 and 건물명):  # 모든 필드 입력 확인
                        QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
                        return

                    # 강의실 추가 쿼리 실행
                    query = "INSERT INTO 강의실_2번 (호실명, 호실, 건물명) VALUES (%s, %s, %s)"
                    cursor.execute(query, (호실명, 호실, 건물명))
                    db.commit()
                    QMessageBox.information(self, "성공", "강의실이 추가되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"강의실 추가 실패: {str(e)}")

            # 강의실 수정 함수
            def edit_room(inputs, table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:  # 선택된 행이 없을 때
                        QMessageBox.warning(self, "오류", "수정할 항목을 선택하세요.")
                        return

                    강의실ID = table.item(selected_row, 0).text()
                    호실명 = inputs["호실명"].text()
                    호실 = inputs["호실"].text()
                    건물명 = inputs["건물명"].text()

                    if not (호실명 and 호실 and 건물명):  # 모든 필드 입력 확인
                        QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
                        return

                    # 강의실 수정 쿼리 실행
                    query = "UPDATE 강의실_2번 SET 호실명 = %s, 호실 = %s, 건물명 = %s WHERE 강의실ID = %s"
                    cursor.execute(query, (호실명, 호실, 건물명, 강의실ID))
                    db.commit()
                    QMessageBox.information(self, "성공", "강의실이 수정되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"강의실 수정 실패: {str(e)}")

            # 강의실 삭제 함수
            def delete_room(table):
                try:
                    selected_row = table.currentRow()
                    if selected_row < 0:  # 선택된 행이 없을 때
                        QMessageBox.warning(self, "오류", "삭제할 항목을 선택하세요.")
                        return

                    강의실ID = table.item(selected_row, 0).text()

                    # 강의실 삭제 쿼리 실행
                    query = "DELETE FROM 강의실_2번 WHERE 강의실ID = %s"
                    cursor.execute(query, (강의실ID,))
                    db.commit()
                    QMessageBox.information(self, "성공", "강의실이 삭제되었습니다.")
                    refresh_table()  # 테이블 새로고침
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"강의실 삭제 실패: {str(e)}")

            # 테이블 새로고침 함수
            def refresh_table():
                try:
                    cursor.execute(query)
                    updated_data = cursor.fetchall()
                    table.setRowCount(0)  # 기존 테이블 데이터 초기화
                    for row_idx, row_data in enumerate(updated_data):
                        table.insertRow(row_idx)
                        for col_idx, col_data in enumerate(row_data.values()):
                            table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"테이블 새로고침 실패: {str(e)}")

            # 관리 인터페이스 생성
            dialog, table, inputs = self.create_table_with_controls(
                data=[[room[col] for col in headers] for room in rooms],
                headers=headers,
                inputs={
                    "호실명": "text",
                    "호실": "text",  # 호실 입력 필드 추가
                    "건물명": "text",
                },
                on_add=add_room,
                on_edit=edit_room,
                on_delete=delete_room,
            )

            # 다이얼로그 실행
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"강의실 관리 실행 실패: {str(e)}")
            
    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃합니다.")
        self.close()


class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원가입")
        self.setGeometry(150, 150, 400, 300)
        self.layout = QVBoxLayout()

        self.user_type_label = QLabel("회원가입 유형을 선택하세요:", self)
        self.layout.addWidget(self.user_type_label)

        self.user_type_combo = QComboBox(self)
        self.user_type_combo.addItems(["학생", "교수", "교직원"])
        self.layout.addWidget(self.user_type_combo)

        self.signup_button = QPushButton("회원가입 진행", self)
        self.layout.addWidget(self.signup_button)
        self.signup_button.clicked.connect(self.handle_signup)

        self.setLayout(self.layout)

    def handle_signup(self):
        user_type = self.user_type_combo.currentText()

        if user_type == "학생":
            self.student_signup()
        elif user_type == "교수":
            self.professor_signup()
        elif user_type == "교직원":
            self.staff_signup()
        else:
            QMessageBox.warning(self, "오류", "올바른 사용자 유형을 선택하세요.")

    def fetch_departments(self):
        """
        Fetch a list of departments from the 학과_2번 table.
        Returns a list of tuples: [(학과ID, 학과명), ...].
        """
        try:
            query = "SELECT 학과ID, 학과명 FROM 학과_2번"
            cursor.execute(query)
            departments = cursor.fetchall()
            return [(dept["학과ID"], dept["학과명"]) for dept in departments]
        except Exception as e:
            QMessageBox.critical(self, "오류", f"학과 목록 조회 실패: {str(e)}")
            return []

    def student_signup(self):
        """
        Handle student signup by collecting student data and inserting it into the database.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("학생 회원가입")
        layout = QVBoxLayout(dialog)

        name_label = QLabel("이름:")
        name_input = QLineEdit()
        department_label = QLabel("소속 학과:")
        department_combo = QComboBox()

        # Fetch departments and populate the combo box
        departments = self.fetch_departments()
        for dept_id, dept_name in departments:
            department_combo.addItem(dept_name, userData=dept_id)

        username_label = QLabel("아이디:")
        username_input = QLineEdit()
        password_label = QLabel("비밀번호:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        submit_button = QPushButton("회원가입 완료")

        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(department_label)
        layout.addWidget(department_combo)
        layout.addWidget(username_label)
        layout.addWidget(username_input)
        layout.addWidget(password_label)
        layout.addWidget(password_input)
        layout.addWidget(submit_button)

        def submit():
            name = name_input.text()
            department_id = department_combo.currentData()  # Get the selected 학과ID
            username = username_input.text()
            password = password_input.text()

            if not (name and department_id and username and password):
                QMessageBox.warning(dialog, "오류", "모든 필드를 입력하세요.")
                return

            try:
                # Insert student into 학생_2번 table
                query = "INSERT INTO 학생_2번 (이름, 소속학과ID) VALUES (%s, %s)"
                cursor.execute(query, (name, department_id))
                student_id = cursor.lastrowid

                # Insert login info into 학생_로그인 table
                query = "INSERT INTO 학생_로그인 (학생ID, 아이디, 비밀번호) VALUES (%s, %s, %s)"
                cursor.execute(query, (student_id, username, password))
                db.commit()

                QMessageBox.information(dialog, "성공", f"학생 회원가입이 완료되었습니다. 학생ID: {student_id}")
                dialog.close()
            except Exception as e:
                QMessageBox.critical(dialog, "오류", f"학생 회원가입 실패: {str(e)}")

        submit_button.clicked.connect(submit)
        dialog.setLayout(layout)
        dialog.exec()

    def professor_signup(self):
        """
        Handle professor signup by collecting professor data and inserting it into the database.
        """
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("교수 회원가입")
            layout = QVBoxLayout(dialog)

            # 교수명 입력
            name_label = QLabel("교수명:")
            name_input = QLineEdit()

            # 학과 선택
            department_label = QLabel("소속 학과:")
            department_combo = QComboBox()

            # Fetch departments and populate the combo box
            query = "SELECT 학과ID, 학과명 FROM 학과_2번"
            cursor.execute(query)
            departments = cursor.fetchall()

            for dept in departments:
                department_combo.addItem(dept["학과명"], userData=dept["학과ID"])

            # 아이디 입력
            username_label = QLabel("아이디:")
            username_input = QLineEdit()

            # 비밀번호 입력
            password_label = QLabel("비밀번호:")
            password_input = QLineEdit()
            password_input.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 마스킹 처리

            # 회원가입 버튼
            submit_button = QPushButton("회원가입 완료")

            # Layout에 위젯 추가
            layout.addWidget(name_label)
            layout.addWidget(name_input)
            layout.addWidget(department_label)
            layout.addWidget(department_combo)
            layout.addWidget(username_label)
            layout.addWidget(username_input)
            layout.addWidget(password_label)
            layout.addWidget(password_input)
            layout.addWidget(submit_button)

            # 회원가입 완료 버튼 클릭 시 처리
            def submit():
                try:
                    name = name_input.text().strip()
                    department_id = department_combo.currentData()  # Get the selected 학과ID
                    username = username_input.text().strip()
                    password = password_input.text().strip()

                    if not (name and department_id and username and password):
                        QMessageBox.warning(dialog, "오류", "모든 필드를 입력하세요.")
                        return

                    # 중복 교수 확인
                    query = """
                    SELECT 교수ID FROM 교수_2번
                    WHERE 교수명 = %s AND 소속학과ID = %s
                    """
                    cursor.execute(query, (name, department_id))
                    existing_professor = cursor.fetchone()

                    if not existing_professor:
                        QMessageBox.warning(dialog, "오류", f"학과에 '{name}' 교수님이 등록되어 있지 않습니다.")
                        return

                    # 아이디 중복 확인
                    query = "SELECT 교수ID FROM 교수_로그인 WHERE 아이디 = %s"
                    cursor.execute(query, (username,))
                    if cursor.fetchone():
                        QMessageBox.warning(dialog, "오류", "해당 아이디는 이미 사용 중입니다.")
                        return

                    # 로그인 정보 등록
                    query = "INSERT INTO 교수_로그인 (교수ID, 아이디, 비밀번호) VALUES (%s, %s, %s)"
                    cursor.execute(query, (existing_professor["교수ID"], username, password))
                    db.commit()

                    QMessageBox.information(dialog, "성공", f"교수 회원가입이 완료되었습니다. 교수ID: {existing_professor['교수ID']}")
                    # 회원가입 성공 시 창 닫기
                    dialog.accept()

                except Exception as e:
                    QMessageBox.critical(dialog, "오류", f"회원가입 중 오류 발생: {str(e)}")
                    print(f"회원가입 오류: {str(e)}")  # 디버깅용 로그 출력

            submit_button.clicked.connect(submit)
            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "오류", f"회원가입 UI 생성 중 오류 발생: {str(e)}")
            print(f"회원가입 UI 오류: {str(e)}")  # 디버깅용 로그 출력

    def staff_signup(self):
        """
        Handle staff signup by collecting staff data and inserting it into the database.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("교직원 회원가입")
        layout = QVBoxLayout(dialog)

        name_label = QLabel("이름:")
        name_input = QLineEdit()

        username_label = QLabel("아이디:")
        username_input = QLineEdit()
        password_label = QLabel("비밀번호:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        submit_button = QPushButton("회원가입 완료")

        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(username_label)
        layout.addWidget(username_input)
        layout.addWidget(password_label)
        layout.addWidget(password_input)
        layout.addWidget(submit_button)

        def submit():
            name = name_input.text()
            username = username_input.text()
            password = password_input.text()

            if not (name and username and password):
                QMessageBox.warning(dialog, "오류", "모든 필드를 입력하세요.")
                return

            try:
                # Insert staff into 직원_2번 table
                query = "INSERT INTO 직원_2번 (이름) VALUES (%s)"
                cursor.execute(query, (name,))
                staff_id = cursor.lastrowid

                # Insert login info into 직원_로그인 table
                query = "INSERT INTO 직원_로그인 (직원ID, 아이디, 비밀번호) VALUES (%s, %s, %s)"
                cursor.execute(query, (staff_id, username, password))
                db.commit()

                QMessageBox.information(dialog, "성공", f"교직원 회원가입이 완료되었습니다. 직원ID: {staff_id}")
                dialog.close()
            except Exception as e:
                QMessageBox.critical(dialog, "오류", f"교직원 회원가입 실패: {str(e)}")

        submit_button.clicked.connect(submit)
        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
