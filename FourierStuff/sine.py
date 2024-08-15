import matplotlib.pyplot as plt
import numpy as np

A = .8
f0 = 1000
phi = np.pi/2
fs = 44100
T = 1.0/fs

t = np.arange( -0.002, 0.002, T )

x = A * np.cos( 2 * np.pi * f0 * t + phi )

plt.plot( t, x )
plt.axis( [ -0.002, 0.002, -0.8, 0.8 ] )
plt.xlabel('time')
plt.ylabel('amplitude')

plt.show()

