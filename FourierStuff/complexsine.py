import matplotlib.pyplot as plt
import numpy as np

N  = 32 
k = 5
n = np.arange( -N/2, N/2 )
s = np.exp( 1j * 2 * np.pi * k * n / N )

plt.plot( n, np.imag( s ) )
plt.axis( [ -N/2, N/2-1, -1, 1 ] ) 
plt.xlabel('n')
plt.ylabel('amplitude')

plt.show()

