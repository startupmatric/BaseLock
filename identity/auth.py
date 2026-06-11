# Mock token → email mapping (Day 3 version)
AGENT_TOKENS = {
    "agent_user1": "user1@test.com",
    "agent_user2": "user2@test.com"
}

def resolve_token(token: str):
    if token not in AGENT_TOKENS:
        return None
    return AGENT_TOKENS[token]