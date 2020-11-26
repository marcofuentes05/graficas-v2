import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np
from obj import Obj

class Model(object):
    def __init__(self, fileName, textureName):
        self.model = Obj(fileName)

        self.createVertBuffer()

        self.texture_surface = pygame.image.load(textureName)
        self.texture_data = pygame.image.tostring(
            self.texture_surface, "RGB", 1)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)  # pitch, yaw, roll
        self.scale = glm.vec3(1, 1, 1)

    def getMatrix(self):
        i = glm.mat4(1)
        translate = glm.translate(i, self.position)
        pitch = glm.rotate(i, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(i, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(i, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        return translate * rotate * scale
      
    def createVertBuffer(self):
        buffer = []

        for face in self.model.faces:
            for i in range(4):
                try:
                    #verts
                    buffer.append(self.model.vertices[face[i][0] - 1][0])
                    buffer.append(self.model.vertices[face[i][0] - 1][1])
                    buffer.append(self.model.vertices[face[i][0] - 1][2])
                    buffer.append(1)
                except:
                    continue

                try:
                    #norms
                    buffer.append(self.model.normals[face[i][2] - 1][0])
                    buffer.append(self.model.normals[face[i][2] - 1][1])
                    buffer.append(self.model.normals[face[i][2] - 1][2])
                    buffer.append(0)
                except:
                    continue
                try:
                    #texcoords
                    buffer.append(self.model.texcoords[face[i][1] - 1][0])
                    buffer.append(self.model.texcoords[face[i][1] - 1][1])
                except:
                    continue
        self.vertBuffer = np.array(buffer, dtype=np.float32)
        self.VBO = glGenBuffers(1)  # Vertex Buffer Object
        self.VAO = glGenVertexArrays(1)  # Vertex Array Object

    def renderInScene(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes,
                     self.vertBuffer, GL_STATIC_DRAW)

        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE,
                              4 * 10, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de normal de vertices
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE,
                              4 * 10, ctypes.c_void_p(4 * 4))
        glEnableVertexAttribArray(1)

        ## Atributo de uvs de vertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                              4 * 10, ctypes.c_void_p(4 * 8))
        glEnableVertexAttribArray(2)

        # Dar textura
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture_surface.get_width(
        ), self.texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_QUADS, 0, len(self.model.faces) * 4)
