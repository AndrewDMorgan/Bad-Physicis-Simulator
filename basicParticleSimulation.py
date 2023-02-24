import pygame, time, math, random
CHUNK_SIZE = 5
GRAVITY = 8
DAMPER = 0.9
ID = 0  # the current particles id

pygame.init()


class Particle:
    def __init__(self, x: float, y: float, r: float, density: float = 1) -> None:
        global ID
        
        self.__x = x
        self.__y = y
        self.__r = r
        self.__density = density

        self.__vX = 0
        self.__vY = 0

        self.id = ID
        ID += 1

        self.__mass = math.pi * (r*r) * self.__density
    
    def AddForce(self, fX: float, fY: float, dt: float) -> None:
        aX = fX / self.__mass
        aY = fY / self.__mass

        self.__vX += dt * aX
        self.__vY += dt * aY

    def Update(self, dt: float) -> None:
        self.__vY += 9.81 * dt * GRAVITY

        self.__x += self.__vX * dt
        self.__y += self.__vY * dt
    
    def GetRadius(self) -> float:
        return self.__r
    
    def GetX(self) -> float:
        return self.__x
    def GetY(self) -> float:
        return self.__y
    
    def GetVelocityX(self) -> float:
        return self.__vX
    def GetVelocityY(self) -> float:
        return self.__vY
    
    def SetVelocity(self, vX: float, vY: float) -> None:
        self.__vX = vX
        self.__vY = vY
    
    def GetMass(self) -> float:
        return self.__mass
    
    def MovePos(self, dX: float, dY: float) -> None:
        self.__x += dX
        self.__y += dY


class ParticleManager:
    def __init__(self) -> None:
        self.__particles = {}

    def SolveCollision1D(self, m1: float, m2: float, v1: float, v2: float) -> tuple:
        # solving two equations so a 2 variable system can be solved
        equation1Left = m1 * v1 + m2 * v2  # getting the value of the left side of the equation to be further solved
        equation2Left = v1 - v2  # getting the left hand side of the solved equation

        finalEquationLeft = m1 + m2
        finalEquationRight = equation1Left + equation2Left * m1

        # getting the final velocities
        v2f = finalEquationRight / finalEquationLeft
        v1f = v2f - v1 + v2

        return [v1f, v2f]

    def Reposition(self, particle: Particle, dt: float) -> None:
        global colSphere, colNormalPos, colHeadingPos, colRefledPos, dtScalar
        radius = particle.GetRadius()

        rchunkX, rchunkY = round(particle.GetX() / CHUNK_SIZE), round(particle.GetY() / CHUNK_SIZE)
        chunkX, chunkY = int(particle.GetX() // CHUNK_SIZE), int(particle.GetY() // CHUNK_SIZE)

        shift = [1, 1]
        if rchunkX == chunkX:
            shift[0] = -1
        if rchunkY == chunkY:
            shift[1] = -1

        chunks = [(chunkX, chunkY), (chunkX + shift[0], chunkY), (chunkX, chunkY + shift[1]), (chunkX + shift[0], chunkY + shift[1])]
        for chunkPos in chunks:
            if chunkPos in self.__particles:
                for otherParticle in self.__particles[chunkPos]:
                    if otherParticle.id != particle.id:
                        difX = otherParticle.GetX() - particle.GetX()
                        difY = otherParticle.GetY() - particle.GetY()

                        distance = math.sqrt(difX*difX + difY*difY)

                        radiusSum = radius + otherParticle.GetRadius()
                        
                        if distance < radiusSum:
                            particleX = particle.GetX()
                            particleY = particle.GetY()
                            otherParticleX = otherParticle.GetX()
                            otherParticleY = otherParticle.GetY()

                            halfDif = 0.5 * (radiusSum - distance)

                            scaledDifX = difX / distance * halfDif
                            scaledDifY = difY / distance * halfDif

                            otherParticle.MovePos(scaledDifX, scaledDifY)
                            particle.MovePos(-scaledDifX, -scaledDifY)

                            m1 = particle.GetMass()
                            m2 = otherParticle.GetMass()

                            v1x = particle.GetVelocityX()
                            v1y = particle.GetVelocityY()

                            v2x = otherParticle.GetVelocityX()
                            v2y = otherParticle.GetVelocityY()
                            
                            centerDifX , centerDifY  = particleX - otherParticleX, particleY - otherParticleY

                            dot = ((v1x - v2x)*centerDifX + (v1y - v2y)*centerDifY)

                            v1xf = v1x - (2 * m2 / (m1 + m2)) * (dot / (centerDifX*centerDifX + centerDifY*centerDifY)) * centerDifX
                            v1yf = v1y - (2 * m2 / (m1 + m2)) * (dot / (centerDifX*centerDifX + centerDifY*centerDifY)) * centerDifY
                            v2xf = v2x - (2 * m1 / (m1 + m2)) * (dot / (difX*difX + difY*difY)) * difX
                            v2yf = v2y - (2 * m1 / (m1 + m2)) * (dot / (difX*difX + difY*difY)) * difY

                            # setting the new velocities
                            particle     .SetVelocity(v1xf * DAMPER, v1yf * DAMPER)
                            otherParticle.SetVelocity(v2xf * DAMPER, v2yf * DAMPER)

                            del self.__particles[chunkPos][self.__particles[chunkPos].index(otherParticle)]
                            if self.__particles[chunkPos] == []:
                                del self.__particles[chunkPos]
                            self.AddParticle(otherParticle)
        
        # this system is not pushing particles out of the walls correctly sometimes
        x = particle.GetX()
        y = particle.GetY()
        if x < 0 or x > width:
            vx = particle.GetVelocityX()
            vy = particle.GetVelocityY()

            if vx == 0:
                if x < 0:
                    particle.MovePos(0, abs(x))
                else:
                    particle.MovePos(0, width - x)
            else:
                if x < 0:
                    if vx < 0:
                        vx *= -1
                        particle.SetVelocity(vx, vy)
                    distOut = abs(x) / vx
                else:
                    if vx > 0:
                        vx *= -1
                        particle.SetVelocity(vx, vy)
                    distOut = (x - width) / vx
                distOut = abs(distOut)

                particle.MovePos(vx * distOut, vy * distOut)
                particle.SetVelocity(vx * DAMPER, vy * DAMPER)
            
            x = particle.GetX()
            y = particle.GetY()
        if y < 0 or y > height:
            vx = particle.GetVelocityX()
            vy = particle.GetVelocityY()

            if vy == 0:
                if y < 0:
                    particle.MovePos(0, abs(y))
                else:
                    particle.MovePos(0, height - y)
            else:
                if y < 0:
                    if vy < 0:
                        vy *= -1
                    distOut = abs(y) / vy
                else:
                    if vy > 0:
                        vy *= -1
                    distOut = (y - height) / vy
                distOut = abs(distOut)
                
                particle.MovePos(vx * distOut, vy * distOut)
                particle.SetVelocity(vx * DAMPER, vy * DAMPER)
        
        del self.__particles[chunks[0]][self.__particles[chunks[0]].index(particle)]
        if self.__particles[chunks[0]] == []:
            del self.__particles[chunks[0]]
        
        self.AddParticle(particle)

    def Update(self, dt: float) -> None:
        copy = self.__particles.copy()
        dtNew = dt / 10
        
        for i in range(10):
            for particleChunk in copy:
                if particleChunk in self.__particles:
                    particles = self.__particles[particleChunk]
                    del self.__particles[particleChunk]
                    for particle in particles:
                        particle.Update(dtNew)
                        self.AddParticle(particle)
                        self.Reposition(particle, dt)
    
    def AddParticle(self, particle: Particle):
        chunkX, chunkY = int(particle.GetX() // CHUNK_SIZE), int(particle.GetY() // CHUNK_SIZE)
        if (chunkX,chunkY) not in self.__particles:
            self.__particles[(chunkX,chunkY)] = []
        self.__particles[(chunkX, chunkY)].append(particle)
    def GetParticles(self) -> list:
        return self.__particles


width, height = 1200, 750
screen = pygame.display.set_mode((width, height))


particleColors = []
particleManager = ParticleManager()

"""
for i in range(100):
    particle = Particle(random.randint(25, width - 25), random.randint(25, height - 25), random.randint(10, 25))
    particle.AddForce(random.uniform(-1, 1), random.uniform(-1, 1), 1500 * particle.GetRadius())
    particleManager.AddParticle(particle)
    particleColors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#"""

dt = 0
totTime = 0
totTimeMark = 0
running = True

while running:
    frameStart = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not running:
        pygame.quit()
        break

    screen.fill((225, 225, 225))

    #"""
    if totTime > totTimeMark and totTime < 1000*16:
        particle = Particle(100, 100, 5)
        particle.AddForce(3.5, 0, 1750 * particle.GetRadius())
        particleManager.AddParticle(particle)
        particleColors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        totTimeMark += 1/16
    #"""

    particles = particleManager.GetParticles()
    for chunkPos in particles:
        for particle in particles[chunkPos]:
            pygame.draw.circle(screen, particleColors[particle.id], (particle.GetX(), particle.GetY()), particle.GetRadius())

    particleManager.Update(dt * 15)

    pygame.display.update()

    frameEnd = time.time()
    dt = frameEnd - frameStart
    totTime += dt


