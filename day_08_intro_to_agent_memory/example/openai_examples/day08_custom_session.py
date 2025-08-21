# day08_custom_session.py
from typing import List
from agents.memory import Session  # protocol interface

class MyCustomSession(Session):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._items = []

    async def get_items(self, limit: int | None = None) -> List[dict]:
        return self._items[-limit:] if limit else list(self._items)

    async def add_items(self, items: List[dict]) -> None:
        self._items.extend(items)

    async def pop_item() -> dict | None:
        return self._items.pop() if self._items else None

    async def clear_session() -> None:
        self._items.clear()