"""
Material.py
Clase material usada en RayTracer para modelar distintos tipos de superficies.
"""
from Render import color, V3, V4
WHITE = color(1,1,1)
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec

        self.matType = matType
        self.ior = ior

        self.texture = texture
        