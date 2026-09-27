"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: read freefall.csv into arrays t and y
#         (hint: np.loadtxt with a comma delimiter, skipping the header)

data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)


t = data[:, 0]
y = data[:, 1]

# TODO 2: compute velocity v = derivative of y w.r.t. t   (np.gradient)
#         and acceleration a = derivative of v w.r.t. t    (np.gradient again)
#         Print the mean acceleration. Is it close to -9.81? Is it noisy?
v = np.gradient(y, t)
a = np.gradient(v, t)
print("Mean acceleration:", np.mean(a))
print("Acceleration standard deviation:", np.std(a))

# TODO 3: integrate a back up to recover velocity and position
#         (hint: cumulative_trapezoid(a, t, initial=0) + v[0], then again)
v_recovered = cumulative_trapezoid(a, t, initial=0) + v[0]
y_recovered = cumulative_trapezoid(v_recovered, t, initial=0) + y[0]

max_difference = np.max(np.abs(y_recovered - y))
print("Largest position difference:", max_difference)


# TODO 4: make a figure with 3 stacked panels: position, velocity, acceleration
#         vs time. Mark the true -9.81 line on the acceleration panel.
#         Save it as motion.png


fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 10))

axes[0].plot(t, y)
axes[0].set_ylabel("Position (m)")
axes[0].set_title("Free-Fall Motion")

axes[1].plot(t, v)
axes[1].set_ylabel("Velocity (m/s)")

axes[2].plot(t, a)
axes[2].axhline(-9.81, linestyle="--")
axes[2].set_ylabel("Acceleration (m/s²)")
axes[2].set_xlabel("Time (s)")

plt.tight_layout()
plt.savefig("motion.png")
plt.show()

# Bonus: 2D tracked trajectory

trajectory = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)

t2 = trajectory[:, 0]
x = trajectory[:, 1]
y2 = trajectory[:, 2]

vx = np.gradient(x, t2)
vy = np.gradient(y2, t2)

speed = np.sqrt(vx**2 + vy**2)

plt.figure(figsize=(8, 6))
plt.plot(x, y2)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("2D Trajectory")
plt.axis("equal")
plt.tight_layout()
plt.savefig("trajectory.png")
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t2, speed)
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title("Speed vs Time")
plt.tight_layout()
plt.savefig("speed.png")
plt.show()