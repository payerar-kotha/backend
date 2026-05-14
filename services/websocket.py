from fastapi import WebSocket
from typing import Set, Dict

class PubSub:
    def __init__(self):
        self.__active_connections: Dict[str, Set[WebSocket]] = {}

    def subscribe(self, topic: str, websocket: WebSocket):
        if topic not in self.__active_connections:
            self.__active_connections[topic] = set()
        self.__active_connections[topic].add(websocket)

    def unsubscribe(self, topic: str, websocket: WebSocket):
        if topic in self.__active_connections:
            self.__active_connections[topic].discard(websocket)

    async def publish(self, topic: str, message: str):
        if topic in self.__active_connections:
            for connection in self.__active_connections[topic]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    print(f"Error occurred while sending message: {e}")