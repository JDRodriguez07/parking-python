from services.rate_service import RateService


class RateController:

    def __init__(self):
        self.service = RateService()

    def get_rate_by_vehicle_type(self, vehicle_type):
        return self.service.get_rate_by_vehicle_type(vehicle_type)

    def list_rates(self):
        return self.service.list_rates()