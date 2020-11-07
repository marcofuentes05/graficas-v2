import pygame
from math import cos, sin, pi, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (64, 64, 64)
SPRITE_BACKGROUND = (152, 0, 136, 255)

textures = {
    '1': pygame.image.load('./Assets/Textures/wall1.jpg'),
    '2': pygame.image.load('./Assets/Textures/wall2.jpg'),
    '3': pygame.image.load('./Assets/Textures/wall.jpg'),
    '4': pygame.image.load('./Assets/Textures/wall4.png'),
    '5': pygame.image.load('./Assets/Textures/wall5.png')
}

colors = {
    '0': (20, 165, 0),
    '1': (255, 165, 0),
    '2': (0, 64, 255),
    '3': (0, 255, 64),
    '4': (255, 15, 100)
}

enemies = [{"x": 100,
            "y": 200,
            "texture": pygame.image.load('./Assets/Sprites/zombie.png')},

           {"x": 270,
            "y": 200,
            "texture": pygame.image.load('./Assets/Sprites/zombie.png')},

           {"x": 320,
            "y": 420,
            "texture": pygame.image.load('./Assets/Sprites/zombie.png')}
           ]

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        self.gameState = {
            'screen': 'menu',
            'buttons': [
                'start',
                'quit'
            ],
            'followMouse': False
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
            },
            'playPause':{
                'x': 200,
                'y': 400,
                'fontColor': 'orange',
                'backgroundColor': 'red'
            },
            'returnMenuPause':{
                'x': 500,
                'y': 400,
                'fontColor': 'orange',
                'backgroundColor': 'red'
            },
            'followMousePause': {
                'x': 350,
                'y': 200,
                'fontColor': 'orange',
                'backgroundColor': 'red'
            }
        }
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.zbuffer = [-float('inf') for z in range(int(self.width / 2))]
        
        self.blocksize = 50
        self.wallHeight = 50
        
        self.stepSize = 5
        
        self.player = {
            "x": 75,
            "y": 175,
            "angle": 0,
            "fov": 60
        }
        self.setColor(WHITE)

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
        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def drawSprite(self, sprite, size):
          # Pitagoras
        spriteDist = ((self.player['x'] - sprite['x'])**2 + (self.player['y'] - sprite['y'])**2) ** 0.5
        
        # Angulo entre el personaje y el sprite, arco tangente 2
        spriteAngle = atan2(sprite['y'] - self.player['y'], sprite['x'] - self.player['x'])

        aspectRatio = sprite["texture"].get_width() / sprite["texture"].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        #Convertir a radianes
        angleRads = self.player['angle'] * pi / 180
        fovRads = self.player['fov'] * pi / 180

        #Buscamos el punto inicial para dibujar el sprite
        startX = (self.width * 3 / 4) + (spriteAngle - angleRads)*(self.width/2) / fovRads - (spriteWidth/2)
        startY = (self.height / 2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY)

        for x in range(startX, int(startX + spriteWidth)):
            for y in range(startY, int(startY + spriteHeight)):
                if (self.width / 2) < x < self.width:
                    if self.zbuffer[ x - int(self.width/2)] >= spriteDist:
                        tx = int( (x - startX) * sprite["texture"].get_width() / spriteWidth )
                        ty = int( (y - startY) * sprite["texture"].get_height() / spriteHeight )
                        texColor = sprite["texture"].get_at((tx, ty))
                        if texColor[3] > 128 and texColor != SPRITE_BACKGROUND:
                            self.screen.set_at((x,y), texColor)
                            self.zbuffer[ x - int(self.width/2)] = spriteDist

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

    def changeScreen(self, newScreen):
        self.gameState['screen'] = newScreen

    def render(self):
        if self.gameState['screen']=='game':
            halfWidth = int(self.width / 2)
            halfHeight = int(self.height / 2)

            # Draw walls
            for x in range(0, halfWidth, self.blocksize):
                for y in range(0, self.height, self.blocksize):
                    i = int(x/self.blocksize)
                    j = int(y/self.blocksize)
                    if self.map[j][i] != ' ':
                        self.drawRect(x, y, textures[self.map[j][i]])
            self.drawPlayerIcon(BLACK)

            # Draw FPS
            for i in range(halfWidth):
                angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
                dist, wallType, tx = self.castRay(angle)
                self.zbuffer[i] = dist
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

            for enemy in enemies:
                self.screen.fill(pygame.Color("black"), (enemy['x'], enemy['y'], 3,3))
                self.drawSprite(enemy, 30)
            for i in range(self.height):
                self.screen.set_at((halfWidth, i), BLACK)
                self.screen.set_at((halfWidth+1, i), BLACK)
                self.screen.set_at((halfWidth-1, i), BLACK)
        elif self.gameState['screen']=='menu':
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
        elif self.gameState['screen']=='pause':
            halfWidth = int(self.width / 2)
            halfHeight = int(self.height / 2)

            # Draw walls
            for x in range(0, halfWidth, self.blocksize):
                for y in range(0, self.height, self.blocksize):
                    i = int(x/self.blocksize)
                    j = int(y/self.blocksize)
                    if self.map[j][i] != ' ':
                        self.drawRect(x, y, textures[self.map[j][i]])
            self.drawPlayerIcon(BLACK)

            # Draw FPS
            for i in range(halfWidth):
                angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
                dist, wallType, tx = self.castRay(angle)
                self.zbuffer[i] = dist
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

            s = pygame.Surface((1000,750))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill((255,255,255))           # this fills the entire surface
            self.screen.blit(s, (0,0)) 

            titleFont = pygame.font.SysFont("Arial", 45)
            buttonTextFont = pygame.font.SysFont("Arial", 25)   
            tfont = titleFont.render('JUEGO FANTÁSTICO' , 1 ,pygame.Color('orange'))
            startGameT = buttonTextFont.render('Continuar el juego' , 1 , pygame.Color( self.buttons['playPause']['fontColor'] ))
            exitGameT = buttonTextFont.render('Regresar a Menu Principal' , 1 , pygame.Color( self.buttons['returnMenuPause']['fontColor'] ))
            
            followMouseP = buttonTextFont.render('Seguir al Mouse: {}'.format('SI' if self.gameState['followMouse'] else 'NO') , 1 , pygame.Color( self.buttons['followMousePause']['fontColor'] ))
            
            self.screen.blit(tfont , (200,100))
            
            screen.fill(pygame.Color(self.buttons['followMousePause']['backgroundColor']), (self.buttons['followMousePause']['x'] ,self.buttons['followMousePause']['y'], 200, 30))
            self.screen.blit(followMouseP , (self.buttons['followMousePause']['x'] ,self.buttons['followMousePause']['y'] ))

            screen.fill(pygame.Color(self.buttons['playPause']['backgroundColor']), (self.buttons['playPause']['x'] ,self.buttons['playPause']['y'], 200, 30))
            self.screen.blit(startGameT , (self.buttons['playPause']['x'] ,self.buttons['playPause']['y'] ))

            screen.fill(pygame.Color(self.buttons['returnMenuPause']['backgroundColor']), (self.buttons['returnMenuPause']['x'] ,self.buttons['returnMenuPause']['y'], 300, 30))
            self.screen.blit(exitGameT, (self.buttons['returnMenuPause']['x'] ,self.buttons['returnMenuPause']['y']))

pygame.init()
screen = pygame.display.set_mode((1000, 500) , pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 25)

def getFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render('{fps} fps'.format(fps=fps), 1, pygame.Color("white"))
    return fps

r = Raycaster(screen)
r.load_map('mapTextures.txt')

isRunning = True
while isRunning:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        if r.gameState['screen'] == 'game':
            if (r.gameState['followMouse']):
                mouse = pygame.mouse.get_pos()
                r.player['angle'] = -atan2(mouse[0] - r.player['x'] , mouse[1]-r.player['y']) * 180 / 3.1594 + 90
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    r.changeScreen('pause')
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
                elif ev.key == pygame.K_q and not r.gameState['followMouse'] :
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e and not r.gameState['followMouse'] :
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
                    r.changeScreen('game')
                if r.buttons['exitMain']['x'] <= mouse[0] <= r.buttons['exitMain']['x']+150 and r.buttons['exitMain']['y'] <= mouse[1] <= r.buttons['exitMain']['y']+30:
                    isRunning = False
        elif r.gameState['screen']=='pause':
            mouse = pygame.mouse.get_pos()
            if r.buttons['playPause']['x'] <= mouse[0] <= r.buttons['playPause']['x']+200 and r.buttons['playPause']['y'] <= mouse[1] <= r.buttons['playPause']['y']+30:
                r.buttons['playPause']['backgroundColor'] = 'yellow'
            else:
                r.buttons['playPause']['backgroundColor'] = 'red'
            if r.buttons['returnMenuPause']['x'] <= mouse[0] <= r.buttons['returnMenuPause']['x']+200 and r.buttons['returnMenuPause']['y'] <= mouse[1] <= r.buttons['returnMenuPause']['y']+30:
                r.buttons['returnMenuPause']['backgroundColor'] = 'yellow'
            else:
                r.buttons['returnMenuPause']['backgroundColor'] = 'red'

            if r.buttons['followMousePause']['x'] <= mouse[0] <= r.buttons['followMousePause']['x']+200 and r.buttons['followMousePause']['y'] <= mouse[1] <= r.buttons['followMousePause']['y']+30:
                r.buttons['followMousePause']['backgroundColor'] = 'yellow'
            else:
                r.buttons['followMousePause']['backgroundColor'] = 'red'

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    r.changeScreen('game')

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if r.buttons['playPause']['x'] <= mouse[0] <= r.buttons['playPause']['x']+200 and r.buttons['playPause']['y'] <= mouse[1] <= r.buttons['playPause']['y']+30:
                    r.changeScreen('game')
                if r.buttons['returnMenuPause']['x'] <= mouse[0] <= r.buttons['returnMenuPause']['x']+150 and r.buttons['returnMenuPause']['y'] <= mouse[1] <= r.buttons['returnMenuPause']['y']+30:
                    r.changeScreen('menu')
                if r.buttons['followMousePause']['x'] <= mouse[0] <= r.buttons['followMousePause']['x']+150 and r.buttons['followMousePause']['y'] <= mouse[1] <= r.buttons['followMousePause']['y']+30:
                    r.gameState['followMouse'] = not r.gameState['followMouse']
    screen.fill(BACKGROUND)
    if (r.gameState['screen'] == 'game' or r.gameState['screen'] == 'pause'):
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
    screen.fill(pygame.Color("black"), (0, 0, 80, 30))
    screen.blit(getFPS(), (0, 0))
    clock.tick(30)

    pygame.display.update()
pygame.quit()
