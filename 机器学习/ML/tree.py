import numpy as np
import  matplotlib.pyplot as plt
from collections import Counter

def cut(X, y, d, v):
    ind_left = (X[:, d] < v)
    ind_right = (X[:, d] > v)
    return X[ind_left], X[ind_right], y[ind_left], y[ind_right]

def gini(x):
    counter = Counter(x)
    result = 0
    for v in counter.values():
        result += (v / len(x)) ** 2
    return 1 - result

def try_split(X, y):  #
    best_g = 1
    best_d = -1
    best_v = -1
    for d in range(X.shape[1]):
        sorted_index = np.argsort(X[:, d])
        for i in range(len(X) - 1):
            if X[sorted_index[i], d] == X[sorted_index[i + 1], d]:
                continue
            v = (X[sorted_index[i], d] + X[sorted_index[i + 1], d]) / 2
            # print('d={} v={}'.format(d,v))
            X_left, X_right, y_left, y_right = cut(X, y, d, v)
            g_all = gini(y_left) + gini(y_right)
            # print('d={} v={} g={}'.format(d,v,g_all))
            if g_all < best_g:
                best_g = g_all
                best_d = d
                best_v = v
    return best_d, best_v, best_g


class DecisionTreeClassifier():

    def __init__(self):
        self.tree_ = None

    def fit(self,X,y):
        '''
        fit方法是用来训练模型的
        :param X:  源数据
        :param y:   源数据对应的分类
        :return:
        '''
        self.tree_ = self.create_tree(X,y)

        return  self

    def create_tree(self,X, y):
        d, v, g = try_split(X, y)

        if d == -1 or g == 0:
            return None
        node = Node(d, v, g)
        X_left, X_right, y_left, y_right = cut(X, y, d, v)
        node.children_left = self.create_tree(X_left, y_left)
        if node.children_left is None:
            label = Counter(y_left).most_common(1)[0][0]
            node.children_left = Node(l=label)
        node.children_right = self.create_tree(X_right, y_right)
        if node.children_right is None:
            label = Counter(y_right).most_common(1)[0][0]
            node.children_right = Node(l=label)
        return node

    def predict(self,X):
        '''
            实现循环调用，一次性实现对多个样本进行分类的预测
        '''
        assert self.tree_ is not None, '请先调用fit()方法对数据进行预测'

        return np.array([self._predict(x,self.tree_) for x in X])


    def _predict(self,x,node):
        if node.label is not None:
            return node.label

        if x[node.dim] <= node.value:
            return self.predict(x,node.children_left)

        else:
            return self.predict(x,node.children_right)



class Node():
    def __init__(self, d=None, v=None, g=None, l=None):
        self.dim = d
        self.value = v
        self.gini = g
        self.label = l

        self.children_left = None
        self.children_right = None

    def __repr__(self):
        return 'Node(d={},v={},g={},l={})'.format(self.dim, self.value, self.gini, self.label)
