import pygame as pg
import random as r
import math

RUN = True

WIDTH = 800
HEIGHT = 800
MINSPEED = 0
TOPSPEED = 0
MINSIZE = 5
MAXSIZE = 10
DENSITY = 50
GConstant = 1
TICKRATE = 30
METEORCOUNT = 50
AFTERIMGCOUNT = 100
afterimageseparator = 5
afterimageswitch = False
FILLSWITCH = True
dt =5000

pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode((WIDTH,HEIGHT))

# QOL FUNCTIONS
def DistanceFromMouseVector(pos,mousePos):
    return [mousePos[0]-pos[0],mousePos[1]-pos[1]]

def DistanceFromMouse(pos,mousePos):
    return math.sqrt((pos[0]-mousePos[0])**2 + (pos[1]-mousePos[1])**2)


# METEOR CLASS
class meteor:
    def __init__(self):
        self.originVector = [r.randint(0,WIDTH),r.randint(0,HEIGHT)]
        self.radius = r.uniform(MINSIZE,MAXSIZE)
        self.dx = r.uniform(MINSPEED,TOPSPEED)
        self.dy = r.uniform(MINSPEED,TOPSPEED)
        self.distanceFromMouse = None
        self.ddx = 0
        self.ddy = 0
        self.color = (r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.mass = DENSITY * 4/3 * math.pi * self.radius
        self.afterimg = []
        self.ogcolor = self.color

    def move(self,mousePos,focused):

        # MOUSE METHODS
        if(focused):
            self.distanceFromMouseVector = DistanceFromMouseVector(self.originVector,mousePos)
            self.distanceFromMouse = DistanceFromMouse(self.originVector,mousePos)

            # force between 2 masses = F, divide by m to get a
            # force = (GConstant * MOUSEMASS * self.mass) / (self.distanceFromMouse**2)

            self.distanceFromMouseVector = self.distanceFromMouseVector[0]*dt,self.distanceFromMouseVector[1]*dt
            self.dx += self.distanceFromMouseVector[0] / (self.distanceFromMouse**2 * self.mass)
            self.dy += self.distanceFromMouseVector[1] / (self.distanceFromMouse**2 * self.mass)

        # multiplier = 60
        # if abs(self.dx)*multiplier > 255:
        #     self.color = (255,255,255)
        # else: self.color = (abs(self.dx)*multiplier,abs(self.dx)*multiplier,abs(self.dx)*multiplier)



        # MOVE
        self.originVector[0] += self.dx
        self.originVector[1] += self.dy

        # RETURN THE OTHER SIDE IF IT GOES PAST THE WIDTH/LENGTH
        # if self.originVector[0]-self.radius > WIDTH:
        #     self.originVector[0] = 0 -self.radius
        # if self.originVector[1]-self.radius > HEIGHT:
        #     self.originVector[1] = 0-self.radius
            
    def draw(self):
        pg.draw.circle(window,self.color,(self.originVector[0],self.originVector[1]),self.radius)
        if afterimageswitch:
            if len(self.afterimg) == (AFTERIMGCOUNT-1):
                del self.afterimg[0]
            if len(self.afterimg) < AFTERIMGCOUNT:
                item = self.originVector.copy()
                self.afterimg += [item] 
            if len(self.afterimg) >= 1: 
                for idx, i in enumerate(self.afterimg[::-1]): 
                    if idx % afterimageseparator:
                        pg.draw.circle(window,self.color,(i[0],i[1]),self.radius*0.95**idx)
                        # pg.draw.circle(window,self.color,(i[0],i[1]),self.radius)


# STARTUP METHODS
meteors = [meteor() for i in range(METEORCOUNT)]

# main game loop
while RUN:

    # EVENT METHODS
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            key = event.unicode
            if key == 'q':
                RUN = False
            if key =='p':
                dt = int(input(f"enter the desired gravitational strength, the current strength is {dt}: "))
            if key =='o':
                METEORCOUNT = int(input(f"enter the new meteor count, the current is {METEORCOUNT}: "))
                meteors = [meteor() for i in range(METEORCOUNT)]
            if key =='c':
                meteors = [meteor() for i in range(METEORCOUNT)]
            if key =='a':
                afterimageswitch =  not afterimageswitch
            if key =='f':
                FILLSWITCH =  not FILLSWITCH
            
        if event.type == pg.QUIT:
            RUN = False

    # METEOR METHODS
    for i in meteors:
        i.draw() 
        i.move(pg.mouse.get_pos(),pg.mouse.get_focused())

    # PYGAME METHODS
    pg.display.update()
    if FILLSWITCH:
        window.fill('black')
    clock.tick(TICKRATE)
