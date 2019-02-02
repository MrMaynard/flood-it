class Node():

    def __init__(self, value, coordinates=()):
        self.value = value
        self.coordinates = coordinates
        self.links = []


    def __str__(self):
        return str(self.value)+ " @ " + str(self.coordinates) + " -> " + str(self.links)