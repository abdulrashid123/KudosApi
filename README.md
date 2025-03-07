# Kudos API

## Setup Instructions

Follow the steps below to set up and run the Kudos API.

### Prerequisites
- Python 3.7+
- Django
- db.sqlite3

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KudosApi
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Migration
Run the following command to apply migrations:
```bash
python manage.py migrate
```

### Running the Server
Start the Django development server:
```bash
python manage.py runserver
```

### Loading Dummy Data
To populate the database with dummy data, run the fixture script:
```bash
python fixture.py
```

### Resetting Kudos Data
To reset the Kudos data, run the reset script you can use crontab to schedule it every week:
```bash
python reset.py
```

### API Endpoints
For API details, refer to the API documentation or use tools like Postman to test the endpoints.

---

Now your Kudos API is set up and running!

