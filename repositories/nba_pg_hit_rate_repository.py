from repositories.hit_rate_repository_interface import HitRateRepositoryInterface
from db.initiate_db_connection_interface import InitiateConnectionInterface


class NBAHitRateRepository(HitRateRepositoryInterface):
    def __init__(self, db_connection: InitiateConnectionInterface):
        self.db_connection = db_connection
    def get_hit_rates_within_hours(
            self, 
            hours: int,
            prop_type: str = None,
            min_hit_rate_10: str = None,
            min_hit_rate_30: str = None,
            min_hit_rate_60: str = None    
            ) -> list:

        interval_str = f"{hours} hours"
    
        query = f"""
        SELECT * FROM nba_hit_rate_snapshots
        WHERE event_start_time >= NOW()
        AND event_start_time <= (NOW() + INTERVAL '{interval_str}')
        """

        params = []

        if prop_type:
            query += " AND prop_type = %s"
            params.append(prop_type)
        if min_hit_rate_10:
            query += " AND hit_rate_10_game >= %s"
            params.append(min_hit_rate_10)
        if min_hit_rate_30:
            query += " AND hit_rate_30_game >= %s"
            params.append(min_hit_rate_30)
        if min_hit_rate_60:
            query += " AND hit_rate_60_game >= %s"
            params.append(min_hit_rate_60)

        query += " ORDER BY event_start_time DESC"

        print(query)
        
        return self.db_connection.execute_query(query, tuple(params))
    

    def get_hot_props_within_hours(self, hours: int) -> list:
        interval_str = f"{hours} hours"
        query = f"""
        SELECT * FROM nba_hit_rate_snapshots
        WHERE event_start_time >= NOW()
        AND event_start_time <= (NOW() + INTERVAL '{interval_str}')
        AND hit_rate_10_game >= 0.7
        ORDER BY event_start_time DESC
        """
        return self.db_connection.execute_query(query)
    