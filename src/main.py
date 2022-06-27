# import json
import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core import settings as s
from core.logger import LOGGING
from api.v1 import notifications


app = FastAPI(
    title=s.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(notifications.router,
                   prefix='/api/v1/notifications',
                   tags=['notifications'])


if __name__ == '__main__':
    uvicorn.config.LOGGING_CONFIG
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG if s.DEBUG else logging.INFO
    )
