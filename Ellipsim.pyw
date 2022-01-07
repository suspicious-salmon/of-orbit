import pygame, math, sys, time, random
from timeit import default_timer as timer
pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

#G = 6.67408*math.pow(10, -11)
G = 100
timeInterval = 0.01

doTimeAccuracy = False
pausing = True
placing = False
pos = []
counter = 0
radiusConstant = 10

class Celestial:
    def __init__(self, mass, pos, vel, acc, xf, yf, rad): #xf = force components in x direction, acc = acceleration, rad = radius
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.xf = xf
        self.yf = yf
        self.rad = int(round(math.sqrt(self.mass/math.pi*radiusConstant)))

cels = [] #array of celestials
#cels.append(Celestial(10))
#for i in range(100):
#    cels.append(Celestial(random.randint(2, 20), [random.randint(20, 1260), random.randint(20, 700)], [0,0], [0,0], [], [], 1))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not placing:
                    pausing = not pausing
            if event.type == pygame.MOUSEBUTTONDOWN and pausing:
                if event.button == 1: #left mouse button
                    if counter == 0:
                        placing = True
                        pos = pygame.mouse.get_pos()
                        counter = 0
                if event.button == 3: #right mouse button
                    pos = []
                    del cels[-1]
                    placing = False
            if event.type == pygame.MOUSEBUTTONUP and placing:
                counter += 1
                if counter == 2: #setting mass
                    temp = math.sqrt(math.pow(pygame.mouse.get_pos()[0] - pos[0], 2) + math.pow(pygame.mouse.get_pos()[1] - pos[1], 2))
                    a = int(round(temp))
                    b = math.pi * math.pow(temp, 2) / radiusConstant
                    cels.append(Celestial(b, pos, [0,0], [0,0], [], [], a))
                if counter == 3: #setting velocity
                    placing = False
                    cels[-1].vel[0] = (pygame.mouse.get_pos()[0] - pos[0])/10
                    cels[-1].vel[1] = (pygame.mouse.get_pos()[1] - pos[1])/10
                    print(cels[-1].mass)
                    counter = 0
             
    screen.fill([0,0,0])
    if not pausing: start = timer()

    if not pausing:
        for i in range(len(cels)):
            cels[i].xf = []
            cels[i].yf = []

        #combines colliding celestials - goes through all celestial pais and check for collisions. Then creates an array which contains each multi-object collision. Then goes through array and computes new location of newly formed object etc as well as deleting colliding objects.
        #STILL BROKEN when there is a collision between objects but every object is not touching every other object e.g. 4 colliding in a square pattern
        collisions = []
        for i in range(len(cels)):
            collidingwith = []
            for j in range(len(cels)):
                if i != j:
                    distance = math.sqrt(math.pow((cels[i].pos[0] - cels[j].pos[0]), 2) + math.pow((cels[i].pos[1] - cels[j].pos[1]), 2))
                    if cels[i].rad + cels[j].rad >= distance:
                        collidingwith.append(j)
            if len(collidingwith) > 0:
                collidingwith.append(i)
                x, y, c = 0, 0, 0
                temparr = []
                for j in range(len(collidingwith)):
                    temparr.append(collidingwith[j])
                    x += cels[collidingwith[j]].mass * cels[collidingwith[j]].pos[0]
                    y += cels[collidingwith[j]].mass * cels[collidingwith[j]].pos[1]
                    c += cels[collidingwith[j]].mass
                temparr.sort()
                temparr.insert(0, y/c)
                temparr.insert(0, x/c)
                print(temparr)
                if temparr not in collisions:
                    collisions.append(temparr)

        dellist = []
        for i in range(len(collisions)):
            cels.append(Celestial(0, [collisions[i][0], collisions[i][1]], [0,0], [0,0], [], [], 1))
            for j in range(2, len(collisions[i])):
                cels[-1].mass += cels[collisions[i][j]].mass
                cels[-1].vel[0] += cels[collisions[i][j]].mass * cels[collisions[i][j]].vel[0]
                cels[-1].vel[1] += cels[collisions[i][j]].mass * cels[collisions[i][j]].vel[1]
                dellist.append(collisions[i][j])
            cels[-1].vel[0] = cels[-1].vel[0] / cels[-1].mass
            cels[-1].vel[1] = cels[-1].vel[1] / cels[-1].mass
            cels[-1].rad = int(round(math.sqrt(cels[-1].mass/math.pi*radiusConstant)))
            print(cels[-1].mass, cels[-1].vel)
        if len(dellist) > 0:
            dellist.sort(reverse = True)
            print(dellist)
            for j in range(len(dellist)):
                del cels[dellist[j]]

        #OLD combines colliding celestials
        #dellist = []
        #for i in range(len(cels)):
        #    for j in range(i+1, len(cels)):
        #        distance = math.sqrt(math.pow((cels[i].pos[0] - cels[j].pos[0]), 2) + math.pow((cels[i].pos[1] - cels[j].pos[1]), 2))
        #        if cels[i].rad + cels[j].rad >= distance:
        #            temp1 = distance*(cels[j].mass*(cels[j].pos[0]-cels[i].pos[0]))/(distance*(cels[i].mass+cels[j].mass))
        #            temp2 = distance*(cels[j].mass*(cels[j].pos[1]-cels[i].pos[1]))/(distance*(cels[i].mass+cels[j].mass))
        #            cels[i].pos[0] += temp1
        #            cels[i].pos[1] += temp2
        #            cels[i].vel[0] = (cels[i].vel[0]*cels[i].mass+cels[j].vel[0]*cels[j].mass)/(cels[i].mass+cels[j].mass)
        #            cels[i].vel[1] = (cels[i].vel[1]*cels[i].mass+cels[j].vel[1]*cels[j].mass)/(cels[i].mass+cels[j].mass)
        #            cels[i].mass += cels[j].mass
        #            cels[i].rad = int(round(math.sqrt(cels[i].mass/math.pi*10)))
        #            dellist.append(j)
        #dellist.sort(reverse = True)
        #for i in range(len(dellist)):
        #    del cels[dellist[i]]

        #finds force acting on each celestial
        if len(cels) > 1:
            for i in range(len(cels)):
                for j in range(i+1, len(cels)):
                    #distance between celestials
                    distance = math.sqrt(math.pow((cels[i].pos[0] - cels[j].pos[0]), 2) + math.pow((cels[i].pos[1] - cels[j].pos[1]), 2))
                    
                    #gravitational force equation
                    force = G * cels[i].mass * cels[j].mass / math.pow(distance, 2)

                    #x and y component vectors for celestial 1
                    cels[i].xf.append(force * (cels[j].pos[0] - cels[i].pos[0]) / distance)
                    cels[i].yf.append(force * (cels[j].pos[1] - cels[i].pos[1]) / distance)

                    #x and y component vectors for celestial 2
                    cels[j].xf.append(force * (cels[i].pos[0] - cels[j].pos[0]) / distance)
                    cels[j].yf.append(force * (cels[i].pos[1] - cels[j].pos[1]) / distance)

        #resolves forces for each celestial, calculating vectors for acceleration and velocity
        for i in range(len(cels)):

            #resolves forces into one x and one y force
            if len(cels) > 1:
                temp = 0
                for j in range(len(cels[i].xf)):
                    temp += cels[i].xf[j]
                cels[i].xf[0] = temp
                temp = 0
                for j in range(len(cels[i].yf)):
                    temp += cels[i].yf[j]
                cels[i].yf[0] = temp

            #finds acceleration vector
            if len(cels) > 1:
                cels[i].acc = [cels[i].xf[0] / cels[i].mass , cels[i].yf[0] / cels[i].mass]
            else:
                cels[i].acc = [0,0]

            #finds velocity vector
            cels[i].vel = [cels[i].vel[0] + timeInterval*cels[i].acc[0], cels[i].vel[1] + timeInterval*cels[i].acc[1]]
        
            #finds position vector
            cels[i].pos = [cels[i].pos[0] + timeInterval*cels[i].vel[0], cels[i].pos[1] + timeInterval*cels[i].vel[1]]

    for i in range(len(cels)):
        pygame.draw.circle(screen, [125,125,125], [int(round(cels[i].pos[0])), int(round(cels[i].pos[1]))], cels[i].rad)

    if pausing:
        pygame.draw.line(screen, [250,250,250], [1270,5], [1270,15], 5)
        pygame.draw.line(screen, [250,250,250], [1263,5], [1263,15], 5)
    if placing:
        if counter == 1:
            pygame.draw.circle(screen, [175,175,175], pos, int(round(math.sqrt(math.pow(pygame.mouse.get_pos()[0] - pos[0], 2) + math.pow(pygame.mouse.get_pos()[1] - pos[1], 2)))))
        if counter == 2:
            pygame.draw.line(screen, [125,125,125], pos, pygame.mouse.get_pos(), 3)

    if not pausing and doTimeAccuracy: #a timer makes sure each step is no shorter than a set amount of real life time
        end = timer()
        if timeInterval/2 - (end - start) > 0:
            time.sleep(timeInterval/2 - (end - start))

    pygame.display.flip()
    
