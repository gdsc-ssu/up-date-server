# up-date-cli-server
업데이트 CLI 서버입니다. 다음은 람다 배포 방법입니다.

## 준비 사항
- 경로에 맞는 API Gateway가 설정되어 있어야 합니다.
- API Gateway는 HTTP로 구성하며, 경로는 Develop의 Route에서 추가하면 됩니다.

## 배포 단계

1. 프로젝트 디렉토리에서 다음 명령어를 실행하여 ZIP 파일을 생성합니다:

    ```bash
    zip -r up-date-cli-server.zip ./
    ```

    이 명령은 현재 디렉토리의 모든 파일 및 하위 디렉토리를 `up-date-cli-server.zip`으로 압축합니다.

2. 생성된 ZIP 파일을 Lambda 함수에 업로드합니다. 이 과정은 AWS Management Console에서 진행할 수 있습니다.

3. Lambda 함수가 완전히 업로드되었으면, API Gateway에서 해당 Lambda 함수와 연결합니다.

4. 업데이트 CLI 서버가 성공적으로 배포되면 해당 API 엔드포인트를 통해 업데이트 서비스를 이용할 수 있습니다.

## 모니터링
AWS CloudWatch의 /aws/lambda/update 로그그룹에서 로그를 확인할 수 있습니다.

**TODO: 공용 AWS 계정 만들어야 함**
