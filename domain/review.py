import dbinfo

from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc

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

page_size = 5


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    place_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


def retrieve_reviews(reviews):
    if reviews:
        result = []

        for review in reviews:
            review_data = {
                "id": review.id,
                "userId": review.user_id,
                "content": review.content,
                "createdAt": format_datetime(review.created_at)
            }
            result.append(review_data)

        return get_success_schema(200, result)
    else:
        return get_error_schema(404, '리뷰가 존재하지 않습니다.')


def get_reviews_by_place(path_parameters, query_string_parameters):
    if not query_string_parameters:
        return get_error_schema(400, 'page를 보내주세요.')

    page = int(query_string_parameters['page'])

    reviews = session \
        .query(Review) \
        .filter_by(place_id=path_parameters["placeId"]) \
        .order_by(desc(Review.created_at)) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    return retrieve_reviews(reviews)


def get_my_reviews(path_parameters, query_string_parameters):
    if not query_string_parameters:
        return get_error_schema(400, 'page를 보내주세요.')

    page = int(query_string_parameters['page'])

    reviews = session \
        .query(Review) \
        .filter_by(user_id=path_parameters["userId"]) \
        .order_by(desc(Review.created_at)) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    return retrieve_reviews(reviews)


def create_review(path_parameters, request_body):
    review = Review(
        content=request_body['content'],
        user_id=path_parameters['userId'],
        place_id=path_parameters['placeId']
    )
    session.add(review)
    session.commit()

    result = {
        "id": review.id,
    }

    return get_success_schema(200, result)
