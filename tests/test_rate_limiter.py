from app.utils.rate_limiter import check_rate_limit, check_guest_limit
from app.redis_client import get_redis


# ============================================================
# TEST 1: FIRST REQUEST
# ============================================================

def test_rate_limit_allows_requests_within_limit():

    redis_client = get_redis()

    identifier = "test_rate_limit_user"

    redis_client.delete(
        f"rate_limit:{identifier}"
    )

    allowed, count = check_rate_limit(
        identifier=identifier,
        limit=5,
        window_seconds=60
    )

    assert allowed is True
    assert count == 1


# ============================================================
# TEST 2: REQUESTS UP TO LIMIT
# ============================================================

def test_rate_limit_allows_requests_up_to_limit():

    redis_client = get_redis()

    identifier = "test_multiple_requests"

    redis_client.delete(
        f"rate_limit:{identifier}"
    )

    for expected_count in range(1, 6):

        allowed, count = check_rate_limit(
            identifier=identifier,
            limit=5,
            window_seconds=60
        )

        assert allowed is True
        assert count == expected_count


# ============================================================
# TEST 3: LIMIT EXCEEDED
# ============================================================

def test_rate_limit_blocks_request_after_limit():

    redis_client = get_redis()

    identifier = "test_limit_exceeded"

    redis_client.delete(
        f"rate_limit:{identifier}"
    )

    limit = 3

    for expected_count in range(1, 4):

        allowed, count = check_rate_limit(
            identifier=identifier,
            limit=limit,
            window_seconds=60
        )

        assert allowed is True
        assert count == expected_count

    allowed, count = check_rate_limit(
        identifier=identifier,
        limit=limit,
        window_seconds=60
    )

    assert allowed is False
    assert count == 4


# ============================================================
# TEST 4: REDIS EXPIRY
# ============================================================

def test_rate_limit_sets_expiry():

    redis_client = get_redis()

    identifier = "test_expiry"

    key = f"rate_limit:{identifier}"

    redis_client.delete(key)

    check_rate_limit(
        identifier=identifier,
        limit=5,
        window_seconds=60
    )

    ttl = redis_client.ttl(key)

    assert ttl > 0
    assert ttl <= 60
    
# ============================================================
# TEST 5: FIRST GUEST REQUEST
# ============================================================

def test_guest_limit_allows_first_request():

    redis_client = get_redis()

    client_ip = "test_guest_first_request"

    key = f"guest_usage:{client_ip}"

    # Clean old test data
    redis_client.delete(key)

    allowed, count = check_guest_limit(
        client_ip=client_ip,
        limit=5
    )

    assert allowed is True
    assert count == 1
    
# ============================================================
# TEST 6: GUEST ALLOWED UP TO LIMIT
# ============================================================

def test_guest_limit_allows_requests_up_to_limit():

    redis_client = get_redis()

    client_ip = "test_guest_multiple_requests"

    key = f"guest_usage:{client_ip}"

    # Start with clean Redis data
    redis_client.delete(key)

    limit = 5

    for expected_count in range(1, limit + 1):

        allowed, count = check_guest_limit(
            client_ip=client_ip,
            limit=limit
        )

        assert allowed is True
        assert count == expected_count
        
# ============================================================
# TEST 7: GUEST BLOCKED AFTER LIMIT
# ============================================================

def test_guest_limit_blocks_request_after_limit():

    redis_client = get_redis()

    client_ip = "test_guest_limit_exceeded"

    key = f"guest_usage:{client_ip}"

    # Clean previous test data
    redis_client.delete(key)

    limit = 5

    # First 5 requests should be allowed
    for expected_count in range(1, limit + 1):

        allowed, count = check_guest_limit(
            client_ip=client_ip,
            limit=limit
        )

        assert allowed is True
        assert count == expected_count

    # Sixth request should be blocked
    allowed, count = check_guest_limit(
        client_ip=client_ip,
        limit=limit
    )

    assert allowed is False
    assert count == limit
    
# ============================================================
# TEST 8: GUEST COUNT IS STORED IN REDIS
# ============================================================

def test_guest_usage_is_stored_in_redis():

    redis_client = get_redis()

    client_ip = "test_guest_redis_storage"

    key = f"guest_usage:{client_ip}"

    # Clean previous data
    redis_client.delete(key)

    # Make 3 requests
    for _ in range(3):

        check_guest_limit(
            client_ip=client_ip,
            limit=5
        )

    # Read directly from Redis
    stored_count = redis_client.get(key)

    assert stored_count is not None
    assert int(stored_count) == 3
    
# def test_guest_can_create_url_within_limit(client):

#     # Make request as a guest (no Authorization header)
#     response = client.post(
#         "/shorten",
#         json={
#             "url": "https://guest-api-test.com"
#         }
#     )

#     print(response.status_code)
#     print(response.json())

#     # Guest should be allowed if under the limit
#     assert response.status_code == 200

# ============================================================
# PHASE 6.2 - MISSING URL FIELD
# ============================================================

def test_shorten_url_missing_url_field(client):

    response = client.post(
        "/shorten",
        json={}
    )

    assert response.status_code == 422
    
# ============================================================
# PHASE 6.3 - INVALID URL FORMAT
# ============================================================

def test_shorten_url_invalid_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": "this-is-not-a-valid-url"
        }
    )

    assert response.status_code == 422
    
# ============================================================
# PHASE 6.4 - EMPTY URL
# ============================================================

def test_shorten_url_empty_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": ""
        }
    )

    assert response.status_code == 422