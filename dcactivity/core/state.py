import time


class State:
    def __init__(self):
        self.last_state = None
        self.last_details = None
        self.last_command = None
        self.started_at = int(time.time())
        self.last_activity_time = time.time()

    def should_update(self, new_state: str, new_details: str = None):
        return (new_state != self.last_state) or (new_details != self.last_details)

    def set(self, new_state: str, new_details: str = None, command: str = None):
        if self.should_update(new_state, new_details):
            self.last_state = new_state
            self.last_details = new_details
            self.last_command = command
            self.started_at = int(time.time())
        self.last_activity_time = time.time()

    def touch(self):
        self.last_activity_time = time.time()

    def idle_seconds(self):
        return time.time() - self.last_activity_time

    def elapsed(self):
        return int(time.time() - self.started_at)
