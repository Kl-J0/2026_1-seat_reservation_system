from seat_reservation_system.seat_store import SeatStore


def test_reserve_and_cancel_flow():
    store = SeatStore([1, 2])
    seat_id, name = store.reserve(1, "Alex")
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.status(1)
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.cancel(1, "Alex")
    assert (seat_id, name) == (1, None)


def test_stats_counts_reserved_and_available():
    store = SeatStore([1, 2, 3])
    store.reserve(2, "Mina")
    assert store.stats() == {"total": 3, "reserved": 1, "available": 2}

def test_cancel_all_by_name():
    from seat_reservation_system.seat_store import SeatStore
    import pytest

    store = SeatStore(["A1", "A2", "B1"])
    store.reserve("A1", "Kim")
    store.reserve("A2", "Kim")
    store.reserve("B1", "Lee")

    # Kim으로 예약된 모든 좌석 일괄 취소 검증
    canceled = store.cancel_all_by_name("Kim")
    assert "A1" in canceled
    assert "A2" in canceled
    assert len(canceled) == 2
    
    # 취소 후 상태 확인
    assert store.status("A1")[1] is None
    assert store.status("A2")[1] is None
    assert store.status("B1")[1] == "Lee"

    # 없는 이름 취소 시 에러 발생 검증
    with pytest.raises(ValueError):
        store.cancel_all_by_name("Choi")

def test_list_available_seats():
    from seat_reservation_system.seat_store import SeatStore
    
    store = SeatStore(["A1", "A2"])
    store.reserve("A1", "Kim")
    
    # 비어있는 좌석 목록 필터링 검증
    available = store.list_available_seats()
    assert len(available) == 1
    assert available[0][0] == "A2"
