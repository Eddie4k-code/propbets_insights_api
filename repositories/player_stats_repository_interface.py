from abc import ABC, abstractmethod

class PGPlayerStatsRepositoryInterface(ABC):
    @abstractmethod
    def get_player_stats(self, player_name: str, sport: str) -> dict:
        pass