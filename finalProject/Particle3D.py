from scipy.integrate import odeint
import matplotlib.pyplot as plt  # for plotting
import numpy as np


class Particle(object):
    """Class that describes particle"""
    m = 1.0

    def __init__(self, x0=1.0, y0=0.0, z0=0.00, u0=0.0, v0=0.0, w0=0.0, tf=10.0, dt=0.01):
        # print("particle init'd")
        self.x = np.array([x0, y0, z0])
        self.v = np.array([u0, v0, w0])
        self.t = 0.0
        self.tf = tf
        self.dt = dt
        npoints = int(tf / dt)  # always starting at t = 0.0
        self.npoints = npoints
        self.tarray = np.linspace(0.0, tf, npoints, endpoint=True)  # include final timepoint
        self.xv0 = np.ravel(np.array([self.x, self.v]))  # NumPy array with initial position and velocity

    def reinitialize(self):
        self.npoints = int(self.tf / self.dt)
        self.x = self.xv0[0:3]
        self.v = self.xv0[3:]
        self.t = 0

    def F(self, x, v, t):
        return np.array([0.0, 0.0, 0.0])

    def RK4_step(self):
        a1 = self.F(self.x, self.v, self.t) / self.m

        k1 = np.array([self.v, a1]) * self.dt

        a2 = self.F(self.x + k1[0] / 2, self.v + k1[1] / 2, self.t + self.dt / 2) / self.m
        k2 = np.array([self.v + k1[1] / 2, a2]) * self.dt

        a3 = self.F(self.x + k2[0] / 2, self.v + k2[1] / 2, self.t + self.dt / 2) / self.m
        k3 = np.array([self.v + k2[1] / 2, a3]) * self.dt

        a4 = self.F(self.x + k3[0], self.v + k3[1], self.t + self.dt) / self.m
        k4 = np.array([self.v + k3[1], a4]) * self.dt

        if self.x[2] > 0:  # if above ground....
            if 11.89-0.01<= self.x[1] <= 11.89+0.01 and self.x[2] <= 0.94:  # if hit net
                1+1
            else:
                self.x += (k1[0] + k4[0]) / 6 + (k2[0] + k3[0]) / 3
                self.v += (k1[1] + k4[1]) / 6 + (k2[1] + k3[1]) / 3
                self.t += self.dt

    def RK4_trajectory(self):  # calculate trajectory as before
        # need to reinitialize if you want to call this method and others
        x_RK4 = np.zeros([self.npoints, 3])
        v_RK4 = np.zeros([self.npoints, 3])

        for ii in range(self.npoints):
            x_RK4[ii] = self.x
            v_RK4[ii] = self.v
            self.RK4_step()

        self.x_RK4 = x_RK4
        self.v_RK4 = v_RK4

class Rotating_Projectile(Particle):
    """Subclass of Particle Class that describes a falling rotating particle"""

    def __init__(self, m=57.7e-3, r=3.35e-2, x0=0.0, y0=0.0, z0=1.0, u0=0.0, v0=0.0, w0=0.0, i0=0, j0=0, k0=0, tf=3.0,
                 dt=0.001):
        # print("projectile init'd")
        self.m = m
        self.omega = np.array([i0, j0, k0])
        self.r = r
        self.A = np.pi * r ** 2  # cross-secitonal area

        super().__init__(x0, y0, z0, u0, v0, w0, tf, dt)  # call initialization method of the super (parent) class

    def Reynolds(self, speed):
        dynamicViscosity = 1.516e-5
        Re = 2 * self.r * speed / dynamicViscosity
        return Re
        # ranges from 0 to approx 3.1e5 (0, 150mph)

    def F(self, x, v, t):
        g = 9.8
        mod_v = np.sqrt(np.sum(v ** 2))
        mod_omega = np.sqrt(np.sum(self.omega ** 2))
        p = 1.21
        Fg = np.array([0, 0, -self.m * g])

        if mod_v < 1e-6:  # no reason to calculate drag or lift for very small velocities.
            return Fg

        drag = -(0.5 * self.A * p * v * mod_v) / 2  # Drag force = -0.5(A*p*v^2)/2 (opposite of velocity)

        if mod_omega > 0:
            lift_coeff = 1 / (2 + mod_v / (mod_omega * self.r))  # scalar coefficient of lift force
            direction = (np.cross(v, self.omega)) / np.linalg.norm((np.cross(v, self.omega)))
        else:  # no spin, no effect
            lift_coeff = 0
            direction = np.array([0,0,0])
        lift = (lift_coeff * self.A * p * mod_v ** 2) * direction / 2
        # Lift Force = (1/(2+v/wr))*A*p*v^2/2 (weird direction)

        return Fg + drag + lift



