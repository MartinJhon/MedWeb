import  numpy as np
class StandardScaler:
    def __init__(self):
        '''
        初始化均值mean_ 和 标准差scale_
        '''
        self.mean_ = None   #将均值初始化
        self.scale_ = None  #将标准差初始化
    def fit(self,X):
        '''
        计算均值mean_ 和 标准差scale_
        :param X: 数组数据
        :return: 返回值
        '''
        self.mean_ = np.mean(X,axis=0)     #计算均值
        self.scale_ = np.std(X, axis=0)     #计算标准差
        return self
    def transform(self,X):
        '''
            用来将数据进行标准化
        '''
        assert  self.mean_ is not None and  self.scale_ is not None,\
            '请先调用fit方法'
        assert X.shape[1] == len(self.mean_),\
            'X的特征数量需要与计算标准差和均值时传入的数据相同'
        temp = np.empty(shape=X.shape,dtype=float) # 用来存放标准化后的数据
        for col in range(X.shape[1]):   #采用循环的方式进行将数据标准化
            #将标准化后的数据存放在temp[col]中
            temp[:,col] = (X[:,col] - self.mean_[col]) / self.scale_[col]
        return temp  #最终返回标准花数据