import random
li = [random.random() for i in range(1000000)]
%timeit li.sort()
