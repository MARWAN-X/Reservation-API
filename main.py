from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Event, Seat, Reservation

app = FastAPI()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1️⃣ Get all events
@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    response = []

    for event in events:
        total_seats = db.query(Seat).filter(Seat.event_id == event.id).count()
        reserved_seats = (
            db.query(Seat)
            .filter(Seat.event_id == event.id, Seat.is_reserved == True)
            .count()
        )
        available_seats = total_seats - reserved_seats

        response.append(
            {
                "id": event.id,
                "name": event.name,
                "total_seats": total_seats,
                "available_seats": available_seats,
            }
        )

    return response


# 2️⃣ Get seating availability for an event
@app.get("/events/{event_id}/seats")
def get_seats(event_id: int, db: Session = Depends(get_db)):
    seats = db.query(Seat).filter(Seat.event_id == event_id).all()
    if not seats:
        raise HTTPException(status_code=404, detail="Event not found")
    return seats


# 3️⃣ Reserve a seat
@app.post("/events/{event_id}/reservations")
def reserve_seat(
    event_id: int, seat_number: str, user_name: str, db: Session = Depends(get_db)
):
    # Check if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if the seat exists
    seat = (
        db.query(Seat)
        .filter(Seat.event_id == event_id, Seat.seat_number == seat_number)
        .first()
    )
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")

    # Check if the seat is already reserved
    if seat.is_reserved:
        raise HTTPException(status_code=400, detail="Seat already reserved")

    try:
        # Reserve the seat
        seat.is_reserved = True
        db.commit()

        # Create the reservation
        reservation = Reservation(
            event_id=event_id, seat_id=seat.id, user_name=user_name
        )
        db.add(reservation)
        db.commit()
        return {
            "message": "Seat reserved successfully!",
            "reservation_id": reservation.id,
        }

    except Exception:
        db.rollback()  # Rollback any changes if an error occurs
        raise HTTPException(
            status_code=400, detail="An error occurred while reserving the seat"
        )


# 4️⃣ Cancel a reservation
@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    seat = db.query(Seat).filter(Seat.id == reservation.seat_id).first()
    seat.is_reserved = False

    db.delete(reservation)
    db.commit()

    return {"message": "Reservation canceled successfully!"}
