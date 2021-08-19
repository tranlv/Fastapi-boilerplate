from pydantic import BaseModel


class SuccessMessageResponse(BaseModel):
    status: bool
    code: int = 200
    message: str
    data: dict


class ErrorMessageResponse(BaseModel):
    status: bool
    code: int
    message: str
    data: dict
