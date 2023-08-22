from util.trace import generate_random_string


def get_success_schema(status_code, body):
    trace_id = generate_random_string(32)
    print(trace_id)

    response = {
        "traceId": trace_id,
        "statusCode": status_code,
        "body": body
    }

    return response


def get_error_schema(status_code, reason):
    trace_id = generate_random_string(32)
    print(trace_id)

    response = {
        "traceId": trace_id,
        "statusCode": status_code,
        "body": {
            "error": reason

        }
    }

    return response
