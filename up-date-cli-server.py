import boto3
import random
import string
import json

ddb = boto3.resource('dynamodb')
table = ddb.Table('Login')  # Replace 'YOUR_DYNAMODB_TABLE_NAME' with your actual table name

fleet = [
    {
        'Name': 'Bucephalus',
        'Password': 'password1',
        'Gender': 'Male',
    },
    {
        'Name': 'Shadowfax',
        'Password': 'password2',
        'Gender': 'Male',
    },
    {
        'Name': 'Rocinante',
        'Password': 'password3',
        'Gender': 'Female',
    },
]

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def authenticate_user(username, password):
    # 사용자 인증 로직 구현
    # 필요한 경우 데이터베이스나 인증 서비스와 통신하여 인증 수행
    # 예시로 간단하게 사용자 목록(fleet)에서 인증 수행
    for user in fleet:
        if user['Name'] == username and user['Password'] == password:
            return True
    return False

def generate_access_token(username):
    # 액세스 토큰 생성 로직 구현
    # 예시로 간단하게 랜덤 문자열 생성하여 사용자 이름과 함께 반환
    access_token = generate_random_string(16)
    return f"{username}:{access_token}"

def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': 'Invalid request body',
        }

    # 사용자가 제공한 인증 정보 가져오기
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']

    # 인증 정보 확인 및 사용자 인증
    authenticated = authenticate_user(username, password)

    if authenticated:
        # 로그인 성공 시 응답 바디 생성
        access_token = generate_access_token(username)
        response_body = {
            'message': '로그인 성공',
            'access_token': access_token
        }
        response = {
            'statusCode': 200,
            'body': json.dumps(response_body, ensure_ascii=False)
        }
    else:
        # 로그인 실패 시 응답 바디 생성
        response_body = {
            'message': '로그인 실패'
        }
        response = {
            'statusCode': 401,
            'body': json.dumps(response_body, ensure_ascii=False)
        }

    return response
