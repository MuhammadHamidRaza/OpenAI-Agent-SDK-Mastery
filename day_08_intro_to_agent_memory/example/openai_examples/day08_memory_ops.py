import asyncio
from agents import SQLiteSession

async def demo():
    session = SQLiteSession("memory_ops", "test.db")

    # Add items (programmatically)
    new_items = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help?"}
    ]
    await session.add_items(new_items)
    print("Added conversation items.")

    # Read items
    items = await session.get_items()
    print(f"Memory contains {len(items)} items.")
    for i in items[-5:]:
        print(i)

    # Pop last item (undo)
    last = await session.pop_item()
    print("Removed last item:", last)

    # Clear session
    await session.clear_session()
    print("Cleared session. Items now:", await session.get_items())

asyncio.run(demo())