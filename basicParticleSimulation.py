import pygame, time, math
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
        # self.__vY += 9.81 * dt

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
        self.__particles = []

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

    def Reposition(self, particle: Particle) -> None:
        radius = particle.GetRadius()

        for otherParticle in self.__particles:
            if otherParticle.id != particle.id:
                difX = otherParticle.GetX() - particle.GetX()
                difY = otherParticle.GetY() - particle.GetY()

                distance = math.sqrt(difX*difX + difY*difY)

                radiusSum = radius + otherParticle.GetRadius()
                
                if distance < radiusSum:
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

                    v1xf, v2xf = self.SolveCollision1D(m1, m2, v1x, v2x)
                    v1yf, v2yf = self.SolveCollision1D(m1, m2, v1y, v2y)

                    def Div(n: float, d: float) -> float:
                        try:
                            return n / d
                        except ZeroDivisionError:
                            return 0

                    # the surface normal of the two spheres at the approximate point of collision (not completly correct)
                    surfNormalX = difX / distance
                    surfNormalY = difY / distance
                    otherSurfNormalX = -difX / distance
                    otherSurfNormalY = -difY / distance

                    # the magnitude of the velocities
                    velocityMagnitude = math.sqrt(v1x*v1x + v1y*v1y)
                    otherVelocityMagnitude = math.sqrt(v2x*v2x + v2y*v2y)
                    
                    # the direction of headings of the two spheres
                    headingX = Div(v1x, velocityMagnitude)
                    headingY = Div(v1y, velocityMagnitude)
                    otherHeadingX = Div(v2x, otherVelocityMagnitude)
                    otherHeadingY = Div(v2y, otherVelocityMagnitude)

                    # fidning the reflected directions for the spheres        rd - (normal * 2) * (rd * normal)
                    reflectedX = headingX - (surfNormalX * 2) * (headingX * surfNormalX)
                    reflectedY = headingY - (surfNormalY * 2) * (headingY * surfNormalY)
                    otherReflectedX = otherHeadingX - (otherSurfNormalX * 2) * (otherHeadingX * otherSurfNormalX)
                    otherReflectedY = otherHeadingY - (otherSurfNormalY * 2) * (otherHeadingY * otherSurfNormalY)

                    reflectedMagnitude = math.sqrt(reflectedX*reflectedX + reflectedY*reflectedY)
                    otherReflectedMagnitude = math.sqrt(otherReflectedX*otherReflectedX + otherReflectedY*otherReflectedY)

                    # getting the magnitudes of the final velocities
                    finalVelocityMagnitude = math.sqrt(v1xf*v1xf + v1yf*v1yf)
                    otherFinalVelocityMagnitude = math.sqrt(v2xf*v2xf + v2yf*v2yf)

                    # finding the new velocities using the correct magnitudes and directions
                    newVX = finalVelocityMagnitude * Div(reflectedX, reflectedMagnitude)
                    newVY = finalVelocityMagnitude * Div(reflectedY, reflectedMagnitude)
                    otherNewVX = otherFinalVelocityMagnitude * Div(otherReflectedX, otherReflectedMagnitude)
                    otherNewVY = otherFinalVelocityMagnitude * Div(otherReflectedY, otherReflectedMagnitude)

                    # setting the new velocities
                    particle     .SetVelocity(newVX, newVY)
                    otherParticle.SetVelocity(otherNewVX, otherNewVY)

    def Update(self, dt: float) -> None:
        dtNew = dt / 25

        for i in range(25):
            for particle in self.__particles:
                particle.Update(dtNew)
            
            for j in range(10):
                for particle in self.__particles:
                    self.Reposition(particle)
    
    def AddParticle(self, particle: Particle):
        self.__particles.append(particle)
    def GetParticles(self) -> list:
        return self.__particles


width, height = 1200, 750
screen = pygame.display.set_mode((width, height))


particleColors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
particleManager = ParticleManager()

particleManager.AddParticle(Particle(5 , 15, 10, 10000000.))
particleManager.AddParticle(Particle(80, 15, 10, 10000000.))

particle = Particle(15, 15, 1, 0.5)
particle.AddForce(10, 0.1, 3)
particleManager.AddParticle(particle)

particle = Particle(25, 15, 1, 0.5)
particle.AddForce(-10, 0.1, 3)
particleManager.AddParticle(particle)


dt = 0
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

    particles = particleManager.GetParticles()
    for particle in particles:
        pygame.draw.circle(screen, ((0, 0, 0)), (particle.GetX() * 10, particle.GetY() * 10), particle.GetRadius() * 10)

    particleManager.Update(dt * 1.5)

    pygame.display.update()

    frameEnd = time.time()
    dt = frameEnd - frameStart



