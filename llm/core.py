import os
from typing import Any, Dict
from urllib import response
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from repositories.nba_pg_hit_rate_repository import NBAHitRateRepository
from db.connection import db
from db.postgres_db_connection import PostgresConnection
from repositories.player_stats_repository import PGPlayerStatsRepository
from langchain.memory import ConversationBufferMemory


load_dotenv()

model = init_chat_model(model="gpt-4-turbo", model_provider="openai")

@tool
def get_hit_rates(sport: str) -> Dict:
    """
    Tool to retrieve hit rates for a specific sport.
    """
    if sport.lower() == "nba":
        nba_hit_rate_repository = NBAHitRateRepository(db_connection=db)
        hit_rates = nba_hit_rate_repository.get_hit_rates_within_hours(hours=24)
        return {"hit_rates": hit_rates}
    
@tool
def get_player_stats(player_name: str, sport: str) -> Dict:
    """
    Tool to retrieve player stats for a specific player and sport.
    """
    player_stats_repository = PGPlayerStatsRepository(db_connection=db)
    stats = player_stats_repository.get_player_stats(player_name.lower(), sport)
    return {"player_stats": stats}

async def run_llm(query: str):
    system_prompt = (
        "You are a knowledgeable assistant specializing in sports prop bets, hit rates, and player stats. "
        "You ONLY support the following sports: nba, mlb, and nfl. "
        "When a user requests hit rates or prop bets for a specific sport, use the get_hit_rates tool with the correct sport as an argument, but only if the sport is nba, mlb, or nfl. "
        "When a user requests player stats for a specific player and sport, use the get_player_stats tool with the correct player name and sport as arguments, but only if the sport is nba, mlb, or nfl. "
        "If the user requests a sport other than nba, mlb, or nfl, clearly inform them that only nba, mlb, and nfl are supported. "
        "Always provide the following details for each prop bet: hit rate percentage, time frame of the data, and the price/odds of the prop. "
        "When giving game times or event times, always include every timezone. "
        "Respond in a concise, accurate, and user-friendly manner, ensuring all information is up-to-date and relevant. "
        "Always respond in plain text without any Markdown, code formatting, or unnecessary line breaks. Do not use \\n or special characters for formatting. Write your answers as clear, single-paragraph sentences suitable for direct display in a web UI."
    )

    agent = initialize_agent(
        tools=[get_hit_rates, get_player_stats],
        llm=model,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs={"system_message": system_prompt}
    )

    response = await agent.ainvoke({"input": query})
    return response['output']

# if __name__ == "__main__":
#     load_dotenv()
#     query = input()
#     run_llm(query)


