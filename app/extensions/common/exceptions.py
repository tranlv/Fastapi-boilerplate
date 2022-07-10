import traceback
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.encoders import jsonable_encoder

from fastapi import HTTPException


class AppException(HTTPException):
    status_code = 500
    label = "Internal Error"

    def __init__(self, errcode, message, data=None):
        self.message = message
        self.code = errcode
        self.data = data

        if isinstance(data, Exception):
            self.data = traceback.format_exc()

        # @TODO: logging goes here
        print(
            "AppException [%s-%s] %s\n"
            "---------------DEBUG DATA---------------\n"
            "%r\n"
            "----------------------------------------",
            self.status_code,
            self.code,
            self.message,
            self.data,
        )

    def __repr__(self):
        # This exception is meant to be handled by the
        # application error handler.
        return "[!!WRAPPED!!] " + self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "{label} [{c}] {m} => {d}".format(
            label=self.label, c=self.code, m=self.message, d=self.data
        )

    def response(self):
        JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": False,
                "code": HTTP_422_UNPROCESSABLE_ENTITY,
                "message": jsonable_encoder(self.message),
                "data": None
            },
        )


class SuccessResponse(JSONResponse):
    def response(self):
        JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": False,
                "code": HTTP_422_UNPROCESSABLE_ENTITY,
                "message": jsonable_encoder(self.message),
                "data": None
            },
        )


class NotFoundError(AppException):
    label = "Not Found"
    status_code = 404


class BadRequestError(AppException):
    label = "Bad Request"
    status_code = 400


class UnauthorizedError(AppException):
    label = "Unauthorized Request"
    status_code = 401


class ForbiddenError(AppException):
    label = "Forbidden"
    status_code = 403


class UnprocessableError(AppException):
    label = "Unprocessable Entity"
    status_code = 422


class LockedError(AppException):
    label = "Resource Locked"
    status_code = 423
