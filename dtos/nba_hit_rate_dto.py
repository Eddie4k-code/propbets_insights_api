import dataclasses

@dataclasses.dataclass
class NBAHitRateDTO:
    player_name: str
    prop_type: str
    line: str
    event_start_time: str
    outcome_name: str
    price: int
    sportsbook: str
    market_last_update: str
    hit_rate_10_game: float
    hit_rate_30_game: float
    hit_rate_60_game: float