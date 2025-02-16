import threading
import requests

API_URL = "http://127.0.0.1:8000"


def reserve():
    response = requests.post(
        f"{API_URL}/events/1/reservations?seat_number=A1&user_name=John"
    )
    print(response.json())


# Run multiple threads to simulate concurrent bookings
threads = []
for _ in range(5):  # Simulating 5 users booking the same seat
    t = threading.Thread(target=reserve)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
