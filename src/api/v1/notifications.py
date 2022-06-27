from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from http import HTTPStatus


router = APIRouter()


@router.post('email/check')
async def check_email(
        payload,

):
    pass