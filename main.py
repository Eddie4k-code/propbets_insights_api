from fastapi import FastAPI
from routes.hit_rates import router as hit_rates_router
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from db.postgres_db_connection import PostgresConnection
import os

app = FastAPI()
app.state.limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(hit_rates_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
