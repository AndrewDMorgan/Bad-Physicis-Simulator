import java.util.concurrent.TimeUnit;

public class Main
{
    private static final String[] particleChars = {"  ", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"};

    public static void main(String[] args) throws InterruptedException
    {
        ParticleManager particleManager = new ParticleManager();

        /*
        // creating the particle manager
        for (int i = 0; i < 19; i++) AddRandomParticle(particleManager, 0);

        Particle particle = new Particle(-5, 15, 3);
        particle.AddForce(30, 0, 10);
        particleManager.AddParticle(particle);
        */
        Particle particle;

        particle = new Particle(5 , 15, 10, 10000000.); particleManager.AddParticle(particle);
        particle = new Particle(80, 15, 10, 10000000.); particleManager.AddParticle(particle);

        particle = new Particle(15, 15, 1, 0.5);
        particle.AddForce(10, 0.1, 3);
        particleManager.AddParticle(particle);

        particle = new Particle(25, 15, 1, 0.5);
        particle.AddForce(-10, 0.1, 3);
        particleManager.AddParticle(particle);
        /*// adding a bunch of particles
        double dt = 10;
        Particle newParticle;
        newParticle = new Particle(50, 10, 0.75); newParticle.AddForce(-1, 0, dt);
        particleManager.AddParticle(newParticle);
        newParticle = new Particle(10, 10, 0.75); newParticle.AddForce( 1, 0, dt);
        particleManager.AddParticle(newParticle);*/

        // running the simulation
        for (int i = 0; i < 150; i++)
        {
            RenderBoard(particleManager);
            particleManager.Update(0.4);

            TimeUnit.MILLISECONDS.sleep(225);
        }
    }

    // adds a particle at a random position with random velocities
    public static void AddRandomParticle(ParticleManager particleManager, double forceScalar)
    {
        Particle particle = new Particle(Math.random() * 75 + 5, Math.random() * 25 + 5, Math.random() * 2 + 0.75);
        particle.AddForce(Math.random() * 2 * forceScalar, Math.random() * 2 * forceScalar, 15);
        particleManager.AddParticle(particle);
    }

    public static void RenderBoard(ParticleManager particleManager)
    {
        // the final render (so the screen updates evenly)
        String render = "";

        // looping through the y-axis
        for (double y = 0; y < 35; y++)
        {
            String row = "";  // the final row being printed
            // looping through the x-axis
            for (double x = 0; x < 85; x++)
            {
                // looping through the particles and getting the distance to them from the point (to see if its within the radius)
                int i = 0;
                int particleNumber = -1;
                for (Particle particle : particleManager.GetParticles())
                {
                    // getting the difference in position of the point and the particles center
                    double difX = (x + 0.5) - particle.GetX();
                    double difY = (y + 0.5) - particle.GetY();

                    // finding the distance from the center of the particle to the point
                    double distance = Math.sqrt(difX * difX + difY * difY);

                    // checking if it's within the particles radius or not
                    if (distance < particle.GetRadius()) particleNumber = i;
                    i++;
                }
                row += particleChars[particleNumber + 1];
            }

            // printing the row
            render += row + "\n";
        }

        // printing the render
        System.out.println("\n" + render);
    }
}
