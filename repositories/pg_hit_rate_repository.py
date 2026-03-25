from exceptions.hit_rate_not_found import HitRateNotFoundException

from .hit_rate_repository_interface import HitRateRepositoryInterface
from db.initiate_db_connection_interface import InitiateConnectionInterface
class PGHitRateRepository(HitRateRepositoryInterface):
    """
    PostgreSQL implementation of the HitRateRepositoryInterface.
    """
    def __init__(self, db_connection: InitiateConnectionInterface):
        self.db_connection = db_connection

    def get_all_hit_rates(self) -> list:
        """
        Fetches all hit rate snapshots from the PostgreSQL database.
        """
        query = "SELECT * from hit_rate_snapshots"
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        if result:
            return result
        else:
            return None
        
    def get_hit_rates_by_sport(self, sport: str) -> list:
        """
        Fetches hit rate snapshots for a specific sport from the PostgreSQL database.
        """
        query = "SELECT * FROM hit_rate_snapshots WHERE sport_key = %s"
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(query, (sport,))
            result = cursor.fetchall()

        if result == None or len(result) == 0:
            raise HitRateNotFoundException()
        else:
            return result