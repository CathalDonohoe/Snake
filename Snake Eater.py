import random, pygame, sys,time
from pygame.locals import *

FPS = 12
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

pygame.init()
mainClock = pygame.time.Clock()
pygame.mixer.music.load('background.ogg')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

def showStartScreen():
    drawStart()
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()

def drawText(text,font,surface,x,y):
    textobj = font.render(text,1,TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake Eater')
    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoordinates = [{'x': startx,     'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    apple = getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                elif (event.key == ord('m')):
                    pygame.mixer.music.stop()
                elif (event.key == ord('n')):
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = True
                musicPlaying= not musicPlaying


        if snakeCoordinates[HEAD]['x'] == -1 or snakeCoordinates[HEAD]['x'] == CELLWIDTH or snakeCoordinates[HEAD]['y'] == -1 or snakeCoordinates[HEAD]['y'] == CELLHEIGHT:
            return #this is the death for the walls
        for snakeBody in snakeCoordinates[1:]:
            if snakeBody['x'] == snakeCoordinates[HEAD]['x'] and snakeBody['y'] == snakeCoordinates[HEAD]['y']:
                return#death for hitting self

        if snakeCoordinates[HEAD]['x'] == apple['x'] and snakeCoordinates[HEAD]['y'] == apple['y']: #kill for apple
            apple = getRandomLocation()
            scoreSound=pygame.mixer.Sound('bite.ogg')
            scoreSound.play()
        else:
            del snakeCoordinates[-1]

        if direction == UP:
            newHead = {'x': snakeCoordinates[HEAD]['x'], 'y': snakeCoordinates[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoordinates[HEAD]['x'], 'y': snakeCoordinates[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoordinates[HEAD]['x'] - 1, 'y': snakeCoordinates[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoordinates[HEAD]['x'] + 1, 'y': snakeCoordinates[HEAD]['y']}
        snakeCoordinates.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawSnake(snakeCoordinates)
        drawApple(apple)

        drawScore(len(snakeCoordinates) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawStart():
    startSurf = BASICFONT.render('Press a key to play.', True, WHITE)
    startRect = startSurf.get_rect()
    startRect= (WINDOWWIDTH - 220, WINDOWHEIGHT - 140)
    DISPLAYSURF.blit(startSurf, startRect)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    gameOver=pygame.mixer.Sound('end.ogg')
    gameOver.play()

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE) #score code
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawSnake(snakeCoordinates):
    for coord in snakeCoordinates:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, GREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, snakeInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


if __name__ == '__main__':
    main()