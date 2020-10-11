from Render import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from Material import *

from Lights import *

from Plane import *
from AABB import *
from sphere import *
import random

# Dedinicion de materiales
WHITE = Material(diffuse = color( 1,1,1 ) , spec= 16 )
brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT)
boxMat = Material(texture = Texture('./Assets/box.bmp'))
earthMat = Material(texture = Texture('./Assets/earthDay.bmp') )

# Variables de iniciacion de render
width = 256
height = 256
r = Raytracer(width,height)
r.envmap = Envmap('./Assets/envmap.bmp')
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()


# Lights
# r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))

# r.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)

r.ambientLight = AmbientLight(strength = 0.1)

# Objects
r.scene.append( Plane(V3(0,-4,10) , V3(0,1,0) , WHITE) )
# for i in range(10):  
#   r.scene.append( Sphere(V3(-2, -2 ,-i*2-5) , 0.5 , WHITE))
#   r.scene.append( Sphere(V3(-2, -2 ,-i*2-5) , 0.5 , WHITE))
r.scene.append( Plane(V3(0,0,10) , V3(0,0,-1) , WHITE) )

r.scene.append( Plane(V3(-10,0,-10) , V3(1,0,0) , WHITE) )
r.scene.append( Plane(V3(10,0,10) , V3(-1,0,0) , WHITE) )

r.scene.append( Plane(V3(0,10,0) , V3(0,-1,0) , WHITE) )
r.scene.append( Plane(V3(0,-10,0) , V3(0,1,0) , WHITE) )

r.scene.append( Sphere(V3( 0, -2, -8), 2, mirror) )
r.scene.append( Sphere(V3( 0, 2, -8), 2, glass) )
r.scene.append( Sphere(V3( -0.5, 0.5, -5), 0.25, stone))
r.scene.append( Sphere(V3( 0.25, 0.5, -5), 0.25, brick))


# r.scene.append( AABB(V3(0, -3, -10), V3(5, 0.1, 5) , boxMat ) )
# r.scene.append( AABB(V3(1.5, 1.5, -5), V3(1, 1, 1) , glass ) )
# r.scene.append( AABB(V3(-1.5, 0, -5), V3(1, 1, 1) , boxMat ) )

# r.scene.append( Sphere(V3( 0, 0, -8), 2, earthMat))


# Render Scene
r.rtRender()

# Print into BMP file
r.glFinish('./Results/output.bmp')