'''
将kNN算法封装到knn.py
'''
#导入我们需要的包
import numpy as np
from collections import Counter

#对kNN计算距离进行封装，为了计算方便 我们可以默认k=5
def kNN_classify(X_train,y_train,X_predict,k=5,p=2):
    '''
    kNN分类器
    :param X_train: 需要进行预测的数据
    :param y_train: X_train的分类数组
    :param x:
    :param k: 需要预测的值
    :param p: 明可夫斯基当中的参数
    :return:  返回值
    '''
    assert k > 0   #k需要大于0
    assert  k <= y_train.shape[0]  #k需要小于或者等于总的样本数
    assert  p> 0    #p需要大于0
    assert  X_train.shape[0] == y_train.shape[0]  #X_train中样本刷零需要和y_train中的相同
    assert X_train.shape[1] == X_predict.shape[1]   #预测的特征数量需要等于样本的特征数量
    return np.array([_predict(X_train,y_train,x,k,p) for x in X_predict])  #调用_predict方法，

def _predict(X_train,y_train,x,k,p):
    distances = [distance(item, x, p=p) for item in X_train]  # 将计算后的距离参数存放到distances中
    nearest = np.argsort(distances)[:k]  # 将排序的后的内容放入到nearest变量当中
    k_labels = y_train[nearest]  # 取出对应的标签信息并放在k_labels中

    return Counter(k_labels).most_common(1)[0][0]    # 使用Counter进行投票

# kNN距离计算函数，p=1,为曼哈顿距离；p=2，欧拉距离；p不等于1或者2  则为  明可夫斯基距离
def distance(a,b,p=2):
    '''
    计算距离
    :param a:   参数变量a
    :param b:   参数变量b
    :param p:   参数变量p
    :return:    返回值
    '''
    return (np.sum(np.abs(a - b )**p))**(1/p)