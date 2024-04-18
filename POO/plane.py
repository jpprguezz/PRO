class Plane:
    BLACKBOX = True

    def __init__(self, fuel_capacity: float, max_passengers: int, storage_capacity: float, manufacturer: str, model: str, reactor: bool = True, doors = bool, wheels = bool):
        self.fuel_capacity = fuel_capacity
        self.max_passengers = max_passengers 
        self.storage_capacity = storage_capacity
        self.manufacturer = manufacturer
        self.model = model
        self.reactor = reactor
        self.doors = doors
        self.wheels = wheels

    def close_doors(self):
        if self.doors is False:
            print("Puertas cerradas")

    def open_doors(self):
        if self.doors is True:
            print("Puertas abiertas")

    def wheels_deployed(self):
        if self.wheels is True:
            print("Ruedas desplegadas")

    def wheels_retracted(self):
        if self.wheels is False:
            print("Ruedas guardadas")
