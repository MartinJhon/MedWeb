def accuracy_score(y,y_predict):
    '''
    计算准确率
    :param y:           y的真值
    :param y_predict:   y的预测值
    :return:            返回值
    '''
    # y与y_predict长度需要相同
    assert y.shape[0] == y_predict.shape[0],\
           ' y与y_predict长度需要相同'
    return sum(y == y_predict) / len(y)