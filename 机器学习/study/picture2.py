import matplotlib.pyplot as plt
import numpy as np

# data = np.arange(1,10)
#
# plt.boxplot(data)
# plt.show()
np.random.seed(100)
data = np.random.normal(size=100)
data = np.concatenate([data,[4,7,8,9,-4]])

plt.boxplot(data,widths=0.8)
# plt.hist(data)     #直方图
plt.show()
