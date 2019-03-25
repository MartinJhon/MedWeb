def cut(X,y,d,v):  #划分函数
    #以下俩个返回的是bool索引，从对应的X中取出对应的数据
    ind_left = (X[:,d]<v)     #从X中取出d这个维度，当这个值小于等于v的时候等于一部分
    ind_right = (X[:,d]>v)    #从X中取出d这个维度，当这个值大于等于v的时候等于一部分
    #从X中取出左边、右边的内容，同时也要从对应的标签信息中将左边、右边的内容取出
    return X[ind_left],X[ind_right],y[ind_left],y[ind_right]
def try_split(X,y):
    best_g = 1   #best_g初始值为1
    best_d = -1  #best_d初始值为-1
    best_v = -1  #best_v初始值为-1
    for d in range(X.shape[1]):   #d代表了X轴或者Y轴，X.shape[1]为其特征数
        #为了渠道取出俩个距离最近的点，需要对其进行排序，用sorted_index进行接受
        sorted_index = np.argsort(X[:,d])
        for i in range(len(X)-1):  # 循环的次数为X的样本数量再减1
            #如果排序后使用的值等于相邻的值，则直接跳过
            if X[sorted_index[i],d] == X[sorted_index[i+1],d]:
                continue  #跳过
            #使用排好序的索引从d=0也就是x轴这个维度依次找到相邻的俩个点，（接下一句）
            #取他们中点，使用v接收他们中点的值
            #当d=1时，在y轴这个维度上选择相邻的俩个点找到他们的中点
            v = (X[sorted_index[i],d] + X[sorted_index[i+1],d]) / 2
            #print('d={} v={}'.format(d,v))
            X_left,X_right,y_left,y_right = cut(X,y,d,v) #对数据进行切分，并且接收
            g_all = gini(y_left) + gini(y_right)  #计算出基尼系数
            print('d={} v={} g={}'.format(d,v,g_all))
            if g_all < best_g:
                #如果经过比较基尼系数越小，则取最小的基尼系数，同时取出d,v
                best_g = g_all
                best_d = d
                best_v = v
    return best_d,best_v,best_g   #最后输出得到的三个值
