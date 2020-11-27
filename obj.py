
class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    continue
                if prefix == 'v':
                    try:
                        self.vertices.append(list(map(float,value.split(' '))))
                    except: 
                        continue
                elif prefix == 'vn':
                    try:
                        self.normals.append(list(map(float,value.split(' '))))
                    except:
                        continue
                elif prefix == 'vt':
                    try:
                        self.texcoords.append(list(map(float,value.split(' '))))
                    except:
                        continue
                elif prefix == 'f':
                    try:
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])
                    except:
                        continue

