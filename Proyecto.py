import pygame
from pygame.locals import *

from gl import Renderer
from model import Model
from obj import Obj
import shaders
import glm

deltaTime = 0.0

pygame.init()
clock = pygame.time.Clock()
screenSize = (500, 500)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

r = Renderer(screen)
r.camPosition.z = 5
r.camPosition.y= 5

r.pointLight.z = 5
r.pointLight.y = 5

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
rotateSpeed = 80
r.modelList.append(Model('./Assets/OBJs/coca.obj', './Assets/Textures/white.jpg'))
r.modelList[0].scale = glm.vec3(0.01, 0.01, 0.01)


isPlaying = True
while isPlaying:
    keys = pygame.key.get_pressed()
    if keys[K_d]:
        r.angle -= rotateSpeed * deltaTime
    if keys[K_a]:
        r.angle += rotateSpeed * deltaTime
    if keys[K_w]:
        r.camPosition.y += 10 * deltaTime
    if keys[K_s]:
        r.camPosition.y -= 10 * deltaTime
    if keys[K_q]:
        if (r.camPosition.z <= 10):
            r.camPosition.z +=1 * deltaTime
    if keys[K_e]:
        if (2 <= r.camPosition.z):
            r.camPosition.z -= 1 * deltaTime
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode()
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
    # r.getViewMatrix()
    r.polarCoords()
    r.camOrbit()
    r.render()
    pygame.display.flip()
    clock.tick(30)
    deltaTime = clock.get_time() / 1000
pygame.quit()
