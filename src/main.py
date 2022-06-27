import logging

import asyncpg
import backoff
import pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notifications
from core import dependencies
from core import settings as s
from core.backoff import backoff_hdlr, backoff_hdlr_success
from core.logger import LOGGING

app = FastAPI(
    title=s.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    # dependencies.queque = backoff.on_exception(
    #     wait_gen=backoff.expo,
    #     max_tries=s.BACKOFF_RETRIES,
    #     max_time=s.BACKOFF_MAX_TIME,
    #     exception=Exception,
    #     on_backoff=backoff_hdlr,
    #     on_success=backoff_hdlr_success,
    # )(pika.BlockingConnection)(pika.ConnectionParameters(host=s.RABBIT_HOST))

    dependencies.pool = await backoff.on_exception(
        wait_gen=backoff.expo,
        max_tries=s.BACKOFF_RETRIES,
        max_time=s.BACKOFF_MAX_TIME,
        exception=Exception,
        on_backoff=backoff_hdlr,
        on_success=backoff_hdlr_success,
    )(asyncpg.create_pool)(dsn=s.DB_DSN)


@app.on_event('shutdown')
async def shutdown():
    dependencies.pool.close()
    dependencies.queque.close()


app.include_router(notifications.router,
                   prefix='/api/v1/notifications',
                   tags=['notifications'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG if s.DEBUG else logging.INFO
    )
