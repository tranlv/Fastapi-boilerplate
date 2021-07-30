from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.encoders import jsonable_encoder
from pprint import pprint


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # @TODO: refactor to inherit the jsonable_encoder
    json_serialized = dict()
    for error_wrapper in exc.raw_errors:
        for err in error_wrapper.exc.raw_errors:
            loc_tuple = err.loc_tuple()
            if isinstance(err.exc, ValueError):
                if len(err.exc.args) > 0:
                    message = err.exc.args[0]
                else:
                    message = err.exc
                if callable(message):
                    json_serialized[loc_tuple[-1]] = message()
                else:
                    json_serialized[loc_tuple[-1]] = str(message)
            else:
                json_serialized[loc_tuple[-1]] = str(err.exc)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": False,
            "code": HTTP_422_UNPROCESSABLE_ENTITY,
            "message": jsonable_encoder(json_serialized),
            "data": None
        },
    )


def send_result(data=None, message='OK', code=200, status=True):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code


def send_error(data=None, message='Failed', code=400, status=False):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code
