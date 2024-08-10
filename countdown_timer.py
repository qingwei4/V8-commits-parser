import time

class CountdownTimer:
    def __init__(self, duration=180):
        self.duration = duration
        self.time_remaining = duration

    def start(self):
        self.start_time = time.time()
        while self.time_remaining > 0:
            time.sleep(1)
            self.time_remaining = max(0, self.duration - int(time.time() - self.start_time))
        print("Time's up!")

    def reset(self):
        self.time_remaining = self.duration

def main():
    timer = CountdownTimer()
    timer.start()

if __name__ == "__main__":
    main()