import dbinfo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc

from util.response import get_success_schema, get_error_schema
from util.datetime_util import format_datetime

from domain.entity import User, Place, Review, Station

# MySQL 연결 정보 설정
db_url = f"mysql+pymysql://{dbinfo.db_username}:{dbinfo.db_password}@{dbinfo.db_host}:{dbinfo.db_port}/{dbinfo.db_name}"

# SQLAlchemy 엔진 생성
engine = create_engine(db_url)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

page_size = 5


def retrieve_single_place(place_id):
    place = session \
        .query(
        Place,
        func.coalesce(func.avg(Review.star), 0).label("average_star"),
        func.coalesce(func.count(Review.id), 0).label("review_count")
    ) \
        .outerjoin(Review) \
        .filter(Place.id == place_id) \
        .first()

    return place


def retrieve_places(places):
    if places:
        result = []

        print(len(places))
        for place in places:
            place_data = {
                "id": place[0].id,
                "name": place[0].name,
                "phoneNumber": place[0].phone_number,
                "location": place[0].location,
                "start_time": str(place[0].start_at) if place[0].start_at else None,
                "end_time": str(place[0].end_at) if place[0].end_at else None,
                "latitude": place[0].latitude,
                "longitude": place[0].longitude,
                "menu": place[0].menu if place[0].menu else None,
                "url": place[0].url if place[0].url else None,
                "station": place[0].station,
                "averageStar": float(place[1]) if place[1] else 0,
                "reviewCount": int(place[2]) if place[2] else 0,
                "createdAt": format_datetime(place[0].created_at),
                "updatedAt": format_datetime(place[0].updated_at)
            }
            result.append(place_data)

        return get_success_schema(200, result)
    else:
        return get_error_schema(404, '장소가 존재하지 않습니다.')


def get_check_place(query_string_parameters):
    # TODO: 가게 이름으로 조회, 역 이름으로 조회 추가하기 -> query_string_parameters 에 추가해서 받으면 댐
    if not query_string_parameters:
        return get_error_schema(400, 'page를 보내주세요.')

    page = int(query_string_parameters['page'])

    order = query_string_parameters.get('order')

    # filter에 위도 경도 추가하기
    if order == 'REVIEW':  # 리뷰수순으로
        places = session \
            .query(
                Place,
                func.avg(Review.star).label("average_star"),
                func.count(Review.id).label("review_count")
            ) \
            .outerjoin(Review) \
            .group_by(Place.id) \
            .order_by(desc(func.count(Review.id)), desc(Place.created_at)) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
    elif order == 'STAR':  # 별점순으로
        places = session \
            .query(
                Place,
                func.avg(Review.star).label("average_star"),
                func.count(Review.id).label("review_count")
            ) \
            .outerjoin(Review) \
            .group_by(Place.id) \
            .order_by(desc(func.avg(Review.star)), desc(Place.created_at)) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
    else:  # 최신순으로
        places = session \
            .query(
                Place,
                func.avg(Review.star).label("average_star"),
                func.count(Review.id).label("review_count")
            ) \
            .outerjoin(Review) \
            .group_by(Place.id) \
            .order_by(desc(Place.created_at)) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()

    return retrieve_places(places)


def get_check_single_place(path_parameters):
    place_id = int(path_parameters['placeId'])

    place = retrieve_single_place(place_id)

    if place[0] is None:
        return get_error_schema(404, '해당 가게를 찾을 수 없습니다.')

    response_body = {
        "statusCode": 200,
        "body": {
            "id": place[0].id,
            "name": place[0].name,
            "phoneNumber": place[0].phone_number,
            "location": place[0].location,
            "start_time": str(place[0].start_at) if place[0].start_at else None,
            "end_time": str(place[0].end_at) if place[0].end_at else None,
            "latitude": place[0].latitude,
            "longitude": place[0].longitude,
            "menu": place[0].menu if place[0].menu else None,
            "url": place[0].url if place[0].url else None,
            "station": place[0].station,
            "averageStar": float(place[1]),
            "reviewCount": int(place[2]),
            "createdAt": format_datetime(place[0].created_at),
            "updatedAt": format_datetime(place[0].updated_at)
        }
    }

    return response_body


def create_place(path_parameters, request_body):
    # TODO: 가장 가까운 역 계산해서 station에 자동으로 넣어주기
    place = Place(
        name=request_body['name'],
        phone_number=request_body['phoneNumber'],
        location=request_body['location'],
        start_at=request_body['start_at'],
        end_at=request_body['end_at'],
        latitude=request_body['latitude'],
        longitude=request_body['longitude'],
        url=request_body['url'],
        menu=request_body['menu'],
        station="역 이름",
        user_id=path_parameters['userId']
    )
    session.add(place)
    session.commit()

    result = {
        "id": place.id,
    }

    return get_success_schema(200, result)

# TODO: 가게 수정하기
# PUT /places/{placeId}, 그냥 POST /place랑 body 똑같이 받아서 전부 업데이트 하기
