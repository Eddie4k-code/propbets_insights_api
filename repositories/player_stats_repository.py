from repositories.player_stats_repository_interface import PGPlayerStatsRepositoryInterface

class PGPlayerStatsRepository(PGPlayerStatsRepositoryInterface):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_player_stats(self, player_name: str, sport: str) -> list:
        """Fetch player stats for a given player and sport."""
        query = """
            SELECT *
            FROM player_game_stats
            INNER JOIN player_snapshots 
              ON player_snapshots.player_id = player_game_stats.player_id
            WHERE player_game_stats.sport_key = %s
              AND CONCAT(player_snapshots.first_name, ' ', player_snapshots.last_name) = %s;
        """
        
        return self.db_connection.execute_query(query, (sport, player_name))
