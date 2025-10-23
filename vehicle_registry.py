# OOP WITH PYTHON ASSIGNMENT 3

print (
 "\nUganda Christian University"
 "\nOOP WITH PYTHON ASSIGNMENT 3, ADVENT 2025"
 "\nMaster of science in Data Science and Analystics"

 "\nStudent Name: Samuel Kamutungye"
 "\nAccess Number: B35097"
)


# *** QUESTION 1 ***
print("\n\n*** QUESTION 1 ***\n\n")

import json


class Vehicle:
    def __init__(self, plate_number, owner, engine_cc, base_tax):
        try:
            if not isinstance(plate_number, str) or not plate_number:
                raise ValueError("Invalid plate number.")
            if not isinstance(owner, str) or not owner:
                raise ValueError("Invalid owner name.")
            if not isinstance(engine_cc, (int, float)) or engine_cc < 0:
                raise ValueError("Engine CC must be a positive number.")
            if not isinstance(base_tax, (int, float)) or base_tax < 0:
                raise ValueError("Base tax must be a positive number.")
        except ValueError as e:
            print(f"Error creating vehicle: {e}")
            raise

        self.plate_number = plate_number
        self.owner = owner
        self.engine_cc = engine_cc
        self.base_tax = base_tax

    def calculate_tax(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def to_dict(self):
        return {
            "plate_number": self.plate_number,
            "owner": self.owner,
            "engine_cc": self.engine_cc,
            "base_tax": self.base_tax,
            "type": self.__class__.__name__,
            "tax": self.calculate_tax()
        }


class Car(Vehicle):
    def __init__(self, plate_number, owner, engine_cc, base_tax, passenger_capacity):
        super().__init__(plate_number, owner, engine_cc, base_tax)
        if not isinstance(passenger_capacity, int) or passenger_capacity < 1:
            raise ValueError("Passenger capacity must be a positive integer.")
        self.passenger_capacity = passenger_capacity

    def calculate_tax(self):
        return self.base_tax + (self.engine_cc * 0.05)

    def to_dict(self):
        data = super().to_dict()
        data["passenger_capacity"] = self.passenger_capacity
        return data


class Truck(Vehicle):
    def __init__(self, plate_number, owner, engine_cc, base_tax, load_capacity):
        super().__init__(plate_number, owner, engine_cc, base_tax)
        if not isinstance(load_capacity, (int, float)) or load_capacity < 0:
            raise ValueError("Load capacity must be a non-negative number.")
        self.load_capacity = load_capacity

    def calculate_tax(self):
        return self.base_tax + (self.load_capacity * 0.1)

    def to_dict(self):
        data = super().to_dict()
        data["load_capacity"] = self.load_capacity
        return data


class Motorbike(Vehicle):
    def __init__(self, plate_number, owner, engine_cc, base_tax, type_):
        super().__init__(plate_number, owner, engine_cc, base_tax)
        if type_ not in ['boda', 'private']:
            raise ValueError("Motorbike type must be 'boda' or 'private'.")
        self.type_ = type_

    def calculate_tax(self):
        return self.base_tax + 20000

    def to_dict(self):
        data = super().to_dict()
        data["motorbike_type"] = self.type_
        return data


# Function to demonstrate polymorphism and saving to JSON
def save_vehicle_registry(vehicles, filename="vehicle_registry.json"):
    try:
        data = [v.to_dict() for v in vehicles]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Vehicle registry saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")


# Example usage
if __name__ == "__main__":
    try:
        vehicles = [
            Car("UBL949L", "Sauel", 1800, 500000, 5),
            Truck("UBQ456B", "Monic", 3000, 800000, 7500),
            Motorbike("UBC789Z", "Chris", 150, 100000, "boda")
        ]

        # Demonstrating polymorphism
        for v in vehicles:
            print(f"{v.__class__.__name__} ({v.plate_number}) Tax: UGX {v.calculate_tax():,.0f}")

        # Saving to JSON
        save_vehicle_registry(vehicles)

    except Exception as e:
        print(f"Application error: {e}")
