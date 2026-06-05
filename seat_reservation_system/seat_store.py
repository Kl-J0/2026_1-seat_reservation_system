class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}

    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name and current != name:
            raise ValueError("Name does not match the reservation.")
        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        return seat_id, self._get(seat_id)

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]

    def cancel_all_by_name(self, name):
        """특정 이름으로 예약된 모든 좌석을 찾아 일괄 취소하는 신규 기능"""
        if not name:
            raise ValueError("Name must be provided for bulk cancellation.")
        
        canceled_seats = []
        for seat_id, reserved_name in list(self._seats.items()):
            if reserved_name == name:
                self._seats[seat_id] = None
                canceled_seats.append(seat_id)
        
        if not canceled_seats:
            raise ValueError(f"No reservations found for name: {name}")
        return canceled_seats

    def list_available_seats(self):
        """비어있는 좌석만 필터링해서 반환하는 신규 기능"""
        return [(seat_id, name) for seat_id, name in self._seats.items() if name is None]
