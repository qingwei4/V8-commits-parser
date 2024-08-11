import time

class CountdownTimer:
    def __init__(self, duration=180):
        self.duration = duration
        self.time_remaining = duration
        self.state = "ready"  # Add state variable

    def start(self):
        self.state = "running"  # Set state to running when started
        self.start_time = time.time()
        while self.time_remaining > 0:
            time.sleep(1)
            self.time_remaining = max(0, self.duration - int(time.time() - self.start_time))
        self.state = "finished"  # Update state when countdown finishes

    def reset(self):
        self.time_remaining = self.duration
        self.state = "ready"  # Reset state when timer is reset

    # Add a method to get the current state
    def get_state(self):
        return self.state