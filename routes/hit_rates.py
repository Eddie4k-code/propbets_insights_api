from fastapi import APIRouter, Query, Depends
import db
from repositories.pg_hit_rate_repository import PGHitRateRepository
from db.postgres_db_connection import PostgresConnection
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def get_hit_rate_repository():
    db = PostgresConnection(connection_string=os.getenv("DATABASE_URL"))
    db.initiate_connection()
    return PGHitRateRepository(db_connection=db)

@router.get("/api/hitrates/latest/v1")
async def get_latest_hitrates(
    repo: PGHitRateRepository = Depends(get_hit_rate_repository)
):
    """
    Endpoint to retrieve the latest hit rates for a specific sport.
    """
    hit_rate = repo.get_all_hit_rates()
    if hit_rate is None:
        return {"error": "No hit rate data found"}
    return {"hit_rates": hit_rate}