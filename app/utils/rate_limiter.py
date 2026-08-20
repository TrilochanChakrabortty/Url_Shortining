from app.redis_client import get_redis


def check_rate_limit(
    identifier: str,
    limit: int,
    window_seconds: int,
) -> tuple[bool, int]:
    """
    Check whether an identifier is within its rate limit.

    Returns:
        (allowed, current_count)
    """

    redis_client = get_redis()

    key = f"rate_limit:{identifier}"

    # Increment request counter
    current_count = redis_client.incr(key)

    # First request in this window
    if current_count == 1:
        redis_client.expire(key, window_seconds)

    # Check whether the limit has been exceeded
    if current_count > limit:
        return False, current_count

    return True, current_count


def check_guest_limit(
    client_ip: str,
    limit: int = 5,
) -> tuple[bool, int]:
    """
    Check whether a guest user has reached
    the maximum allowed URL creations.
    """

    # Get Redis connection
    redis_client = get_redis()

    # Unique key for this guest IP
    key = f"guest_usage:{client_ip}"

    # Get current guest usage
    current_count = redis_client.get(key)

    # ----------------------------------------------------
    # First guest URL creation
    # ----------------------------------------------------
    if current_count is None:
        redis_client.set(key, 1)
        return True, 1

    current_count = int(current_count)

    # ----------------------------------------------------
    # Guest has already reached the limit
    # ----------------------------------------------------
    if current_count >= limit:
        return False, current_count

    # ----------------------------------------------------
    # Increase guest usage count
    # ----------------------------------------------------
    new_count = redis_client.incr(key)

    return True, new_count