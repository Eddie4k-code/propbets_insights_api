from abc import ABC, abstractmethod

class HitRateServiceInterface(ABC):
    @abstractmethod
    def get_nba_hit_rates_within_hours(self, hours: int) -> list:
        pass
