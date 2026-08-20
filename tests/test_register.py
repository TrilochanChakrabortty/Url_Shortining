from app import models
from app.utils.auth import verify_password


# ============================================================
# 4.2.1 SUCCESSFUL USER REGISTRATION
# ============================================================

def test_register_user_success(client):

    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    # Check response status
    assert response.status_code == 200

    # Convert response to JSON
    data = response.json()

    # Check success message
    assert data["message"] == "User registered successfully"

    # Check returned user data
    assert "id" in data["user"]
    assert data["user"]["username"] == user_data["username"]
    assert data["user"]["email"] == user_data["email"]


# ============================================================
# 4.2.2 VERIFY USER IS SAVED IN DATABASE
# ============================================================

def test_register_user_saved_in_database(client, db):

    user_data = {
        "username": "databaseuser",
        "email": "databaseuser@example.com",
        "password": "password123"
    }

    # Register user through API
    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 200

    # Check user in test database
    user = (
        db.query(models.User)
        .filter(
            models.User.username == user_data["username"]
        )
        .first()
    )

    # Verify user exists
    assert user is not None

    # Verify stored data
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    
# ============================================================
# 4.2.3 VERIFY PASSWORD IS HASHED IN DATABASE
# ============================================================

def test_register_password_is_hashed(client, db):

    user_data = {
        "username": "secureuser",
        "email": "secureuser@example.com",
        "password": "password123"
    }

    # Register user
    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 200

    # Get user from test database
    user = (
        db.query(models.User)
        .filter(
            models.User.username == user_data["username"]
        )
        .first()
    )

    # User must exist
    assert user is not None

    # Password must NOT be stored as plain text
    assert user.password_hash != user_data["password"]

    # Stored hash must match the original password
    assert verify_password(
        user_data["password"],
        user.password_hash
    ) is True
    
# ============================================================
# 4.2.4 DUPLICATE USERNAME
# ============================================================

def test_register_duplicate_username(client):

    # First user registration
    first_user = {
        "username": "duplicateuser",
        "email": "first@example.com",
        "password": "password123"
    }

    first_response = client.post(
        "/auth/register",
        json=first_user
    )

    # First registration should succeed
    assert first_response.status_code == 200


    # Second user with same username
    second_user = {
        "username": "duplicateuser",
        "email": "second@example.com",
        "password": "password456"
    }

    second_response = client.post(
        "/auth/register",
        json=second_user
    )

    # Duplicate registration should fail
    assert second_response.status_code == 400

    # Check error message
    data = second_response.json()

    assert data["detail"] == "Username already exists"
    
# ============================================================
# 4.2.5 DUPLICATE EMAIL
# ============================================================

def test_register_duplicate_email(client):

    # First user registration
    first_user = {
        "username": "emailuser1",
        "email": "duplicate@example.com",
        "password": "password123"
    }

    first_response = client.post(
        "/auth/register",
        json=first_user
    )

    # First registration should succeed
    assert first_response.status_code == 200


    # Second user with the same email
    second_user = {
        "username": "emailuser2",
        "email": "duplicate@example.com",
        "password": "password456"
    }

    second_response = client.post(
        "/auth/register",
        json=second_user
    )

    # Duplicate email should fail
    assert second_response.status_code == 400

    # Check error message
    data = second_response.json()

    assert data["detail"] == "Email already registered"
    
# ============================================================
# 4.2.6 MISSING PASSWORD
# ============================================================

def test_register_missing_password(client):

    user_data = {
        "username": "missingpassword",
        "email": "missingpassword@example.com"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422
    
# ============================================================
# PASSWORD EXACTLY 8 CHARACTERS
# ============================================================

def test_register_password_exactly_eight_characters(client):

    user_data = {
        "username": "eightcharuser",
        "email": "eightchar@example.com",
        "password": "12345678"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 200
    
# ============================================================
# PASSWORD LESS THAN 8 CHARACTERS
# ============================================================

def test_register_password_less_than_eight_characters(client):

    user_data = {
        "username": "shortpassword",
        "email": "shortpassword@example.com",
        "password": "1234567"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422
    
def test_register_empty_password(client):

    user_data = {
        "username": "emptypassword",
        "email": "empty@example.com",
        "password": ""
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422
    
# ============================================================
# INVALID EMAIL FORMAT
# ============================================================

def test_register_invalid_email(client):

    user_data = {
        "username": "invalidemail",
        "email": "not-a-valid-email",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422
    
def test_login_success(client):

    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123"
    }

    # Register first
    client.post(
        "/auth/register",
        json=user_data
    )

    # Login
    login_data = {
        "username": "loginuser",
        "password": "password123"
    }

    response = client.post(
        "/auth/login",
        json=login_data
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
def test_login_wrong_password(client):

    user_data = {
        "username": "wrongpassworduser",
        "email": "wrongpass@example.com",
        "password": "password123"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "wrongpassworduser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    
def test_login_nonexistent_user(client):

    response = client.post(
        "/auth/login",
        json={
            "username": "doesnotexist",
            "password": "password123"
        }
    )

    assert response.status_code == 401
    
def test_get_current_user(client):

    user_data = {
        "username": "currentuser",
        "email": "current@example.com",
        "password": "password123"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": "currentuser",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "currentuser"
    assert data["email"] == "current@example.com"
    
def test_shorten_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    
def test_url_click_increments_count(client, db):

    # Create short URL
    response = client.post(
        "/shorten",
        json={
            "url": "https://example.com"
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    print("Shorten response:", data)

    # Get the short code depending on your API response
    short_url = data["short_url"]

    # Example:
    # http://localhost:8000/abc123
    short_code = short_url.rstrip("/").split("/")[-1]

    # Visit shortened URL
    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    # Redirect should normally be 307
    assert redirect_response.status_code in [301, 302, 307, 308]

    # Fetch URL from database
    from app import models

    url = (
        db.query(models.URL)
        .filter(
            models.URL.short_code == short_code
        )
        .first()
    )

    assert url is not None
    assert url.click_count == 1
    
def test_shorten_url_missing_url(client):

    response = client.post(
        "/shorten",
        json={}
    )

    assert response.status_code == 422
    
def test_shorten_invalid_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": "this-is-not-a-valid-url"
        }
    )

    assert response.status_code in [400, 422]
    
def test_shorten_empty_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": ""
        }
    )

    assert response.status_code in [400, 422]
    
# ============================================================
# 4.5.4 GUEST URL HAS NO USER ID
# ============================================================

from app import models


def test_guest_url_has_no_user_id(client, db):

    response = client.post(
        "/shorten",
        json={
            "url": "https://guest-example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    short_url = data["short_url"]

    # Extract short code from short URL
    short_code = short_url.rstrip("/").split("/")[-1]

    # Find URL in database
    url = (
        db.query(models.URL)
        .filter(
            models.URL.short_code == short_code
        )
        .first()
    )

    # Verify URL exists
    assert url is not None

    # Guest-created URL should not belong to any user
    assert url.user_id is None
    
def test_authenticated_user_url_has_correct_user_id(client, db):

    # --------------------------------------------------------
    # Step 1: Register a user
    # --------------------------------------------------------

    user_data = {
        "username": "urlowner",
        "email": "urlowner@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    registered_user = register_response.json()["user"]

    # --------------------------------------------------------
    # Step 2: Login and get JWT token
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": "urlowner",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # --------------------------------------------------------
    # Step 3: Create URL as authenticated user
    # --------------------------------------------------------

    response = client.post(
        "/shorten",
        json={
            "url": "https://authenticated-example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    # --------------------------------------------------------
    # Step 4: Extract short code
    # --------------------------------------------------------

    short_url = data["short_url"]

    short_code = short_url.rstrip("/").split("/")[-1]

    # --------------------------------------------------------
    # Step 5: Check URL in database
    # --------------------------------------------------------

    url = (
        db.query(models.URL)
        .filter(
            models.URL.short_code == short_code
        )
        .first()
    )

    # URL must exist
    assert url is not None

    # --------------------------------------------------------
    # Step 6: Verify ownership
    # --------------------------------------------------------

    assert url.user_id == registered_user["id"]
    
def test_users_urls_are_isolated(client, db):

    # ========================================================
    # USER A
    # ========================================================

    user_a = {
        "username": "user_a",
        "email": "user_a@example.com",
        "password": "password123"
    }

    # Register User A
    register_a = client.post(
        "/auth/register",
        json=user_a
    )

    assert register_a.status_code == 200

    user_a_id = register_a.json()["user"]["id"]

    # Login User A
    login_a = client.post(
        "/auth/login",
        json={
            "username": user_a["username"],
            "password": user_a["password"]
        }
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    # User A creates URL
    url_a_response = client.post(
        "/shorten",
        json={
            "url": "https://user-a-example.com"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    assert url_a_response.status_code == 200, url_a_response.json()

    short_url_a = url_a_response.json()["short_url"]
    short_code_a = short_url_a.rstrip("/").split("/")[-1]

    # ========================================================
    # USER B
    # ========================================================

    user_b = {
        "username": "user_b",
        "email": "user_b@example.com",
        "password": "password123"
    }

    # Register User B
    register_b = client.post(
        "/auth/register",
        json=user_b
    )

    assert register_b.status_code == 200

    user_b_id = register_b.json()["user"]["id"]

    # Login User B
    login_b = client.post(
        "/auth/login",
        json={
            "username": user_b["username"],
            "password": user_b["password"]
        }
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    # User B creates URL
    url_b_response = client.post(
        "/shorten",
        json={
            "url": "https://user-b-example.com"
        },
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert url_b_response.status_code == 200, url_b_response.json()

    short_url_b = url_b_response.json()["short_url"]
    short_code_b = short_url_b.rstrip("/").split("/")[-1]

    # ========================================================
    # CHECK DATABASE OWNERSHIP
    # ========================================================

    url_a = (
        db.query(models.URL)
        .filter(models.URL.short_code == short_code_a)
        .first()
    )

    url_b = (
        db.query(models.URL)
        .filter(models.URL.short_code == short_code_b)
        .first()
    )

    assert url_a is not None
    assert url_b is not None

    # User A's URL belongs only to User A
    assert url_a.user_id == user_a_id
    assert url_a.user_id != user_b_id

    # User B's URL belongs only to User B
    assert url_b.user_id == user_b_id
    assert url_b.user_id != user_a_id
    
# ============================================================
# PHASE 4.7.1 - DASHBOARD STATS FOR AUTHENTICATED USER
# ============================================================

def test_dashboard_stats_for_new_user(client):

    # --------------------------------------------------------
    # Step 1: Register user
    # --------------------------------------------------------

    user_data = {
        "username": "dashboarduser",
        "email": "dashboard@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    # --------------------------------------------------------
    # Step 2: Login user
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # --------------------------------------------------------
    # Step 3: Get dashboard statistics
    # --------------------------------------------------------

    response = client.get(
        "/dashboard/stats",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print(response.status_code)
    print(response.json())

    # --------------------------------------------------------
    # Step 4: Verify response
    # --------------------------------------------------------

    assert response.status_code == 200

    data = response.json()

    assert "total_urls" in data
    assert "total_clicks" in data
    
# ============================================================
# PHASE 4.7.2 - DASHBOARD TOTAL URL COUNT
# ============================================================

def test_dashboard_total_urls(client):

    # --------------------------------------------------------
    # Step 1: Register user
    # --------------------------------------------------------

    user_data = {
        "username": "statsuser",
        "email": "statsuser@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    # --------------------------------------------------------
    # Step 2: Login user
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # --------------------------------------------------------
    # Step 3: Check initial dashboard statistics
    # --------------------------------------------------------

    initial_response = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert initial_response.status_code == 200

    initial_data = initial_response.json()

    assert initial_data["total_urls"] == 0

    # --------------------------------------------------------
    # Step 4: Create first URL
    # --------------------------------------------------------

    response1 = client.post(
        "/shorten",
        json={
            "url": "https://dashboard-url-one.com"
        },
        headers=headers
    )

    assert response1.status_code == 200, response1.json()

    # --------------------------------------------------------
    # Step 5: Check dashboard again
    # --------------------------------------------------------

    stats_response_1 = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert stats_response_1.status_code == 200

    stats_data_1 = stats_response_1.json()

    assert stats_data_1["total_urls"] == 1

    # --------------------------------------------------------
    # Step 6: Create second URL
    # --------------------------------------------------------

    response2 = client.post(
        "/shorten",
        json={
            "url": "https://dashboard-url-two.com"
        },
        headers=headers
    )

    assert response2.status_code == 200, response2.json()

    # --------------------------------------------------------
    # Step 7: Check dashboard again
    # --------------------------------------------------------

    stats_response_2 = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert stats_response_2.status_code == 200

    stats_data_2 = stats_response_2.json()

    assert stats_data_2["total_urls"] == 2
    
# ============================================================
# PHASE 4.7.3 - DASHBOARD TOTAL CLICKS
# ============================================================

def test_dashboard_total_clicks(client):

    # --------------------------------------------------------
    # Step 1: Register user
    # --------------------------------------------------------

    user_data = {
        "username": "clickstatsuser",
        "email": "clickstatsuser@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    # --------------------------------------------------------
    # Step 2: Login user
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # --------------------------------------------------------
    # Step 3: Check initial click count
    # --------------------------------------------------------

    initial_stats = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert initial_stats.status_code == 200
    assert initial_stats.json()["total_clicks"] == 0

    # --------------------------------------------------------
    # Step 4: Create a short URL
    # --------------------------------------------------------

    shorten_response = client.post(
        "/shorten",
        json={
            "url": "https://click-test-example.com"
        },
        headers=headers
    )

    assert shorten_response.status_code == 200, shorten_response.json()

    data = shorten_response.json()

    short_url = data["short_url"]

    # Extract short code
    short_code = short_url.rstrip("/").split("/")[-1]

    # --------------------------------------------------------
    # Step 5: Click the shortened URL 3 times
    # --------------------------------------------------------

    for _ in range(3):

        click_response = client.get(
            f"/{short_code}",
            follow_redirects=False
        )

        assert click_response.status_code in [301, 302, 307, 308]

    # --------------------------------------------------------
    # Step 6: Check dashboard statistics
    # --------------------------------------------------------

    stats_response = client.get(
        "/dashboard/stats",
        headers=headers
    )

    assert stats_response.status_code == 200

    stats_data = stats_response.json()

    # --------------------------------------------------------
    # Step 7: Verify total clicks
    # --------------------------------------------------------

    assert stats_data["total_urls"] == 1
    assert stats_data["total_clicks"] == 3
    
# ============================================================
# PHASE 4.7.4 - DASHBOARD USER ISOLATION
# ============================================================

def test_dashboard_statistics_are_isolated_between_users(client):

    # ========================================================
    # USER A - REGISTER
    # ========================================================

    user_a = {
        "username": "dashboard_user_a",
        "email": "dashboard_user_a@example.com",
        "password": "password123"
    }

    register_a = client.post(
        "/auth/register",
        json=user_a
    )

    assert register_a.status_code == 200

    # Login User A
    login_a = client.post(
        "/auth/login",
        json={
            "username": user_a["username"],
            "password": user_a["password"]
        }
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    # ========================================================
    # USER A CREATES URL 1
    # ========================================================

    response_a1 = client.post(
        "/shorten",
        json={
            "url": "https://user-a-first-url.com"
        },
        headers=headers_a
    )

    assert response_a1.status_code == 200, response_a1.json()

    short_code_a1 = (
        response_a1.json()["short_url"]
        .rstrip("/")
        .split("/")[-1]
    )

    # ========================================================
    # USER A CREATES URL 2
    # ========================================================

    response_a2 = client.post(
        "/shorten",
        json={
            "url": "https://user-a-second-url.com"
        },
        headers=headers_a
    )

    assert response_a2.status_code == 200, response_a2.json()

    short_code_a2 = (
        response_a2.json()["short_url"]
        .rstrip("/")
        .split("/")[-1]
    )

    # ========================================================
    # CLICK USER A URLS TOTAL 5 TIMES
    # URL 1 -> 3 clicks
    # URL 2 -> 2 clicks
    # ========================================================

    for _ in range(3):

        response = client.get(
            f"/{short_code_a1}",
            follow_redirects=False
        )

        assert response.status_code in [301, 302, 307, 308]

    for _ in range(2):

        response = client.get(
            f"/{short_code_a2}",
            follow_redirects=False
        )

        assert response.status_code in [301, 302, 307, 308]

    # ========================================================
    # USER B - REGISTER
    # ========================================================

    user_b = {
        "username": "dashboard_user_b",
        "email": "dashboard_user_b@example.com",
        "password": "password123"
    }

    register_b = client.post(
        "/auth/register",
        json=user_b
    )

    assert register_b.status_code == 200

    # Login User B
    login_b = client.post(
        "/auth/login",
        json={
            "username": user_b["username"],
            "password": user_b["password"]
        }
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # ========================================================
    # USER B CREATES 1 URL
    # ========================================================

    response_b = client.post(
        "/shorten",
        json={
            "url": "https://user-b-url.com"
        },
        headers=headers_b
    )

    assert response_b.status_code == 200, response_b.json()

    short_code_b = (
        response_b.json()["short_url"]
        .rstrip("/")
        .split("/")[-1]
    )

    # ========================================================
    # CLICK USER B URL 2 TIMES
    # ========================================================

    for _ in range(2):

        response = client.get(
            f"/{short_code_b}",
            follow_redirects=False
        )

        assert response.status_code in [301, 302, 307, 308]

    # ========================================================
    # CHECK USER A DASHBOARD
    # ========================================================

    stats_a = client.get(
        "/dashboard/stats",
        headers=headers_a
    )

    assert stats_a.status_code == 200

    data_a = stats_a.json()

    assert data_a["total_urls"] == 2
    assert data_a["total_clicks"] == 5

    # ========================================================
    # CHECK USER B DASHBOARD
    # ========================================================

    stats_b = client.get(
        "/dashboard/stats",
        headers=headers_b
    )

    assert stats_b.status_code == 200

    data_b = stats_b.json()

    assert data_b["total_urls"] == 1
    assert data_b["total_clicks"] == 2