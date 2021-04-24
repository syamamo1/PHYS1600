from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#from Groundstrokes import r, v, r1, v1, r2, v2
from bounce import full_path

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

center_line = np.arange(11.885-6.4, 11.885+6.4, 12.8/1000)
service_line = np.arange(-8.23/2, 8.23/2, 8.23/1000)
zeros = np.zeros(1000)

# plot everything
fig = plt.figure()
ax = plt.axes(projection = '3d')

# plot court
ax.plot_surface(xx1, y_net, zz1, alpha = '0.7')
ax.plot_surface(xx, yy, z_ground, color = 'y', alpha = '0.3')
ax.plot3D(zeros, center_line, zeros)
ax.plot3D(service_line, np.array(1000*[11.885-6.4]), zeros)
ax.plot3D(service_line, np.array(1000*[11.885+6.4]), zeros)

# Create shots
##########topspin
init_height = 2.286 + 0.4572
init_y = 1
init_x = 0.5
init_spin = 3000*2*np.pi/60 # rad/sec
init_speed = 100*0.44704 # m/s
init_angle = -5*np.pi/180
init_vy = init_speed*np.cos(init_angle)
init_vz = init_speed*np.sin(init_angle)

xxx, yyy = full_path([init_x,init_y,init_height], [-4, init_vy, init_vz], [init_spin, 0, 0])
ax.plot3D(xxx[:, 0], xxx[:, 1], xxx[:, 2], label = 'Top Spin Serve')

#######slice
xxx1, yyy1 = full_path([init_x,init_y,init_height], [-4, init_vy, init_vz], [init_spin/1.5, 0, init_spin])

ax.plot3D(xxx1[:, 0], xxx1[:, 1], xxx1[:, 2], label = 'Slice Serve')

#######kick serve
xxx2,yyy2= full_path([init_x,init_y,init_height], [-4, init_vy, init_vz], [init_spin/1.1, 0, -init_spin])
ax.plot3D(xxx2[:, 0], xxx2[:, 1], xxx2[:, 2], label = 'Kick  Serve')

# set limits etc
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
scale = 8.23/11.89
scale1 = 4/11.89
#y_lim = max(max(r[:, 1]), max(r1[:, 1]), max(r2[:, 1]))
y_lim = max(xxx[:,1])
ax.set_ylim([0, y_lim])
ax.set_xlim([-y_lim*scale/2, y_lim*scale/2])
ax.set_zlim([0, y_lim/2])
plt.show()
