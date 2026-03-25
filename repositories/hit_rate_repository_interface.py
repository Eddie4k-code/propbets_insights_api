from abc import ABC, abstractmethod

class HitRateRepositoryInterface(ABC):
    """
    Interface for hit rate repository.
    """
    @abstractmethod
    def get_hit_rates_within_hours(self, hours: int) -> list:
        pass

    @abstractmethod
    def get_hot_props_within_hours(self, hours: int) -> list:
        pass
