import numpy as np
def train_test_split(X,y,test_size=0.25,seed=None):
    '''
    :param X: 原始数据集
    :param y: 原始数据集标签信息
    :param test_size: 用于指定测试数据集的数量，默认为0.25，即1/4
    :return: 返回值
    '''
    assert X.shape[0] == y.shape[0]   #X中的样本数量需要等于y中的标签数量
    assert  0 <= test_size <=1   #test_size的有效范围在0~1之间
    if seed:
        np.random.seed(seed)
    shuffle = np.random.permutation(len(X))   #定义变量shuffer来接受随机抽取数据的信息
    size = int(len(X) * test_size)   #计算将要拿出进行测试数据的数量
    test_index = shuffle[:size]   #测试数据索引
    train_inedx = shuffle[size:]    #寻来你数据索引
    X_test = X[test_index]   #测试数据集
    y_test = y[test_index]   #测试数据集标签
    X_train = X[train_inedx]    #训练数据集
    y_train = y[train_inedx]    #训练数据集标签

    return X_train,X_test,y_train,y_test