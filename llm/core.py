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
import db
from db.postgres_db_connection import PostgresConnection

load_dotenv()


# Initialize the DB connection once at module load
db_connection = PostgresConnection(connection_string=os.getenv("DATABASE_URL"))
db_connection.initiate_connection()

model = init_chat_model(model="gpt-4-turbo", model_provider="openai")


@tool
def get_hit_rates(sport: str) -> Dict:
    """
    Tool to retrieve hit rates for a specific sport.
    """
    if sport.lower() == "nba":
        nba_hit_rate_repository = NBAHitRateRepository(db_connection=db_connection)
        hit_rates = nba_hit_rate_repository.get_hit_rates_within_hours(hours=24)
        return {"hit_rates": hit_rates}

async def run_llm(query: str):
    system_prompt = (
        "You are a knowledgeable assistant specializing in sports prop bets and hit rates. "
        "When a user requests hit rates or prop bets for a specific sport, use the get_hit_rates tool with the correct sport as an argument. "
        "Always provide the following details for each prop bet: hit rate percentage, time frame of the data, and the price/odds of the prop. "
        "When giving game times or event times, always include every timezone. "
        "If the requested sport is not supported, clearly inform the user which sports are available. "
        "Respond in a concise, accurate, and user-friendly manner, ensuring all information is up-to-date and relevant. "
        "Always respond in plain text without any Markdown, code formatting, or unnecessary line breaks. Do not use \\n or special characters for formatting. Write your answers as clear, single-paragraph sentences suitable for direct display in a web UI."
    )

    agent = initialize_agent(
        tools=[get_hit_rates],
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


