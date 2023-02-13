import java.util.concurrent.TimeUnit;

public class Main
{
    private static String[] particleChars = {"  ", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"};

    public static void main(String[] args) throws InterruptedException
    {
        // creating the particle manager
        ParticleManager particleManager = new ParticleManager();

        // adding a bunch of particles
        double dt = 10;
        Particle newParticle;
        newParticle = new Particle(50, 10, 3); newParticle.AddForce(-2, 0, dt);
        particleManager.AddParticle(newParticle);
        newParticle = new Particle(10, 10, 3); newParticle.AddForce( 2, 0, dt);
        particleManager.AddParticle(newParticle);

        // running the simulation
        for (int i = 0; i < 150; i++)
        {
            RenderBoard(particleManager);
            particleManager.Update(0.3);

            TimeUnit.MILLISECONDS.sleep(75);
        }
    }

    public static void RenderBoard(ParticleManager particleManager)
    {
        // looping through the y-axis
        for (double y = 0; y < 25; y++)
        {
            String row = "";  // the final row being printed
            // looping through the x-axis
            for (double x = 0; x < 75; x++)
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
            System.out.println(row);
        }
    }
}
