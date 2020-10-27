import pygame
from math import cos, sin, pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (64, 64, 64)


textures = {
    '1': pygame.image.load('./Assets/Textures/target.jpg'),
    '2': pygame.image.load('./Assets/Textures/Brickwall.jpg'),
    '3': pygame.image.load('./Assets/Textures/Brickwall1.jpg'),
    '4': pygame.image.load('./Assets/Textures/acdc.jpg'),
    '5': pygame.image.load('./Assets/Textures/wall5.png')
}

colors = {
    '0': (20, 165, 0),
    '1': (255, 165, 0),
    '2': (0, 64, 255),
    '3': (0, 255, 64),
    '4': (255, 15, 100)
}



class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        self.gameState = {
            'screen': 'menu',
            'buttons': [
                'start',
                'quit'
            ]
        }
        self.buttons = {
            'startMain':{
                'x':200,
                'y':400,
                'fontColor': 'orange',
                'backgroundColor' : 'red'
            },
            'exitMain':{
                'x': 500,
                'y': 400,
                'fontColor': 'orange',
                'backgroundColor' : 'red'
            }
        }
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.blocksize = 50
        self.wallHeight = 50
        self.stepSize = 5
        self.setColor(WHITE)
        self.player = {
            "x": 75,
            "y": 175,
            "angle": 0,
            "fov": 60
        }
    def setColor(self, color):
        self.blockColor = color
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize))
        rect = tex.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self, color):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))
            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize
                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY
                tx = maxHit / self.blocksize
                return dist, self.map[j][i], tx
            self.screen.set_at((x, y), WHITE)
            dist += 5

    def changeScreen(self):
        if self.gameState['screen'] == 'menu':
            self.gameState['screen'] = 'game'
        else:
            self.gameState['screen'] = 'menu'

    def render(self):
        if self.gameState['screen']=='game':
            halfWidth = int(self.width / 2)
            halfHeight = int(self.height / 2)
            for x in range(0, halfWidth, self.blocksize):
                for y in range(0, self.height, self.blocksize):
                    i = int(x/self.blocksize)
                    j = int(y/self.blocksize)
                    if self.map[j][i] != ' ':
                        self.drawRect(x, y, textures[self.map[j][i]])
            self.drawPlayerIcon(BLACK)
            for i in range(halfWidth):
                angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
                dist, wallType, tx = self.castRay(angle)
                x = halfWidth + i
                h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight
                start = int(halfHeight - h/2)
                end = int(halfHeight + h/2)

                img = textures[wallType]
                tx = int(tx * img.get_width())
                for y in range(start, end):
                    ty = (y - start) / (end - start)
                    ty = int(ty * img.get_height())
                    texColor = img.get_at((tx, ty))
                    self.screen.set_at((x, y), texColor)
            for i in range(self.height):
                self.screen.set_at((halfWidth, i), BLACK)
                self.screen.set_at((halfWidth+1, i), BLACK)
                self.screen.set_at((halfWidth-1, i), BLACK)
        else:
            titleFont = pygame.font.SysFont("Arial", 45)
            buttonTextFont = pygame.font.SysFont("Arial", 25)   
            tfont = titleFont.render('JUEGO FANTÁSTICO' , 1 ,pygame.Color('orange'))
            startGameT = buttonTextFont.render('Comenzar juego' , 1 , pygame.Color( self.buttons['startMain']['fontColor'] ))
            exitGameT = buttonTextFont.render('Salir juego' , 1 , pygame.Color( self.buttons['exitMain']['fontColor'] ))
            self.screen.blit(tfont , (200,100))
            
            screen.fill(pygame.Color(self.buttons['startMain']['backgroundColor']), (self.buttons['startMain']['x'] ,self.buttons['startMain']['y'], 200, 30))
            self.screen.blit(startGameT , (self.buttons['startMain']['x'] ,self.buttons['startMain']['y'] ))

            screen.fill(pygame.Color(self.buttons['exitMain']['backgroundColor']), (self.buttons['exitMain']['x'] ,self.buttons['exitMain']['y'], 150, 30))
            self.screen.blit(exitGameT, (self.buttons['exitMain']['x'] ,self.buttons['exitMain']['y']))



pygame.init()
screen = pygame.display.set_mode((1000, 500) , pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 25)

def getFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

r = Raycaster(screen)
r.load_map('mapTextures.txt')

isRunning = True
while isRunning:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        if r.gameState['screen'] == 'game':
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    r.player['x'] += cos(r.player['angle'] * pi / 180) * r.stepSize
                    r.player['y'] += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s:
                    r.player['x'] -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    r.player['y'] -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a:
                    r.player['x'] -= cos((r.player['angle'] + 90)
                                        * pi / 180) * r.stepSize
                    r.player['y'] -= sin((r.player['angle'] + 90)
                                        * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d:
                    r.player['x'] += cos((r.player['angle'] + 90)
                                        * pi / 180) * r.stepSize
                    r.player['y'] += sin((r.player['angle'] + 90)
                                        * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e:
                    r.player['angle'] += 5

                i = int(r.player['x'] / r.blocksize)
                j = int(r.player['y'] / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = r.player['x']
                    r.player['y'] = r.player['y']
        elif r.gameState['screen'] == 'menu':
            mouse = pygame.mouse.get_pos()
            if r.buttons['startMain']['x'] <= mouse[0] <= r.buttons['startMain']['x']+200 and r.buttons['startMain']['y'] <= mouse[1] <= r.buttons['startMain']['y']+30:
                r.buttons['startMain']['backgroundColor'] = 'yellow'
            else:
                r.buttons['startMain']['backgroundColor'] = 'red'
            if r.buttons['exitMain']['x'] <= mouse[0] <= r.buttons['exitMain']['x']+150 and r.buttons['exitMain']['y'] <= mouse[1] <= r.buttons['exitMain']['y']+30:
                r.buttons['exitMain']['backgroundColor'] = 'yellow'
            else:
                r.buttons['exitMain']['backgroundColor'] = 'red'
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if r.buttons['startMain']['x'] <= mouse[0] <= r.buttons['startMain']['x']+200 and r.buttons['startMain']['y'] <= mouse[1] <= r.buttons['startMain']['y']+30:
                    r.changeScreen()    
                if r.buttons['exitMain']['x'] <= mouse[0] <= r.buttons['exitMain']['x']+150 and r.buttons['exitMain']['y'] <= mouse[1] <= r.buttons['exitMain']['y']+30:
                    isRunning = False
    screen.fill(BACKGROUND)
    if (r.gameState['screen'] == 'game'):
        #Techo
        screen.fill(pygame.Color("saddlebrown"), (int(r.width / 2), 0, int(r.width / 2),int(r.height / 2)))
        #Piso
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2),int(r.height / 2)))
    else:
        texture = pygame.image.load('./Assets/background.jpg')
        back = pygame.transform.scale(texture , (1000,500))
        r.screen.blit(back , (0,0))
    r.render()
    # FPS
    screen.fill(pygame.Color("black"), (0, 0, 30, 30))
    screen.blit(getFPS(), (0, 0))
    clock.tick(30)

    pygame.display.update()
pygame.quit()
