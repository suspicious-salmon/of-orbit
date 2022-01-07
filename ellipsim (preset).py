import pygame, math
pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

#G = 6.67408*math.pow(10, -11)
G = 40
timeInterval = 0.5

pause = -1

class Celestial:
    def __init__(self, mass, pos, vel, acc, xf, yf, rad): #xf = force components in x direction, acc = acceleration, rad = radius
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.xf = xf
        self.yf = yf
        self.rad = int(round(math.sqrt(self.mass/math.pi*10)))

cels = [] #array of celestials

#cels.append(Celestial(5.972*(math.pow(10, 24)), [400, 450], [0,0], [0,0], [], [], 5))
#cels.append(Celestial(1.989*(math.pow(10, 28)), [800, 450], [0,0], [0,0], [], [], 20))

cels.append(Celestial(5, [200, 100], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [800, 140], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [1200, 300], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [1000, 460], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [400, 560], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [100, 460], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [100, 355], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [250, 300], [0,0], [0,0], [], [], 1))
cels.append(Celestial(5, [600, 320], [0,0], [0,0], [], [], 1))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause *= -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                cels.append(Celestial(5, pygame.mouse.get_pos(), [0,0], [0,0], [], [], 1))
    screen.fill([255,255,255])

    if pause != 1:
        for i in range(len(cels)):
            cels[i].xf = []
            cels[i].yf = []

        #combines colliding celestials using a mass-weighted mean to find the new position
        dellist = []
        for i in range(len(cels)):
            for j in range(i+1, len(cels)):
                distance = math.sqrt(math.pow((cels[i].pos[0] - cels[j].pos[0]), 2) + math.pow((cels[i].pos[1] - cels[j].pos[1]), 2))
                if cels[i].rad + cels[j].rad >= distance:
                    temp1 = distance*(cels[j].mass*(cels[j].pos[0]-cels[i].pos[0]))/(distance*(cels[i].mass+cels[j].mass))
                    temp2 = distance*(cels[j].mass*(cels[j].pos[1]-cels[i].pos[1]))/(distance*(cels[i].mass+cels[j].mass))
                    #print(temp1, temp2)
                    #input()
                    cels[i].pos[0] += temp1
                    cels[i].pos[1] += temp2
                    cels[i].vel[0] = (cels[i].vel[0]*cels[i].mass+cels[j].vel[0]*cels[j].mass)/(cels[i].mass+cels[j].mass)
                    cels[i].vel[1] = (cels[i].vel[1]*cels[i].mass+cels[j].vel[1]*cels[j].mass)/(cels[i].mass+cels[j].mass)
                    cels[i].mass += cels[j].mass
                    cels[i].rad = int(round(math.sqrt(cels[i].mass/math.pi*10)))
                    dellist.append(j)
        for i in range(len(dellist)):
            #print(dellist[len(dellist)-i-1])
            del cels[dellist[len(dellist)-i-1]]

        #finds force acting on each celestial
        if len(cels) > 1:
            for i in range(len(cels)):
                for j in range(i+1, len(cels)):
                    #distance between celestials
                    distance = math.sqrt(math.pow((cels[i].pos[0] - cels[j].pos[0]), 2) + math.pow((cels[i].pos[1] - cels[j].pos[1]), 2))
                    #print("Distance:", int(round(distance)))

                    #gravitational force equation
                    force = G * cels[i].mass * cels[j].mass / math.pow(distance, 2)
                    #print("Force:", force)

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
            #print("Acceleration:", cels[i].acc[0], cels[i].acc[1])

            #finds velocity vector
            cels[i].vel = [cels[i].vel[0] + timeInterval*cels[i].acc[0], cels[i].vel[1] + timeInterval*cels[i].acc[1]]
            #print("Velocity:", cels[i].vel[0], cels[i].vel[1])
        
            #finds position vector
            cels[i].pos = [cels[i].pos[0] + timeInterval*cels[i].vel[0], cels[i].pos[1] + timeInterval*cels[i].vel[1]]
            #print("Position:", cels[i].pos[0], cels[i].pos[1])

    for i in range(len(cels)):
        pygame.draw.circle(screen, [0,0,0], [int(round(cels[i].pos[0])), int(round(cels[i].pos[1]))], cels[i].rad)

    pygame.display.flip()
