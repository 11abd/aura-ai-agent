def should_retry(state):
    """
    Decide whether to retry generation
    """

    score = state.get("score", 0)
    retries = state.get("retries", 0)

    # Retry if score low and retries < limit
    if score < 7 and retries < 2:
        return "retry"

    return "end"