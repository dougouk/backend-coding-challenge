import json

# Create class of data objects

class City:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long
        self.confidence_level = 0.0
        self.edit_distance = 0
        self.physical_distance = None
        
    def __repr__(self):
        return f'{self.name}  (Confidence {self.confidence_level}) (Edit Distance {self.edit_distance}) (Distance {self.physical_distance})'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)