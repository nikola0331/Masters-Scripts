import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

f = 2500000
a = 127
sample = 180
theta = 0.00 # np.pi/2
x = np.arange(0,sample,1)
y_1 = a* np.sin(2*np.pi * f * x * (10**(-9)) + theta)
print("y_1 data: \n")
print(y_1)
theta = 0.02
y_2 = a* np.sin(2*np.pi * f * x * (10**(-9)) + theta)
print("y_2 data: \n")
print(y_2)
#print(y_1) # To print the y values
plt.stem(x, y_1,'b', markerfmt='bo', label="Original")
plt.stem(x, y_2,'g', markerfmt='go', label="With delay")
plt.xlabel('Time (ns)')
plt.ylabel('Voltage(V)')
plt.show()


np.savetxt("y_1.txt", (y_1), fmt="\%f")
np.savetxt("y_2.txt", (y_2), fmt="\%f")
