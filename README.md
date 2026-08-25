# URL Shortener API

A backend URL Shortener API built with **FastAPI**, **MySQL**, **SQLAlchemy**, **Redis**, and **JWT Authentication**.

The application allows both guest and registered users to create shortened URLs. Registered users can authenticate using JWT tokens, while Redis is used for rate limiting and controlling guest usage.

The project also includes a comprehensive automated test suite using **Pytest**.

---

# 🚀 Features

## 🔗 URL Shortening

- Convert a long URL into a unique short URL.
- Automatically generate a **6-character short code**.
- Check for short-code collisions before saving.
- Store the original URL and generated short code in MySQL.
- Generate a SHA-256 hash of the original URL.

### Workflow

```text
Original URL
     │
     ▼
Validate URL
     │
     ▼
Generate Short Code
     │
     ▼
Check for Collision
     │
     ▼
Save to Database
     │
     ▼
Return Short URL
```

Example:

```text
Original URL:
https://example.com

        ↓

Short URL:
http://localhost:8000/abc123
```

---

# 👤 Guest Users

Guest users can shorten URLs without creating an account.

However, guest users have a limited number of URL shortening attempts.

Current guest limit:

```text
5 URL shortening attempts
```

### Guest User Workflow

```text
Guest Request
      │
      ▼
Check General Rate Limit
      │
      ▼
Check Guest Usage Limit
      │
      ├───────────────┐
      │               │
   Allowed        Limit Reached
      │               │
      ▼               ▼
Create URL        Return 403
                  Guest limit reached
```

Guest usage is tracked using Redis.

---

# 🔐 User Authentication

Registered users can create accounts and log in to receive a JWT access token.

## Registration Workflow

```text
Register User
      │
      ▼
Validate Input
      │
      ▼
Hash Password
      │
      ▼
Save User in Database
      │
      ▼
Registration Successful
```

## Login Workflow

```text
Username + Password
        │
        ▼
Find User
        │
        ▼
Verify Password
        │
        ▼
Generate JWT Token
        │
        ▼
Return Access Token
```

---

# 🔑 JWT Authentication

The project uses JWT tokens for authenticated requests.

The token contains the user identifier:

```json
{
  "sub": "user_id",
  "exp": "expiration_time"
}
```

### Authentication Workflow

```text
Client Request
      │
      ▼
Authorization Header

Bearer <JWT_TOKEN>

      │
      ▼
Decode JWT
      │
      ▼
Extract "sub"
      │
      ▼
Find User in Database
      │
      ▼
User Authenticated
```

Invalid tokens are rejected with:

```text
401 Unauthorized
```

The authentication system handles:

- Invalid JWT tokens.
- Missing `sub` claim.
- Tokens containing nonexistent user IDs.
- Missing users.
- Valid authenticated users.

---

# 🔒 Password Security

Passwords are not stored directly in the database.

The project uses:

```text
Passlib + Bcrypt
```

### Password Storage Workflow

```text
Plain Password
      │
      ▼
Bcrypt Hashing
      │
      ▼
Store Hashed Password
```

### Login Verification

```text
Entered Password
      │
      ▼
Verify Against Stored Hash
      │
      ▼
Authentication Result
```

---

# ⚡ Rate Limiting

Redis is used to implement request rate limiting.

Current general rate limit:

```text
60 requests per minute per IP
```

### Rate Limiting Workflow

```text
Incoming Request
        │
        ▼
Get Client IP
        │
        ▼
Create Redis Key

rate_limit:ip:<client_ip>

        │
        ▼
Increment Counter
        │
        ▼
Check Limit
        │
   ┌────┴─────┐
   │          │
Allowed    Exceeded
   │          │
   ▼          ▼
Continue   Return 429
Request
```

Redis automatically expires the rate-limit key after the configured time window.

---

# 👥 Guest Usage Limiting

Guest usage is controlled using Redis.

Redis key structure:

```text
guest_usage:<client_ip>
```

### Workflow

```text
Guest Shorten Request
        │
        ▼
Check Redis Counter
        │
        ▼
First Request?
   ┌────┴─────┐
   │          │
  Yes         No
   │          │
   ▼          ▼
Set Count    Check Count
   = 1          │
                ▼
          Count < Limit?
             │       │
            Yes      No
             │       │
             ▼       ▼
         Increment  Return 403
             │
             ▼
        Allow Request
```

---

# 🔁 Duplicate URL Handling

Duplicate handling works differently for guest and authenticated users.

## Registered User

If the same authenticated user submits the same URL again:

```text
User A
   │
   ▼
https://example.com
   │
   ▼
Already Exists?
   │
   ├──── Yes ────► Return Existing Short URL
   │
   └──── No ─────► Create New URL
```

The system prevents creating duplicate records for the same user and URL.

## Different Users

Different users can shorten the same original URL.

Example:

```text
User A
https://example.com
      │
      ▼
abc123


User B
https://example.com
      │
      ▼
xyz789
```

Each registered user can have their own URL record.

## Guest Users

Guest URLs are created without a user ID.

```text
user_id = None
```

---

# 🔒 Short Code Collision Handling

Before saving a new URL, the application verifies that the generated short code does not already exist.

### Workflow

```text
Generate Short Code
        │
        ▼
Check Database
        │
        ▼
Already Exists?
   │            │
  Yes           No
   │            │
   ▼            ▼
Generate Again  Save URL
```

This ensures that every stored short code is unique.

---

# ↪️ URL Redirection

When a user visits a shortened URL:

```text
http://localhost:8000/abc123
```

The application performs the following workflow:

```text
Request Short URL
        │
        ▼
Find Short Code in Database
        │
        ▼
Found?
   │            │
  Yes           No
   │            │
   ▼            ▼
Increase      Return 404
Click Count
   │
   ▼
Redirect to
Original URL
```

---

# 📊 Click Tracking

Each URL contains a click counter.

Initial value:

```text
click_count = 0
```

After the first redirect:

```text
0 → 1
```

After multiple redirects:

```text
1 → 2 → 3 → 4 ...
```

The click count is updated in the database.

---

# 🗄️ Database

The application uses **MySQL** with **SQLAlchemy ORM**.

## User Model

```text
User
├── id
├── username
├── email
└── password_hash
```

## URL Model

```text
URL
├── id
├── original_url
├── original_url_hash
├── short_code
├── click_count
└── user_id
```

For guest-created URLs:

```text
user_id = NULL
```

For authenticated users:

```text
user_id = authenticated user's ID
```

---

# 🧪 Testing

The project uses:

- Pytest
- FastAPI TestClient
- SQLAlchemy Test Database
- Redis

The test suite covers the major functionality of the application.

---

# ✅ Short Code Testing

Tests include:

- Generated short code length validation.
- Default short code length of 6 characters.
- Empty values handling.
- Invalid lengths handling.
- Negative lengths handling.
- Short code collision handling.

---

# 🔐 Authentication Testing

## Password Testing

- Password hashing.
- Correct password verification.
- Incorrect password rejection.
- Password validation.

## JWT Testing

- JWT token generation.
- JWT payload validation.
- Token expiration.
- Invalid token rejection.
- Missing `sub` claim rejection.
- Nonexistent user rejection.
- Valid token returns the correct user.

---

# 👤 Registration Testing

Tests verify:

```text
Register User
      │
      ▼
API Returns Success
      │
      ▼
Verify Response Data
      │
      ▼
Verify User Exists in Test Database
```

The tests confirm:

- Successful registration.
- Correct username.
- Correct email.
- User persistence in the database.

---

# 🔗 URL Shortening Testing

The URL shortening functionality is tested for:

- Successful URL shortening.
- Authenticated URL creation.
- Guest URL creation.
- Database persistence.
- Duplicate URL detection.
- Different users shortening the same URL.
- Short-code uniqueness.
- Short-code collision handling.

---

# ⚡ Rate Limiter Testing

The Redis rate limiter is tested for:

- First request.
- Multiple requests within the allowed limit.
- Requests exactly at the limit.
- Requests exceeding the limit.
- Redis key expiration.

Example:

```text
Limit = 5

Request 1 → Allowed
Request 2 → Allowed
Request 3 → Allowed
Request 4 → Allowed
Request 5 → Allowed
Request 6 → Blocked
```

---

# 👥 Guest Limit Testing

Guest usage tests include:

- First guest request.
- Multiple guest requests within the limit.
- Guest blocked after reaching the limit.
- Guest usage count stored in Redis.

---

# ↪️ Redirection Testing

Tests verify:

- Valid short URL redirects correctly.
- First click increments count.
- Multiple clicks increment correctly.
- Invalid short code returns `404`.

---

# 🚫 Input Validation Testing

The URL input is validated using:

```python
HttpUrl
```

Tests include:

```text
✓ Valid URL
✓ Invalid URL
✓ Empty URL
✓ Missing URL
✓ Null URL
```

Invalid input returns:

```text
422 Unprocessable Entity
```

---

# 🧪 Test Database

The application uses a separate MySQL database for testing.

Example:

```text
url_shortener_test
```

The testing workflow uses SQLAlchemy transactions to isolate tests.

```text
Start Test
    │
    ▼
Create Database Transaction
    │
    ▼
Run Test
    │
    ▼
Rollback Transaction
    │
    ▼
Clean State
```

This helps prevent test data from permanently affecting the test database.

---

# 📁 Project Structure

```text
Url-Shortner/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── config.py
│   ├── redis_client.py
│   ├── auth.py
│   │
│   └── utils/
│       ├── short_code.py
│       └── rate_limiter.py
│
├── tests/
│   ├── conftest.py
│   ├── test_register.py
│   ├── test_rate_limiter.py
│   ├── test_url_validation.py
│   └── test_auth_dependency.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> Note: The exact structure may vary slightly depending on the current project files.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/TrilochanChakrabortty/Url_Shortining.git
```

Move into the project:

```bash
cd Url_Shortining
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔧 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/url_shortener

SECRET_KEY=your_secret_key

ALGORITHM=HS256

REDIS_HOST=localhost
REDIS_PORT=6379
```

> Never commit your `.env` file to GitHub.

---

# 🗄️ Create the MySQL Database

Example:

```sql
CREATE DATABASE url_shortener;
```

For testing:

```sql
CREATE DATABASE url_shortener_test;
```

---

# 🔴 Start Redis

Make sure Redis is running before starting the application.

Example:

```bash
redis-server
```

Verify Redis:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🧪 Run Tests

Run the complete test suite:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_auth_dependency.py -v
```

Run a specific test:

```bash
pytest tests/test_auth_dependency.py::test_get_current_user_returns_valid_user -v
```

---

# 🔄 Complete Application Workflow

```text
                    USER
                     │
                     ▼
              POST /shorten
                     │
                     ▼
             Validate URL Input
                     │
                     ▼
              Check Rate Limit
                     │
          ┌──────────┴──────────┐
          │                     │
       Allowed               Blocked
          │                     │
          ▼                     ▼
   Check Authentication      Return 429
          │
     ┌────┴────┐
     │         │
  Guest      Registered
     │         │
     ▼         ▼
Check Guest   Check Existing
Usage Limit       URL
     │             │
     ▼             ▼
Allowed?      Exists?
 │   │         │     │
Yes  No       Yes    No
 │    │        │      │
 ▼    ▼        ▼      ▼
Create 403  Return   Generate
 URL       Existing   Short Code
                      │
                      ▼
                 Check Collision
                      │
                      ▼
                  Save to MySQL
                      │
                      ▼
                Return Short URL
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | API framework |
| SQLAlchemy | ORM |
| MySQL | Database |
| Redis | Rate limiting and guest usage tracking |
| JWT | Authentication |
| Passlib | Password hashing |
| Bcrypt | Password hashing algorithm |
| Pytest | Automated testing |
| Uvicorn | ASGI server |

---

# 📌 Current Project Status

The core backend functionality has been implemented and tested.

```text
Authentication       ✅
User Registration    ✅
User Login           ✅
JWT Authentication   ✅
Password Hashing     ✅
URL Shortening       ✅
Guest URLs           ✅
Duplicate Detection  ✅
Short Code Collision ✅
Redis Rate Limiting  ✅
Guest Usage Limit    ✅
URL Redirection      ✅
Click Tracking       ✅
Input Validation     ✅
Automated Testing    ✅
Full Test Suite      ✅
```

---

# 🔮 Future Improvements

Possible future improvements include:

- Custom short URLs.
- URL expiration dates.
- User URL dashboard.
- URL analytics.
- Geographic click tracking.
- Device and browser analytics.
- Redis caching.
- Refresh tokens.
- Role-based authentication.
- Docker containerization.
- CI/CD pipeline.
- Cloud deployment.
- Structured logging.
- API versioning.
- Monitoring and health checks.

---

# 👨‍💻 Author

**Trilochan Chakrabortty**

GitHub: https://github.com/TrilochanChakrabortty
