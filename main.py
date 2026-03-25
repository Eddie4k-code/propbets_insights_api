from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from routes.hit_rates import router as hit_rates_router
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from db.postgres_db_connection import PostgresConnection
import os
from exceptions.custom_exception import CustomException
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combined authentication and error handling middleware
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

@app.middleware("http")
async def auth_and_error_middleware(request: Request, call_next):
    try:
        if request.method == "OPTIONS":
            return await call_next(request)

        # Only protect routes that need authentication
        if request.url.path.startswith("/api/protected"):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="No Bearer Token")
            token = auth_header.split("Bearer ")[1]
          
            user = supabase.auth.get_user(token)

            logging.info(f"Authenticated user: {user}")

            if not user or not user.user:
                raise HTTPException(status_code=401, detail="Not Authorized")
            
            request.state.user = user.user

            return await call_next(request)
        
        else:
            return await call_next(request)
        
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
app.state.limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(hit_rates_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
