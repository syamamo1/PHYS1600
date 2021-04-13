from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from Groundstrokes import r, v, r1, v1, r2, v2

# Define court
x_court = np.arange(-8.23/2, 8.23/2, 8.23/1000)
y_court = np.arange(0, 23.77, 23.77/1000)
xx, yy = np.meshgrid(x_court, y_court)
normal = np.array([0, 0, 1]) # normal points straight up
z_ground = (-normal[0]*xx - normal[1]*yy)/normal[2]

x_net = np.arange(-8.23/2-1, 8.23/2+1, 8.23*2/1000)
z_net = np.arange(0, 0.94, 0.94/1000)
xx1, zz1 = np.meshgrid(x_net, z_net)
normal1 = np.array([0, 1, 0])
y_net = (-normal1[0]*xx1 - normal1[2]*zz1) + 11.89/normal1[1]

# plot everything
fig = plt.figure()
ax = plt.axes(projection = '3d')

ax.plot3D(r[:, 0], r[:, 1], r[:, 2], label = 'Top Spin')
ax.plot3D(r1[:, 0], r1[:, 1], r1[:, 2], label = 'Back Spin')
ax.plot3D(r2[:, 0], r2[:, 1], r2[:, 2], label = 'No Spin')

# plot court
ax.plot_surface(xx1, y_net, zz1, alpha = '0.7')
ax.plot_surface(xx, yy, z_ground, color = 'y', alpha = '0.3')

# set limits etc
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
scale = 8.23/11.89
scale1 = 4/11.89
y_lim = max(max(r[:, 1]), max(r1[:, 1]), max(r2[:, 1]))
ax.set_ylim([0, y_lim])
ax.set_xlim([-y_lim*scale/2, y_lim*scale/2])
ax.set_zlim([0, y_lim/2])
plt.show()

#  NOTES FOR SELF 1. improve model for reynolds laminar/turbulent flow, 2. bounce dynamics? 3. make ball into sphere? du
