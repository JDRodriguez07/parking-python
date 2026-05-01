from repositories.rate_repository import RateRepository


class RateService:

    def __init__(self):
        self.repo = RateRepository()

    def get_rate_by_vehicle_type(self, vehicle_type):
        return self.repo.get_by_vehicle_type(vehicle_type)

    def list_rates(self):
        return self.repo.get_all()