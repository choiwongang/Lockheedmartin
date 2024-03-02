from djitellopy import Tello
import threading
import time

class TofTelloDrone:
    def __init__(self, tello: Tello):
        self.tello = tello
        self.tof = None
        self.tof_thread = threading.Thread(target=self.update_tof, daemon=True)

    def start(self):
        self.tof_thread.start()

    def update_tof(self):
        while True:
            self.tof = self.tello.get_distance_tof()
            time.sleep(0.1)  # Don't forget to add a small delay to avoid overloading the drone.

    def get_tof(self):
        time.sleep(0.1)
        return self.tof


