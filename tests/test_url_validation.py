from app import models
from app.redis_client import get_redis

# ============================================================
# PHASE 6.5.1
# SAME AUTHENTICATED USER SHORTENS SAME URL TWICE
# ============================================================

def test_same_user_gets_existing_url_for_duplicate(client, db):

    # ========================================================
    # STEP 1: REGISTER USER
    # ========================================================

    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    # ========================================================
    # STEP 2: LOGIN USER
    # ========================================================

    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data

    token = login_data["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ========================================================
    # STEP 3: SHORTEN URL FOR FIRST TIME
    # ========================================================

    original_url = "https://duplicate-test-example.com"

    response1 = client.post(
        "/shorten",
        json={
            "url": original_url
        },
        headers=headers
    )

    assert response1.status_code == 200, response1.json()

    data1 = response1.json()

    # ========================================================
    # STEP 4: SHORTEN THE SAME URL AGAIN
    # ========================================================

    response2 = client.post(
        "/shorten",
        json={
            "url": original_url
        },
        headers=headers
    )

    assert response2.status_code == 200, response2.json()

    data2 = response2.json()

    # ========================================================
    # STEP 5: VERIFY SAME URL RECORD IS RETURNED
    # ========================================================

    assert data1["id"] == data2["id"]

    assert (
        data1["short_code"]
        == data2["short_code"]
    )

    assert (
        data1["original_url"]
        == data2["original_url"]
    )

    # ========================================================
    # STEP 6: GET THE USER FROM DATABASE
    # ========================================================

    user = (
        db.query(models.User)
        .filter(
            models.User.username
            == user_data["username"]
        )
        .first()
    )

    assert user is not None

    # ========================================================
    # STEP 7: VERIFY THE URL RECORD EXISTS
    #
    # Query by the exact URL ID returned by the API.
    # ========================================================

    url = (
        db.query(models.URL)
        .filter(
            models.URL.id == data1["id"]
        )
        .first()
    )

    assert url is not None

    # Verify URL belongs to the logged-in user
    assert url.user_id == user.id

    # Verify original URL
    assert url.original_url == data1["original_url"]

    # Verify short code
    assert url.short_code == data1["short_code"]

    # ========================================================
    # STEP 8: VERIFY ONLY ONE RECORD EXISTS
    # ========================================================

    url_count = (
        db.query(models.URL)
        .filter(
            models.URL.original_url == data1["original_url"],
            models.URL.user_id == user.id
        )
        .count()
    )

    assert url_count == 1
    
# ============================================================
# PHASE 6.5.2
# DIFFERENT USERS CAN SHORTEN THE SAME URL
# ============================================================

def test_different_users_can_shorten_same_url(client, db):

    # ========================================================
    # STEP 1: REGISTER USER 1
    # ========================================================

    user1_data = {
        "username": "duplicateuser1",
        "email": "duplicateuser1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user1_data
    )

    assert response.status_code == 200

    # ========================================================
    # STEP 2: LOGIN USER 1
    # ========================================================

    response = client.post(
        "/auth/login",
        json={
            "username": user1_data["username"],
            "password": user1_data["password"]
        }
    )

    assert response.status_code == 200

    token1 = response.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # ========================================================
    # STEP 3: REGISTER USER 2
    # ========================================================

    user2_data = {
        "username": "duplicateuser2",
        "email": "duplicateuser2@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user2_data
    )

    assert response.status_code == 200

    # ========================================================
    # STEP 4: LOGIN USER 2
    # ========================================================

    response = client.post(
        "/auth/login",
        json={
            "username": user2_data["username"],
            "password": user2_data["password"]
        }
    )

    assert response.status_code == 200

    token2 = response.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # ========================================================
    # STEP 5: BOTH USERS SHORTEN THE SAME URL
    # ========================================================

    original_url = "https://same-url-for-different-users.com"

    response1 = client.post(
        "/shorten",
        json={
            "url": original_url
        },
        headers=headers1
    )

    assert response1.status_code == 200, response1.json()

    response2 = client.post(
        "/shorten",
        json={
            "url": original_url
        },
        headers=headers2
    )

    assert response2.status_code == 200, response2.json()

    data1 = response1.json()
    data2 = response2.json()

    # ========================================================
    # STEP 6: VERIFY DIFFERENT URL RECORDS WERE CREATED
    # ========================================================

    assert data1["id"] != data2["id"]

    # Both should contain the normalized URL
    assert data1["original_url"] == data2["original_url"]

    # ========================================================
    # STEP 7: VERIFY DATABASE RECORDS
    # ========================================================

    user1 = (
        db.query(models.User)
        .filter(
            models.User.username == user1_data["username"]
        )
        .first()
    )

    user2 = (
        db.query(models.User)
        .filter(
            models.User.username == user2_data["username"]
        )
        .first()
    )

    assert user1 is not None
    assert user2 is not None

    # Get both URL records using API-returned IDs
    url1 = (
        db.query(models.URL)
        .filter(models.URL.id == data1["id"])
        .first()
    )

    url2 = (
        db.query(models.URL)
        .filter(models.URL.id == data2["id"])
        .first()
    )

    assert url1 is not None
    assert url2 is not None

    # Verify ownership
    assert url1.user_id == user1.id
    assert url2.user_id == user2.id

    # Verify records are different
    assert url1.id != url2.id

    # Verify both users have one record for this URL
    assert (
        db.query(models.URL)
        .filter(
            models.URL.user_id == user1.id,
            models.URL.original_url == data1["original_url"]
        )
        .count()
        == 1
    )

    assert (
        db.query(models.URL)
        .filter(
            models.URL.user_id == user2.id,
            models.URL.original_url == data2["original_url"]
        )
        .count()
        == 1
    )


# ============================================================
# PHASE 6.5.3
# GUEST CAN SHORTEN SAME URL MULTIPLE TIMES
# ============================================================

def test_guest_can_shorten_same_url_multiple_times(client, db):

    # ========================================================
    # STEP 0: CLEAR GUEST REDIS LIMIT FOR TESTCLIENT
    # ========================================================

    redis_client = get_redis()

    client_ip = "testclient"

    redis_client.delete(
        f"guest_usage:{client_ip}"
    )

    # ========================================================
    # STEP 1: ORIGINAL URL
    # ========================================================

    original_url = "https://guest-duplicate-test.com"

    # ========================================================
    # STEP 2: SHORTEN URL AS GUEST - FIRST TIME
    # ========================================================

    response1 = client.post(
        "/shorten",
        json={
            "url": original_url
        }
    )

    assert response1.status_code == 200, response1.json()

    data1 = response1.json()

    # ========================================================
    # STEP 3: SHORTEN SAME URL AS GUEST - SECOND TIME
    # ========================================================

    response2 = client.post(
        "/shorten",
        json={
            "url": original_url
        }
    )

    assert response2.status_code == 200, response2.json()

    data2 = response2.json()

    # ========================================================
    # STEP 4: VERIFY DIFFERENT URL RECORDS
    # ========================================================

    assert data1["id"] != data2["id"]

    assert (
        data1["original_url"]
        == data2["original_url"]
    )

    # ========================================================
    # STEP 5: VERIFY BOTH RECORDS EXIST
    # ========================================================

    url1 = (
        db.query(models.URL)
        .filter(
            models.URL.id == data1["id"]
        )
        .first()
    )

    url2 = (
        db.query(models.URL)
        .filter(
            models.URL.id == data2["id"]
        )
        .first()
    )

    assert url1 is not None
    assert url2 is not None

    # ========================================================
    # STEP 6: VERIFY BOTH ARE GUEST URLS
    # ========================================================

    assert url1.user_id is None
    assert url2.user_id is None

    # ========================================================
    # STEP 7: VERIFY EXACTLY TWO GUEST RECORDS
    # ========================================================

    url_count = (
        db.query(models.URL)
        .filter(
            models.URL.original_url
            == data1["original_url"],

            models.URL.user_id.is_(None)
        )
        .count()
    )

    assert url_count == 2
    
from unittest.mock import patch

from app import models


# ============================================================
# PHASE 6.6
# SHORT CODE COLLISION HANDLING
# ============================================================

def test_short_code_collision_generates_new_code(client, db):

    # ========================================================
    # STEP 1: CREATE AN EXISTING URL WITH A FIXED SHORT CODE
    # ========================================================
    
    
    redis_client = get_redis()

    redis_client.delete(
        "guest_usage:testclient"
    )

    existing_url = models.URL(
        original_url="https://already-existing-url.com/",
        original_url_hash="existing_hash_123",
        short_code="ABC123",
        user_id=None,
    )

    db.add(existing_url)
    db.commit()

    # ========================================================
    # STEP 2: MOCK SHORT CODE GENERATOR
    #
    # First generated code -> ABC123 (already exists)
    # Second generated code -> XYZ789 (new)
    # ========================================================

    with patch(
        "app.main.generate_short_code",
        side_effect=[
            "ABC123",
            "XYZ789"
        ]
    ):

        response = client.post(
            "/shorten",
            json={
                "url": "https://new-url-for-collision-test.com"
            }
        )

    # ========================================================
    # STEP 3: VERIFY REQUEST SUCCEEDED
    # ========================================================

    assert response.status_code == 200, response.json()

    data = response.json()

    # ========================================================
    # STEP 4: VERIFY COLLISION WAS AVOIDED
    # ========================================================

    assert data["short_code"] == "XYZ789"

    assert data["short_code"] != "ABC123"

    # ========================================================
    # STEP 5: VERIFY DATABASE RECORD
    # ========================================================

    new_url = (
        db.query(models.URL)
        .filter(
            models.URL.id == data["id"]
        )
        .first()
    )

    assert new_url is not None

    assert new_url.short_code == "XYZ789"
    
# ============================================================
# PHASE 6.7.1
# EXISTING SHORT URL REDIRECTS TO ORIGINAL URL
# ============================================================

def test_short_url_redirects_to_original_url(client, db):

    # ========================================================
    # STEP 1: CREATE A URL RECORD
    # ========================================================

    url = models.URL(
        original_url="https://redirect-test-example.com/",
        original_url_hash="redirect_test_hash",
        short_code="RED123",
        user_id=None,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    # ========================================================
    # STEP 2: ACCESS THE SHORT URL
    #
    # follow_redirects=False is important because
    # we want to inspect the redirect response itself.
    # ========================================================

    response = client.get(
        "/RED123",
        follow_redirects=False
    )

    # ========================================================
    # STEP 3: VERIFY REDIRECT RESPONSE
    # ========================================================

    assert response.status_code in [301, 302, 307, 308]

    # ========================================================
    # STEP 4: VERIFY REDIRECT LOCATION
    # ========================================================

    assert (
        response.headers["location"]
        == "https://redirect-test-example.com/"
    )
    
# ============================================================
# PHASE 6.7.2
# CLICK COUNT INCREMENTS AFTER REDIRECT
# ============================================================

def test_short_url_click_increments_count(client, db):

    # ========================================================
    # STEP 1: CREATE URL WITH CLICK COUNT = 0
    # ========================================================

    url = models.URL(
        original_url="https://click-count-test.com/",
        original_url_hash="click_count_test_hash",
        short_code="CLK123",
        click_count=0,
        user_id=None,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    # Verify initial click count
    assert url.click_count == 0

    # ========================================================
    # STEP 2: VISIT SHORT URL
    # ========================================================

    response = client.get(
        "/CLK123",
        follow_redirects=False
    )

    # Redirect should succeed
    assert response.status_code in [301, 302, 307, 308]

    # ========================================================
    # STEP 3: REFRESH DATABASE RECORD
    # ========================================================

    db.refresh(url)

    # ========================================================
    # STEP 4: VERIFY CLICK COUNT INCREMENTED
    # ========================================================

    assert url.click_count == 1
    
# ============================================================
# PHASE 6.7.3
# MULTIPLE CLICKS INCREMENT COUNT CORRECTLY
# ============================================================

def test_multiple_short_url_clicks_increment_count(client, db):

    # ========================================================
    # STEP 1: CREATE URL WITH CLICK COUNT = 0
    # ========================================================

    url = models.URL(
        original_url="https://multiple-click-test.com/",
        original_url_hash="multiple_click_test_hash",
        short_code="MULTI1",
        click_count=0,
        user_id=None,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    # Verify initial count
    assert url.click_count == 0

    # ========================================================
    # STEP 2: CLICK THE SHORT URL 3 TIMES
    # ========================================================

    for expected_count in range(1, 4):

        response = client.get(
            "/MULTI1",
            follow_redirects=False
        )

        # Verify redirect happened
        assert response.status_code in [301, 302, 307, 308]

        # Refresh database object
        db.refresh(url)

        # Verify click count
        assert url.click_count == expected_count
        
# ============================================================
# PHASE 6.7.4
# INVALID SHORT CODE RETURNS 404
# ============================================================

def test_invalid_short_code_returns_404(client):

    invalid_short_code = "NOTFOUND123"

    response = client.get(
        f"/{invalid_short_code}",
        follow_redirects=False
    )

    # ========================================================
    # VERIFY 404 RESPONSE
    # ========================================================

    assert response.status_code == 404

    # ========================================================
    # VERIFY ERROR MESSAGE
    # ========================================================

    data = response.json()

    assert "detail" in data