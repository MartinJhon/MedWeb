import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# x = np.arange(10)
# print(x)
#
# np.random.seed(1)
# y = np.random.random(size=10)
# print(y)
#
#
# plt.plot(x,y,color='r',marker='*',linestyle="-.")
# plt.show()

x = np.linspace(0,10,100)
y = np.sin(x)
y2 = np.cos(x)
plt.plot(x,y)
plt.plot(x,y2)
plt.show()
