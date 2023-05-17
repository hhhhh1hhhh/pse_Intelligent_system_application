import os
import subprocess
from flask import Flask, render_template, request
from database.database import get_db_connection
from app.gpt_api import get_feedback
from database.models import QList


app = Flask(__name__, static_folder="app/static")
app.template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app", "templates"
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/test_list")
def test_list():
    # 데이터베이스 연결
    conn = get_db_connection()

    # 데이터베이스에서 데이터 가져오기
    q_list = conn.query(QList.q_id, QList.q_name).all()

    # 가져온 데이터를 html 파일에 전달하기
    return render_template("test_list.html", q_list=q_list)


code = ""


@app.route("/submit", methods=["POST"])
def submit():
    global code
    code = request.form.get("code")

    file = open("user_code.c", "w")
    file.write(code)
    file.close()

    # 컴파일 명령어
    compile_command = "gcc -o executable user_code.c"

    # 컴파일 실행
    result = subprocess.run(
        compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    # 컴파일 결과에 따라서 결과 출력
    if result.returncode == 0:
        output = subprocess.run(
            "./executable", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output_str = output.stdout.decode("utf-8")
    else:
        output_str = result.stderr.decode("utf-8")

    os.remove("user_code.c")  # user_code.c 파일 삭제
    os.remove("executable")  # executable 파일 삭제

    return output_str


@app.route("/answer")
def answer():
    answer = '#include <stdio.h>\n\nint main()\n{\n    printf("Hello, world!\\n");\n\n    return 0;\n}'
    return answer


@app.route("/feedback")
def feedback():
    feedback = get_feedback(code)
    return feedback


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/question")
def question():
    return render_template("question.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port="5000", debug=True)
