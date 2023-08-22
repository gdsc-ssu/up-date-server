from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dbinfo
from util.response import get_success_schema, get_error_schema

# MySQL 연결 정보 설정
db_url = f"mysql+pymysql://{dbinfo.db_username}:{dbinfo.db_password}@{dbinfo.db_host}:{dbinfo.db_port}/{dbinfo.db_name}"

# SQLAlchemy 엔진 생성
engine = create_engine(db_url)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# SQLAlchemy 모델 정의
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# 사용자 조회 함수

def get_user_by_id(path_parameters):
    user = session.query(User).filter_by(id=path_parameters["id"]).first()

    if user:
        result = {
            "id": user.id,
            "email": user.email
        }

        return get_success_schema(200, result)
    else:
        return get_error_schema(404, '존재하지 않는 유저입니다.')

if __name__ == "__main__":
    get_user_by_id({'id':'myggona'})
