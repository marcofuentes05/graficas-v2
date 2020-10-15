"""
Intersect.py
Clase Intersect usada en Ray Tracer
"""

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal

        self.texCoords = texCoords

        self.sceneObject = sceneObject
