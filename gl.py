from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np
import math
import pygame

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.temp = 0 
        self.modelList = []
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)
        self.pointLight = glm.vec4(0,0,0,0)
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)
        self.viewMatrix = self.getViewMatrix()
        self.angle = 90
        self.index = 0

    def getViewMatrix(self):
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPosition)
        camPitch = glm.rotate(i, glm.radians( self.camRotation.x ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( self.camRotation.y ), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( self.camRotation.z ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        return glm.inverse( camTranslate * camRotate )
    
    def polarCoords(self):
        x = self.camPosition.x
        z = self.camPosition.z
        r = (x**2 + z**2)**0.5
        self.camPosition.x = r * math.cos(self.angle * math.pi / 180)
        self.camPosition.z = r * math.sin(self.angle * math.pi / 180)

    def camOrbit(self):
        vect = glm.vec3(0,1,0)
        camTranslate = glm.vec3(self.camPosition[0], self.camPosition[1] , self.camPosition[2] )
        self.viewMatrix = glm.lookAt(camTranslate , self.modelList[0].position , vect)

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None
        glUseProgram(self.active_shader)

    def render(self):
        self.polarCoords()
        self.camOrbit()
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"), 1, GL_FALSE, glm.value_ptr( self.viewMatrix ))
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"), 1, GL_FALSE, glm.value_ptr( self.projection ))
            glUniform4f(glGetUniformLocation(self.active_shader, "light"), self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)
            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 1, 1, 1, 1)
        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"), 1, GL_FALSE, glm.value_ptr(self.modelList[self.index].getMatrix()))
        self.modelList[self.index].renderInScene()
