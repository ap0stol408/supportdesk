from collections.abc import Mapping
import secrets


class SessionRegistry:
    def __init__(self) -> None:
        self._sessions: dict[str, int] = {}

    def issue(self, user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        self._sessions[token] = user_id
        return token

    def resolve(self, headers: Mapping[str, str]) -> int | None:
        authorization = headers.get("Authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            return None
        return self._sessions.get(token)
