from database import SessionLocal, Event, Seat

db = SessionLocal()

# Clear existing data (optional)
db.query(Seat).delete()
db.query(Event).delete()
db.commit()

# Create multiple events
events = [
    Event(name="Avengers Movie", total_seats=10),
    Event(name="Spider-Man Show", total_seats=8),
    Event(name="Fast & Furious", total_seats=12),
]

for event in events:
    db.add(event)
db.commit()

# Add seats for each event
for event in db.query(Event).all():
    for i in range(1, event.total_seats + 1):
        seat = Seat(event_id=event.id, seat_number=f"A{i}")
        db.add(seat)

db.commit()
db.close()

print("Database initialized with multiple events!")
