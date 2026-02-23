from abc import ABC, abstractmethod

class HitRateRepositoryInterface(ABC):
    @abstractmethod
    def get_all_hit_rates(self, url: str) -> float:
        pass

