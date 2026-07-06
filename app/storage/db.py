from uuid import uuid4
from datetime import datetime

# user_id -> list of bookings
bookings: dict[int, list[dict]] = {}


def add_booking(user_id: int, guests: int, date: str, time: str) -> str:
    booking_id = str(uuid4())[:8].upper()
    bookings.setdefault(user_id, []).append({
        "id": booking_id,
        "guests": guests,
        "date": date,
        "time": time,
        "status": "pending",
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    })
    return booking_id


def get_user_bookings(user_id: int) -> list[dict]:
    return bookings.get(user_id, [])


def cancel_booking(user_id: int, booking_id: str) -> bool:
    for booking in bookings.get(user_id, []):
        if booking["id"] == booking_id and booking["status"] != "cancelled":
            booking["status"] = "cancelled"
            return True
    return False
