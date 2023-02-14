import java.util.ArrayList;

public class ParticleManager
{
    // all the particles being managed
    private final ArrayList<Particle> particles = new ArrayList<>();
    private int currentId = 0;

    public ParticleManager() {}

    public void Collision(Particle p1, Particle p2)
    {
        // kg m/s  is the unit for momentum
        // is an elastic collision
        // http://websites.umich.edu/~amophys/125/fift/fift.html#:~:text=15.4%20Elastic%20Collision%20of%20Two%20Unequal%20Mass%20Objects&text=A%20smaller%20mass%20approaching%20a,direction%20of%20the%20intial%20momentum.
        
        double absMomentumX = Math.abs(p1.GetVelocityX()) * p1.GetMass();
        double absMomentumY = Math.abs(p1.GetVelocityY()) * p1.GetMass();
    }

    // solves a 1D collision
    private double[] SolveCollision1D(double m1, double m2, double v1, double v2)
    {
        // solving two equations so a 2 variable system can be solved
        double equation1Left = m1 * v1 + m2 * v2;  // getting the value of the left side of the equation to be further solved
        double equation2Left = v1 - v2;  // getting the left hand side of the solved equation

        // solving the system of equations
        double finalEquationLeft = m1 + m2;
        double finalEquationRight = equation1Left + equation2Left * m1;

        // getting the final velocities
        double v2f = finalEquationRight / finalEquationLeft;
        double v1f = v2f - v1 + v2;

        // returning the final velocities
        return new double[] {v1f, v2f};
    }

    private void Reposition(Particle particle)
    {
        /* An optimization:
            * put all particles into a grid with grid cells the size of the particles (assuming they're all the same size)
            * round the particle to the nearest corner
            * take the four surrounding cells and check the particles in them
            * do the calculation on them
        */

        // the main particles radius
        double radius = particle.GetRadius();

        // looping through all the particles
        for (Particle otherParticle : particles)
        {
            if (otherParticle.id != particle.id)
            {
                // getting the difference in position of the particle centers
                double difX = otherParticle.GetX() - particle.GetX();
                double difY = otherParticle.GetY() - particle.GetY();

                // getting the distance between particle centers
                double distance = Math.sqrt(difX * difX + difY * difY);

                // checking if the sum of the radius's is larger than the distance (meaning an overlap)
                double radiusSum = radius + otherParticle.GetRadius();
                if (distance < radiusSum)
                {
                    // getting half the overlapping distance (the amount needing to be moved by both particles)
                    double halfDif = 0.5 * (radiusSum - distance);

                    // normalizing the dif x and y and then multiplying by half the overlap to get the amount needing to be moved in the x and y directions by both particles
                    double scaledDifX = difX / distance * halfDif;
                    double scaledDifY = difY / distance * halfDif;

                    // moving the particles
                    otherParticle.MovePos(scaledDifX, scaledDifY);
                    particle.MovePos(-scaledDifX, -scaledDifY);

                    // simulating collision between the particles
                    // m1*v1 + m2*v2 = m1*v1f + m2*v2f
                    // v1 + v1f = v2 + v2f

                    // getting the mass of the particles
                    double m1 = particle.GetMass();
                    double m2 = otherParticle.GetMass();

                    // getting the final velocities
                    double[] finalXVels = SolveCollision1D(m1, m2, particle.GetVelocityX(), otherParticle.GetVelocityX());
                    double[] finalYVels = SolveCollision1D(m1, m2, particle.GetVelocityY(), otherParticle.GetVelocityY());

                    // setting the new velocities
                    particle     .SetVelocity(finalXVels[0], finalYVels[0]);
                    otherParticle.SetVelocity(finalXVels[1], finalYVels[1]);
                }
            }
        }
    }

    // updates the particles
    public void Update(double dt)
    {
        // micro stepping the physics for better accuracy
        double dtNew = dt / 10;
        for (int i = 0; i < 10; i++)
        {
            // looping through all the particles and updating them
            for (Particle particle : particles) particle.Update(dtNew);

            // looping through all the particles multiple times and repositioning them
            for (int j = 0; j < 10; j++) for (Particle particle : particles) Reposition(particle);
        }
    }

    // adds a particle
    public void AddParticle(Particle particle) {  particle.SetId(currentId); particles.add(particle); currentId++;  }

    // gets the particles
    public ArrayList<Particle> GetParticles() {  return particles;  }
}
