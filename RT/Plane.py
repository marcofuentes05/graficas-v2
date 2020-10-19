"""
Plane.py
Clase Plane usada en RayTracer para modelar un plano infinito.
"""
from Intersect import *
from linearAlgebra import *

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normalizado(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        # t = (( position - origRayo) dot normal) / (dirRayo dot normal)

        denom = dot(dir, self.normal)

        if abs(denom) > 0.0001:
            t = dot(self.normal, restarVectores(self.position, orig)) / denom
            if t > 0:
                # P = O + tD
                hit = sumarVectores(orig, multiplicarPorEscalar(t,dir))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None
