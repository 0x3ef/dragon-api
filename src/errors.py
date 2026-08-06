from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class DragonException(Exception):
    """This is the base class for all Dragon errors"""
    pass


class ClassNotFound(DragonException):
    """Class Not found"""
    pass


class ClassAlreadyExists(DragonException):
    """Dragon class already exists in the db"""


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI) -> None:
    app.add_exception_handler(
        ClassNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Dragon class not found",
                "error_code": "class_not_found",
            },
        ),
    )

    app.add_exception_handler(
        ClassAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "A dragon class with this name already exists",
                "error_code": "class_already_exists"
                }
        ),
    )
