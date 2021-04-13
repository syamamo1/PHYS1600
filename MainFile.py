#from RealParticle import RealTennis
from Particle3D import Rotating_Projectile
import numpy as np

init_height = 2.286 + 0.4572
init_y = 1
init_spin = 3000*2*np.pi/60 # rad/sec
init_speed = 100*0.44704 # m/s
init_angle = -6*np.pi/180
init_vy = init_speed*np.cos(init_angle)
init_vz = init_speed*np.sin(init_angle)

ball = Rotating_Projectile(x0 = 0.0, y0 = init_y, z0 = init_height , u0 = 0.0,
                           v0 = init_vy, w0 = init_vz, i0 = init_spin, j0 = init_spin, k0 = 0, tf = 5,  dt = 0.001)
ball.RK4_trajectory()
r = ball.x_RK4
v = ball.v_RK4

backspin_ball = Rotating_Projectile(x0 = 0.0, y0 = init_y, z0 = init_height , u0 = 0.0,
                           v0 = init_vy, w0 = init_vz, i0 = -init_spin, j0 = 0, k0 = 0, tf = 5,  dt = 0.001)
backspin_ball.RK4_trajectory()
r1 = backspin_ball.x_RK4
v1 = backspin_ball.v_RK4

flat_ball = Rotating_Projectile(x0 = 0.0, y0 = init_y, z0 = init_height , u0 = 0.0,
                           v0 = init_vy, w0 = init_vz, i0 = 0, j0 = 0, k0 = 0, tf = 5,  dt = 0.001)
flat_ball.RK4_trajectory()
r2 = flat_ball.x_RK4
v2 = flat_ball.v_RK4

