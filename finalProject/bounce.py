#from RealParticle import RealTennis
from Particle3D import Rotating_Projectile
import numpy as np

def full_path(x, v, w):
    # Calculate part 1 of path (launch to first contact with ground)
    phase_1 = Rotating_Projectile(x0=x[0],y0= x[1], z0=x[2], u0=v[0],v0= v[1], w0=v[2], i0=w[0], j0=w[1], k0=w[2],
                                  tf = 5, dt = 0.001)
    phase_1.RK4_trajectory()
    x_new = phase_1.x_RK4
    v_new = phase_1.v_RK4

    # Calculate part 2 of path (bounce)
    vels = np.array([0, 0, 0])
    wels = np.array([0, 0, 0])
    xels = x_new[-1]
    v_new2 = v_new[-1]
    x_new2 = x_new[-1]
    m = 57.7e-3
    r = 3.35e-2

    if phase_1.in_net:
        return x_new, v_new

    if w[1] <= 0:  # backspin
        if ((0.8*v_new2[0])**2)-2*(r**2)*(w[1]**2)/5 > 0:
            vels[0] = np.sqrt(((0.8*v_new2[0])**2)-2*(r**2)*(w[1]**2)/5)
        elif ((0.8*v_new2[0])**2)-2*(r**2)*(w[1]**2)/5 <= 0:
            vels[0] = np.sqrt(-((0.8 * v_new2[0]) ** 2) + 2 * (r ** 2) * (w[1] ** 2) / 5)
        wels[1] = w[1] + (8/10)*np.sqrt((5*(0.2*v_new2[0])**2)/(2*r**2))

    if w[0] >= 0:  # backspin
        if ((0.8*v_new2[1])**2)-2*(r**2)*(w[0]**2)/5 > 0:
            vels[1] = np.sqrt(((0.8*v_new2[1])**2)-2*(r**2)*(w[0]**2)/5)
        elif ((0.8*v_new2[1])**2)-2*(r**2)*(w[0]**2)/5 <= 0:
            vels[1] = np.sqrt(-((0.8 * v_new2[1]) ** 2) + 2 * (r ** 2) * (w[0] ** 2) / 5)
        wels[0] = w[0] - 8*np.sqrt((5*(0.2*v_new2[1])**2)/(2*r**2))/10

    if w[1] > 0:  # topspin
        if ((0.8*v_new2[0])**2)+2*(r*w[1]-v_new2[0])/5 > 0:
            vels[0] = np.sqrt(((0.8*v_new2[0])**2)+2*(r*w[1]-v_new2[0])/5)
        elif ((0.8*v_new2[0])**2)+2*(r*w[1]-v_new2[0])/5 <= 0:
            vels[0] = np.sqrt(-((0.8*v_new2[0])**2)-2*(r*w[1]-v_new2[0])/5)
        wels[1] = w[1] - 2*np.sqrt((5*(0.2*v_new2[0])**2)/(2*r**2))/10

    if w[0] < 0:  # topspin
        if ((0.8*v_new2[1])**2)+2*(r*w[0]-v_new2[0])/5 > 0:
            vels[1] = np.sqrt(((0.8*v_new2[1])**2)+2*(r*w[0]-v_new2[1])/5)
        elif ((0.8*v_new2[1])**2)+2*(r*w[0]-v_new2[1])/5 <= 0:
            vels[1] = np.sqrt(-((0.8*v_new2[1])**2)-2*(r*w[0]-v_new2[1])/5)
        wels[0] = w[0] + 2*np.sqrt((5*(0.2*v_new2[0])**2)/(2*r**2))/10

    # Vz
    if np.linalg.norm(np.cross(v_new2, w)) != 0:
        direction = np.cross(v_new2, w)/np.linalg.norm(np.cross(v_new2, w))
    else:
        direction = np.array([0, 0, 0])
    v_xy = np.linalg.norm([v_new2[0], v_new2[1]])
    vels = vels + np.sqrt((5*(0.2*v_xy)**2)/(2*r**2))*direction/1000
    vels[2] = -00.8*v_new[-1][2]

    phase_2 = Rotating_Projectile(x0=xels[0],y0= xels[1], z0=xels[2]+0.01, u0=vels[0],v0= vels[1], w0=vels[2], i0=wels[0], j0=wels[1], k0=wels[2],
                                  tf = 5, dt = 0.001)
    phase_2.RK4_trajectory()
    x_end = phase_2.x_RK4
    v_end = phase_2.v_RK4
    x_total = np.append(x_new, x_end, 0)
    v_total = np.append(v_new, v_end, 0)

    return x_total, v_total

