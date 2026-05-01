class Ticket:
    def __init__(
        self,
        id_ticket=None,
        id_vehicle=None,
        entry_time=None,
        exit_time=None,
        total_price=None
    ):
        self.id_ticket = id_ticket
        self.id_vehicle = id_vehicle
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.total_price = total_price

    def is_open(self):
        return self.exit_time is None