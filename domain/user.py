import dbinfo

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from util.response import get_success_schema, get_error_schema
from util.datetime_util import format_datetime

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
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


def get_user_by_id(path_parameters):
    user = session.query(User).filter_by(id=path_parameters["id"]).first()

    if user:
        result = {
            "id": user.id,
            "created_at": format_datetime(user.created_at)
        }

        return get_success_schema(200, result)
    else:
        return get_error_schema(404, '존재하지 않는 유저입니다.')


def create_user(request_body):
    new_user = User(id=request_body['id'])
    session.add(new_user)
    session.commit()

    result = {
        "id": new_user.id,
        "createdAt": format_datetime(new_user.created_at)
    }

    return get_success_schema(200, result)
