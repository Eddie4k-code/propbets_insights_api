from services.hit_rate_service_interface import HitRateServiceInterface
from repositories.hit_rate_repository_interface import HitRateRepositoryInterface


class HitRateService(HitRateServiceInterface):
    def __init__(self, nba_repository: HitRateRepositoryInterface):
        self.nba_repository = nba_repository

    def get_nba_hit_rates_within_hours(
        self, 
        hours: int,
        prop_type: str = None,
        min_hit_rate_10: str = None,
        min_hit_rate_30: str = None,
        min_hit_rate_60: str = None
        ) -> list:
        hit_rates = self.nba_repository.get_hit_rates_within_hours(
            hours, prop_type, min_hit_rate_10, min_hit_rate_30, min_hit_rate_60
        )

        hit_rates_list = []

        for hit_rate in hit_rates:
            hit_rates_list.append({
                "player_name": hit_rate[0],
                "prop_type": hit_rate[1],
                "line": hit_rate[2],
                "event_start_time": hit_rate[3],
                "outcome_name": hit_rate[4],
                "price": hit_rate[5],
                "sportsbook": hit_rate[6],
                "market_last_update": hit_rate[7],
                "hit_rate_10_game": hit_rate[8],
                "hit_rate_30_game": hit_rate[9],
                "hit_rate_60_game": hit_rate[10],
                "sport": hit_rate[11],
                "edge": hit_rate[12],
                "tier": hit_rate[13],
                "recently_hot": hit_rate[14]
            })
        return hit_rates_list