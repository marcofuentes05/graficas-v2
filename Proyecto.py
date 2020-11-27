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

r.pointLight.z = 500
r.pointLight.y = 5

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
rotateSpeed = 80
r.modelList.append(Model('./Assets/OBJs/aircraft.obj', './Assets/Textures/green.jpg', 4))
r.modelList.append(Model('./Assets/OBJs/model.obj', './Assets/Textures/green.jpg', 3))
r.modelList.append(Model('./Assets/OBJs/helmet.obj', './Assets/Textures/green.jpg', 3))
r.modelList.append(Model('./Assets/OBJs/planta.obj', './Assets/Textures/planta.jpg', 4))
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
        if (r.camPosition.z <= 100):
            r.camPosition.z +=10 * deltaTime
    if keys[K_e]:
        if (2 <= r.camPosition.z):
            r.camPosition.z -= 10 * deltaTime
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode()
            elif ev.key == pygame.K_3:
                r.index = (r.index + 1) %4
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
            elif ev.key == pygame.K_r:
                r.modelList[r.index].textureIndex = (r.modelList[r.index].textureIndex + 1)  % 4
            elif ev.key == pygame.K_t:
                r.setShaders(shaders.vertex_shader0, shaders.fragment_shader0)
            elif ev.key == pygame.K_y:
                r.setShaders(shaders.vertex_shader, shaders.fragment_shader)

    r.render()
    pygame.display.flip()
    clock.tick(30)
    deltaTime = clock.get_time() / 1000
pygame.quit()
