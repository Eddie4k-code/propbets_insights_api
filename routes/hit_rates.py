from fastapi import APIRouter, Query, Depends
from openai import BaseModel
import db
from db.postgres_db_connection import PostgresConnection
import os
from dotenv import load_dotenv
from exceptions.custom_exception import CustomException
import logging
from services.hit_rate_service_interface import HitRateServiceInterface
from services.hit_rate_service import HitRateService
from repositories.nba_pg_hit_rate_repository import NBAHitRateRepository
from slowapi import Limiter
from fastapi import Request
from llm.core import run_llm

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()


# Import the shared DB connection from main.py
from main import db

limiter = Limiter(key_func=lambda: "global")

def get_nba_hit_rate_service():

    nba_hit_rate_repository = NBAHitRateRepository(db_connection=db)

    return HitRateService(nba_repository=nba_hit_rate_repository)

@router.get("/api/protected/hitrates/latest/v1")
async def get_latest_hitrates(  
    request: Request,
    hit_rate_service: HitRateServiceInterface = Depends(get_nba_hit_rate_service),
    sport: str = Query("all", description="The sport for which to retrieve hit rates"),
    prop_type: str = Query(None, description="The type of prop to filter hit rates"),
    min_hit_rate_10: str = Query(None, description="The minimum hit rate for the last 10 games"),
    min_hit_rate_30: str = Query(None, description="The minimum hit rate for the last 30 games"),
    min_hit_rate_60: str = Query(None, description="The minimum hit rate for the last 60 games")
):
    """
    Endpoint to retrieve the latest hit rates for a specific sport.
    """

    try:
        if sport == "nba":
            hit_rates = hit_rate_service.get_nba_hit_rates_within_hours(
                24, prop_type, min_hit_rate_10, min_hit_rate_30, min_hit_rate_60
            )
        else:
            raise CustomException(f"Sport '{sport}' not supported.", status_code=400)
        return {"hit_rates": hit_rates}
    except CustomException as e:
        logger.error(f"Error Occured: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred. Please try again later."}
    

class Query(BaseModel):
    query: str


@router.post("/api/hit_rates/ai_chat_bot")
async def ai_chat_bot(request: Request, query: Query):
    """
    Endpoint to handle AI chatbot queries.
    """
    try:
        response = await run_llm(query.query)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing AI chatbot query: {e}")
        return {"response": "An error occurred while processing your request. Please try again later."}