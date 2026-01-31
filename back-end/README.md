# Hotel Booking System - Django REST Framework + Web Interface

A simple yet complete hotel reservation system built with **Django** and **Django REST Framework**.  
This project provides:

- A full **REST API** for mobile/web clients  
- A basic **web interface** to browse hotels, rooms, and details  
- Admin panel for managing data  
- Automatic room availability update when a reservation is created  

## Features

- List, create, update, and delete Hotels, Rooms, and Reservations  
- API endpoints under `/api/` (powered by DRF ViewSets)  
- Simple HTML web views at root (e.g., list of hotels, room details)  
- When a new reservation is made via API → room `is_available` automatically becomes `False`  
- Fully functional Django Admin  
- Mock data ready for testing  

## Project Structure

```
.
├── db.sqlite3
├── hotel_booking
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── reservations
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── templates
    │   ├── 404.html
    │   ├── hotel_list.html
    │   ├── hotel_list_view.html
    │   ├── main.html
    │   ├── master.html
    │   ├── room_detail.html
    │   └── template.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Erfanm83/Practice-WebCourse
cd Practice-WebCourse
```

### 2. Create Virtual Environment (recommended)

```bash
python -m venv myworld
source myworld/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

**Pre-created superuser for testing:**

- Username: `testTA`  
- Password: `testTA1404@WebFum`

### 6. Add Mock Data

You can add sample data via:

- Django Admin (`/admin/`)
- Or run a custom seed command (if you created one earlier)
- Or manually via shell:

```bash
python manage.py shell
```

```python
from datetime import date
from reservations.models import Hotel, Room

# Example data
hotel = Hotel.objects.create(name="Grand Plaza", city="Tehran", address="Valiasr St", stars=5)

Room.objects.create(hotel=hotel, room_number=101, capacity=2, price_per_night=2500000)
Room.objects.create(hotel=hotel, room_number=102, capacity=4, price_per_night=4200000)
```

### 7. Run the Server

```bash
python manage.py runserver
```

## Access the Application

| URL                        | Description                                      |
|----------------------------|--------------------------------------------------|
| `http://127.0.0.1:8000/`   | Main homepage (web)                              |
| `http://127.0.0.1:8000/hotels/` | List of all hotels (HTML view)              |
| `http://127.0.0.1:8000/hotels/1/` | Rooms in a specific hotel                 |
| `http://127.0.0.1:8000/rooms/1/` | Room detail page                           |
| `http://127.0.0.1:8000/admin/` | Django Admin (login with superuser)         |
| `http://127.0.0.1:8000/api/hotels/` | API: List hotels (JSON)                   |
| `http://127.0.0.1:8000/api/rooms/` | API: List/create rooms                     |
| `http://127.0.0.1:8000/api/reservations/` | API: List/create reservations       |

## API Endpoints (REST)

All API endpoints are under `/api/`

| Method | Endpoint                     | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | `/api/hotels/`               | List all hotels                    |
| GET    | `/api/hotels/1/`             | Retrieve single hotel              |
| GET    | `/api/rooms/`                | List all rooms                     |
| POST   | `/api/rooms/`                | Create new room                    |
| GET    | `/api/reservations/`         | List all reservations              |
| POST   | `/api/reservations/`         | Create new reservation (room becomes unavailable) |

### Example: Create a Reservation (POST)

```json
POST http://127.0.0.1:8000/api/reservations/
Content-Type: application/json

{
  "customer_name": "علی رضایی",
  "phone_number": "09123456789",
  "check_in": "2026-01-10",
  "check_out": "2026-01-15",
  "room": 1
}
```

→ After success: the selected room's `is_available` becomes `False`

## Testing with Postman

1. GET → `http://127.0.0.1:8000/api/hotels/`
2. POST → `http://127.0.0.1:8000/api/rooms/` (add new room)
3. POST → `http://127.0.0.1:8000/api/reservations/` (book a room)

## Future Improvements (Optional)

- Add authentication (Token/JWT) for API  
- Filter available rooms only (`?is_available=true`)  
- Search hotels by city/name  
- Reservation cancellation (re-enable room)  
- Date conflict validation (prevent overlapping reservations)  
- Swagger/OpenAPI documentation (using drf-spectacular)  
- Frontend with React/Vue for better web UI  

## Contributing

Feel free to fork and submit pull requests!  
Issues and feature requests are welcome.

---

**Built with ❤️ using Django & Django REST Framework**  
January 2026

Happy coding! 🚀