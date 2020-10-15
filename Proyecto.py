from Render import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from Material import *

from Lights import *

from Plane import *
from AABB import *
from sphere import *
import random

# Definicion de materiales
WHITE = Material(diffuse = color( 1,1,1 ) , spec= 16 )
brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
orange = Material(diffuse = color(1, 0.6, 0.0 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT)
boxMat = Material(texture = Texture('./Assets/box.bmp'))
earthMat = Material(texture = Texture('./Assets/earthDay.bmp') )
sun = Material(texture=Texture('./Assets/sun.bmp'))
venus = Material(texture=Texture('./Assets/venus.bmp'))

# Variables de iniciacion de render
width = 1920
height = 1080
r = Raytracer(width,height)
r.envmap = Envmap('./Assets/andromeda.bmp')
r.glClearColor(0, 0, 0)
r.glClear()


# Lights
# r.pointLights.append( PointLight(position = V3(-4,5,0), intensity = 0.5))
r.pointLights.append( PointLight( position = V3(4   ,2.5+ 5, 0), intensity=0.5 ))
r.pointLights.append( PointLight( position = V3(-6  ,2.5+6,-30), intensity = 0.5 , _color=color(1, 0.6, 0.0)))
r.pointLights.append( PointLight( position = V3(1.6 ,2.5+ -2.5, -20), intensity=0.5 , _color=color(1, 0.6, 0.0) ))

r.ambientLight = AmbientLight(strength = 0.1)

# Objects
r.scene.append( Plane(V3(0,-7,10) , V3(0,1,0) , WHITE) )

r.scene.append( AABB(V3(0   , -2.5 , -20) , V3(5, 0.1, 5) , glass ) )
r.scene.append( AABB(V3(0   ,  2.5 , -20) , V3(5, 0.1, 5) , glass ) )

r.scene.append( AABB(V3(-2.5, 0, -20) , V3(0.1, 5, 5) , glass ) )
r.scene.append( AABB(V3(2.5 , 0, -20) , V3(0.1, 5, 5) , glass ) )

r.scene.append( AABB(V3(0   , 0 ,-22.5) , V3(5,5,0.5) , glass))
r.scene.append( AABB(V3(0   , 0 ,-17.5) , V3(5,5,0.5) , glass))

r.scene.append( Sphere(V3( 0, 0, -20),2, sun))

r.scene.append( Sphere(V3( -3, -4+2.5 , -15),1, earthMat))
r.scene.append( Sphere(V3( 0 , -5+2.5 , -10),1, orange))
r.scene.append( Sphere(V3( 2 , 1 +2.5 , -9) , 1 , glass))
r.scene.append( Sphere(V3( -6, -3+2.5 , -22) , 1.5 , venus))
r.scene.append( Sphere(V3( 5 , -3+2.5 , -15) , 1 , venus))
r.scene.append( Sphere(V3( 5 , 4 +2.5 , -15) , 1 , brick))
r.scene.append( Sphere(V3( -4, 4 +2.5 , -15) , 1 , stone))


# Render Scene
r.rtRender()

# Print into BMP file
r.glFinish('./Results/output.bmp')
