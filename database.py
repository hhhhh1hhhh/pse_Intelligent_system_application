from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from config import Config
from sqlalchemy.orm import sessionmaker


def get_db_connection():
    # MySQL 데이터베이스 연결 정보를 URL 형식으로 작성
    db_url = f"mysql://{Config.DB_USER}:{Config.DB_PW}@{Config.DB_HOST}:3306/question"

    # create_engine 함수로 데이터베이스에 연결
    engine = create_engine(db_url)

    # 세션 팩토리 생성
    Session = sessionmaker(bind=engine)

    # 세션 생성
    session = Session()

    # 연결 테스트
    try:
        session.execute(text("SELECT 1"))
        print("MySQL database connected")
    except OperationalError:
        print("MySQL database not connected")

    return session
