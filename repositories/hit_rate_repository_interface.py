from abc import ABC, abstractmethod

class HitRateRepositoryInterface(ABC):
    """
    Interface for hit rate repository.
    """
    @abstractmethod
    def get_all_hit_rates(self) -> float:
        pass

    def get_hit_rates_by_sport(self, sport: str) -> float:
        pass