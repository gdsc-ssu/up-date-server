import dbinfo

from sqlalchemy import create_engine, Column, String, DateTime, Integer,Time,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, desc
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


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(16), nullable=False)
    old_address = Column(String(255))
    new_address = Column(String(255), nullable=False)
    start_at = Column(Time)
    end_at = Column(Time)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    url = Column(String(2048))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    user_id = Column(String(255), nullable=False)

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    place_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


def retrieve_places(places):
    if places:
        result = []

        for place in places:
            place_data = {
                "id": place.id,
                "name": place.name,
                "phoneNumber": place.phone_number,
                "oldAddress": place.old_address,
                "newAddress": place.new_address,
                "start_at": place.start_at,
                "end_at": place.end_at,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "url": place.url,
                "createdAt": format_datetime(place.created_at)
            }
            result.append(place_data)

        return get_success_schema(200, result)
    else:
        return get_error_schema(404, '장소가 존재하지 않습니다.')


def create_place(path_parameters, request_body):
    place = Place(
        name=request_body['name'],
        phone_number=request_body['phoneNumber'],
        old_address=request_body.get('oldAddress'),
        new_address=request_body['newAddress'],
        start_at=request_body.get('start_at'),
        end_at=request_body.get('end_at'),
        latitude=request_body['latitude'],
        longitude=request_body['longitude'],
        url=request_body.get('url'),
        user_id=path_parameters['userId']
    )
    session.add(place)
    session.commit()

    result = {
        "id": place.id,
    }

    return get_success_schema(200, result)


def get_check_place(path_parameters, query_string_parameters):
    if not query_string_parameters:
        return get_error_schema(400, 'page를 보내주세요.')

    page = int(query_string_parameters['page'])
    order_by = query_string_parameters['order']

    if 'REVIEW' in order_by: #리뷰수순으로
        places = session \
            .query(Place) \
            .outerjoin(Review) \
            .group_by(Place.id) \
            .order_by(desc(func.count(Review.id))) \
            .offset((page - 1) * 5) \
            .limit(5) \
            .all()
    else: #생성일기준으로 장소 조회
        places = session \
            .query(Place) \
            .order_by(desc(Place.created_at)) \
            .offset((page - 1) * 5) \
            .limit(5) \
            .all()

    return retrieve_places(places)


def get_check_single_place(path_parameters, query_string_parameters):
    if not query_string_parameters:
        return get_error_schema(400, 'page를 보내주세요.')

    page = int(query_string_parameters['page'])
    place_id = int(path_parameters['placeId'])

    place = retrieve_single_place(place_id)

    if place is None:
        return get_error_schema(404, '해당 가게를 찾을 수 없습니다.')

    response_body = {
        "statusCode": 200,
        "body": {
            "id": place.id,
            "name": place.name,
            "phoneNumber": place.phone_number,
            "oldAddress": place.old_address,
            "newAddress": place.new_address,
            "start_at": place.start_at,
            "end_at": place.end_at,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "url": place.url,
            "reviewCounts": place.review_counts,
        }
    }

    return response_body


def retrieve_single_place(place_id):
    place = session.query(Place).filter_by(id=place_id).first()
    return place
