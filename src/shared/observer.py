# ============== INLINE/src/shared/observer.py =============

class Observable:
    def __init__(self):
        self._subscribers: dict[str, list] = {}

    #----------------------

    def subscribe(self, event: str, callback):
        self._subscribers.setdefault(event, []).append(callback)

    #----------------------

    def unsubscribe(self, event: str, callback):
        if event in self._subscribers:
            self._subscribers[event].remove(callback)

    #----------------------

    def notify(self, event: str, payload=None):
        for callback in self._subscribers.get(event, []):
            callback(payload)