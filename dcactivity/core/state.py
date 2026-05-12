import time


class State:
    def __init__(self):
        self.last_state = None
        self.started_at = time.time()

    def should_update(self, new_state: str) -> bool:
        return new_state != self.last_state

    def set_state(self, new_state: str):
        if new_state != self.last_state:
            self.last_state = new_state
            self.started_at = time.time()

    def elapsed(self) -> int:
        return int(time.time() - self.started_at)