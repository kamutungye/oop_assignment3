# OOP WITH PYTHON ASSIGNMENT 3

# *** QUESTION 3 ***
print("\n\n*** QUESTION 3 ***\n\n")


import random
import time
from datetime import datetime


class TrafficLight:
    def __init__(self, location):
        self.location = location
        self.__current_state = "RED"  # Private attribute for encapsulation

    def turn_green(self):
        self.__current_state = "GREEN"

    def turn_red(self):
        self.__current_state = "RED"

    def status(self):
        return self.__current_state


class SmartTrafficLight(TrafficLight):
    def __init__(self, location):
        super().__init__(location)

    def get_car_density(self):
        
    #    Simulated API call that returns car count from sensor.
    #    Returns:
    #        int: Number of cars detected
        
        return random.randint(0, 100)  # Simulated car count

    def adjust_durations(self, car_count):
        
    #    Adjust durations based on car density
        
        if car_count > 80:
            return 90, 30   # High traffic: longer green
        elif car_count > 50:
            return 60, 30   # Moderate traffic
        elif car_count > 15:
            return 45, 45   # Light traffic
        else:
            return 30, 60   # Very low traffic

    def run_cycle(self):
        car_count = self.get_car_density()
        green_duration, red_duration = self.adjust_durations(car_count)

        # Turn green
        self.turn_green()
        self.log_state(green_duration)

        # Simulate wait (Probably turn yelow )
        time.sleep(0.1)  # Simulated time delay (shortened)

        # Turn red
        self.turn_red()
        self.log_state(red_duration)

        # Simulate wait (Probably turn yelow )
        time.sleep(0.1)  # Simulated time delay (shortened)

    def log_state(self, duration):
        current_time = datetime.now().strftime("[%H:%M]") #picks system time
        state = self.status()
        print(f"{current_time} {self.location}: {state} for {duration}s")


# === Simulate multiple cycles ===
if __name__ == "__main__":
    traffic_light = SmartTrafficLight("Jinja Road")

    print("Starting Smart Traffic Light Simulation...\n")
    for _ in range(4):  # Simulate 4 cycles
        traffic_light.run_cycle()
