import json

from domain.user import get_user_by_id, create_user
from domain.review import get_reviews_by_place, get_my_reviews, create_review

from util.response import get_error_schema


def lambda_handler(event, context):
    print(event)

    route_key = event['requestContext']['routeKey'].split()
    method, path = route_key[0], route_key[1]

    path_parameters = event.get('pathParameters')
    if path_parameters is None:
        path_parameters = None

    body = event.get('body')
    if body is None:
        body = None

    query_string_parameters = event.get('queryStringParameters')
    if query_string_parameters is None:
        query_string_parameters = None

    results = route(method, path, path_parameters, query_string_parameters, body)

    return json.dumps(results)


def route(method, path, path_parameters, query_string_parameters, body):
    if method == 'GET' and path == '/user/{id}':
        return get_user_by_id(path_parameters)
    elif method == 'POST' and path == '/user':
        return create_user(json.loads(body))
    elif method == 'GET' and path == '/review/place/{placeId}':
        return get_reviews_by_place(path_parameters, query_string_parameters)
    elif method == 'GET' and path == '/review/user/{userId}':
        return get_my_reviews(path_parameters, query_string_parameters)
    elif method == 'POST' and path == '/review/{userId}/{placeId}':
        return create_review(path_parameters, json.loads(body))

    else:
        return get_error_schema(500, '라우팅 정보를 찾지 못했습니다.')
