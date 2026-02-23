from .hit_rate_repository_interface import HitRateRepositoryInterface
from db.initiate_db_connection_interface import InitiateConnectionInterface
class PGHitRateRepository(HitRateRepositoryInterface):
    """
    PostgreSQL implementation of the HitRateRepositoryInterface.
    """
    def __init__(self, db_connection: InitiateConnectionInterface):
        self.db_connection = db_connection

    def get_all_hit_rates(self) -> float:
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