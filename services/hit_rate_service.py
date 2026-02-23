from services.hit_rate_service_interface import HitRateServiceInterface
from repositories.hit_rate_repository_interface import HitRateRepositoryInterface


class HitRateService(HitRateServiceInterface):
    def __init__(self, repository: HitRateRepositoryInterface):
        self.repository = repository

    def get_all_hit_rates(self):
        return self.repository.get_all_hit_rates()