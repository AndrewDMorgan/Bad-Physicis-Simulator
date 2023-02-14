public class Particle
{
    // the position and radius of the circular particle
    private double x;
    private double y;
    private double r;

    private double vX = 0.;
    private double vY = 0.;

    private double mass;
    public int id;

    private double density = 1.;

    public Particle(double x, double y, double r)
    {
        this.x = x; this.y = y; this.r = r;

        // the mass of the particle
        mass = Math.PI * (r * r) * density;
    }

    public Particle(double x, double y, double r, double density)
    {
        this.x = x; this.y = y; this.r = r; this.density = density;

        mass = Math.PI * (r * r) * density;
    }

    // adds a force
    public void AddForce(double fX, double fY, double dt)
    {
        // getting the acceleration
        double aX = fX / mass;  // (kg * m / s^2) / (kg) = m/s^2
        double aY = fY / mass;  // (kg * m / s^2) / (kg) = m/s^2

        // getting the change in velocity
        vX += dt * aX;  // (m/s^2) * (s) = m/s
        vY += dt * aY;  // (m/s^2) * (s) = m/s
    }

    // updating the particle
    public void Update(double dt)
    {
        // accounting for gravity
        //vY += 9.81 * dt;

        // moving the object
        x += vX * dt;  // (m/s) * (s) = m
        y += vY * dt;  // (m/s) * (s) = m
    }

    // gets the radius
    public double GetRadius() {  return r;  }

    // gets the position
    public double GetX() {  return x;  }
    public double GetY() {  return y;  }

    // gets the velocity
    public double GetVelocityX() {  return vX;  }
    public double GetVelocityY() {  return vY;  }

    // sets the velocity of the particle
    public void SetVelocity(double vX, double vY) {  this.vX = vX; this.vY = vY;  }

    // gets the mass
    public double GetMass() {  return mass;  }

    // sets the id of the particle
    public void SetId(int id) {  this.id = id;  }

    // moves the object
    public void MovePos(double dx, double dy) {  x += dx; y += dy;  }
}
