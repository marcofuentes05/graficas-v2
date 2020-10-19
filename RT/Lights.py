"""
Lights.py
Clases AmbientLight, DirecionalLight, PointLight usadas en RayTracer para modelar esquemas de iluminacion
"""
from Render import color, V3, V4
from linearAlgebra import *

WHITE = color(1,1,1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class DirectionalLight(object):
    def __init__(self, direction = V3(0,-1,0), _color = WHITE, intensity = 1):
        self.direction = normalizado(direction)
        self.intensity = intensity
        self.color = _color

class PointLight(object):
    def __init__(self, position = V3(0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color
