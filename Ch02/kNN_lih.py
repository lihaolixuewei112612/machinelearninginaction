from matplotlib.font_manager import FontProperties
from numpy import *
import numpy as np
import matplotlib.pyplot as plt


def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


#梯度上升法
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)  # convert to NumPy matrix
    labelMat = mat(classLabels).transpose()  # convert to NumPy matrix
    m, n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500  # 迭代次数
    weights_array = np.array([])
    weights = ones((n, 1))
    for k in range(maxCycles):  # heavy on matrix operations
        h = sigmoid(dataMatrix * weights)  # matrix mult
        error = (labelMat - h)  # vector subtraction
        weights = weights + alpha * dataMatrix.transpose() * error  # matrix mult 这是梯度上升公式更新参数
        weights_array = np.append(weights_array,weights)
    return weights.getA(),weights_array.reshape(-1,3) # 返回值为[w0,w1,w2]


def plotDataSet():
    dataMat, labelMat = loadDataSet()  # 加载数据集
    dataArr = np.array(dataMat)  # 转换成numpy的array数组
    n = np.shape(dataMat)[0]  # 数据个数
    xcord1 = [];
    ycord1 = []  # 正样本
    xcord2 = [];
    ycord2 = []  # 负样本
    for i in range(n):  # 根据数据集标签进行分类
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]);
            ycord1.append(dataArr[i, 2])  # 1为正样本
        else:
            xcord2.append(dataArr[i, 1]);
            ycord2.append(dataArr[i, 2])  # 0为负样本
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 添加subplot
    ax.scatter(xcord1, ycord1, s=20, c='red', marker='s', alpha=.5)  # 绘制正样本
    ax.scatter(xcord2, ycord2, s=20, c='green', alpha=.5)  # 绘制负样本
    plt.title('DataSet')  # 绘制title
    plt.xlabel('x');
    plt.ylabel('y')  # 绘制label
    plt.show()  # 显示


def plotBestFit(weights):  # 此处weights即为上面求出的[w0,w1,w2]
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = [];
    ycord1 = []
    xcord2 = [];
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]);
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]);
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]  # 0=w0x0+w1x1+w2x2 (x0=1) 此处x=x1；y=x2
    ax.plot(x, y)
    plt.xlabel('X1');
    plt.ylabel('X2');
    plt.show()


# 随机梯度上升法
def stocGradAscent0(dataMatrix, classLabels):
    m, n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)  # initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights


# 改进的随机梯度上升算法
def stocGradAscent1(dataMatrix, classLabels, numIter=300):
    m, n = shape(dataMatrix)
    weights = ones(n)  # initialize to all ones
    weights_array = np.array([])
    for j in list(range(numIter)):
        dataIndex = list(range(m))
        for i in list(range(m)):
            alpha = 4 / (1.0 + j + i) + 0.0001  # apha decreases with iteration, does not
            randIndex = int(random.uniform(0, len(dataIndex)))  # go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            weights_array = np.append(weights_array, weights, axis=0)
            del (dataIndex[randIndex])
    return weights,weights_array.reshape(-1,3)

def stocGradAscent2(dataMatrix, classLabels, numIter=150):
    # 返回dataMatrix的大小。m为行数,n为列数。
    m,n = np.shape(dataMatrix)
    # 参数初始化
    weights = np.ones(n)
    # 存储每次更新的回归系数
    weights_array = np.array([])
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            # 降低alpha的大小，每次减小1/(j+i)。
            # 相比如前面所做的改变：Alpha在每一次迭代中，都进行了改变
            alpha = 4/(1.0+j+i)+0.01
            # 随机选取样本
            # 这里也是做出的改变：是随机的选择样本，而不是遍历所有的样本
            randIndex = int(random.uniform(0,len(dataIndex)))
            # 随机选取的一个样本，计算h
            # h就是代表z的含义，梯度上升矢量化公式
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            # 计算误差
            error = classLabels[randIndex] - h
            # 更新回归系数
            weights = weights + alpha * error * dataMatrix[randIndex]
            # 添加回归系数到数组当中去
            weights_array = np.append(weights_array, weights, axis=0)
            # 将已经使用过得样本进行删除
            del(dataIndex[randIndex])
    # 改变维度
    weights_array = weights_array.reshape(numIter * m, n)
    # 返回权重
    return weights, weights_array



def classifyVector(inX, weights):
    prob = sigmoid(sum(inX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


def colicTest():
    frTrain = open('horseColicTraining.txt');
    frTest = open('horseColicTest.txt')
    trainingSet = [];
    trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in list(range(21)):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)  # 计算回归系数
    errorCount = 0;
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in list(range(21)):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount) / numTestVec)
    print("the error rate of this test is: %f" % errorRate)
    return errorRate


def multiTest():  # 调用colicTest()10次并求平均值
    numTests = 10;
    errorSum = 0.0
    for k in list(range(numTests)):
        errorSum += colicTest()
    print("after %d iterations the average error rate is: %f" % (numTests, errorSum / float(numTests)))
def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

def plotWeights(weights_array1,weights_array2):
    #设置汉字格式
    font = getChineseFont()
    # font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    #将fig画布分隔成1行1列,不共享x轴和y轴,fig画布的大小为(13,8)
    #当nrow=3,nclos=2时,代表fig画布被分为六个区域,axs[0][0]表示第一行第一列
    fig, axs = plt.subplots(nrows=3, ncols=2,sharex=False, sharey=False, figsize=(20,10))
    x1 = np.arange(0, len(weights_array1), 1)
    #绘制w0与迭代次数的关系
    axs[0][0].plot(x1,weights_array1[:,0])
    axs0_title_text = axs[0][0].set_title(u'梯度上升算法：回归系数与迭代次数关系',FontProperties=font)
    axs0_ylabel_text = axs[0][0].set_ylabel(u'W0',FontProperties=font)
    plt.setp(axs0_title_text, size=20, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][0].plot(x1,weights_array1[:,1])
    axs1_ylabel_text = axs[1][0].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][0].plot(x1,weights_array1[:,2])
    axs2_xlabel_text = axs[2][0].set_xlabel(u'迭代次数',FontProperties=font)
    axs2_ylabel_text = axs[2][0].set_ylabel(u'W2',FontProperties=font)
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')


    x2 = np.arange(0, len(weights_array2), 1)
    #绘制w0与迭代次数的关系
    axs[0][1].plot(x2,weights_array2[:,0])
    axs0_title_text = axs[0][1].set_title(u'改进的随机梯度上升算法：回归系数与迭代次数关系',FontProperties=font)
    axs0_ylabel_text = axs[0][1].set_ylabel(u'W0',FontProperties=font)
    plt.setp(axs0_title_text, size=20, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=20, weight='bold', color='black')
    #绘制w1与迭代次数的关系
    axs[1][1].plot(x2,weights_array2[:,1])
    axs1_ylabel_text = axs[1][1].set_ylabel(u'W1',FontProperties=font)
    plt.setp(axs1_ylabel_text, size=20, weight='bold', color='black')
    #绘制w2与迭代次数的关系
    axs[2][1].plot(x2,weights_array2[:,2])
    axs2_xlabel_text = axs[2][1].set_xlabel(u'迭代次数',FontProperties=font)
    axs2_ylabel_text = axs[2][1].set_ylabel(u'W2',FontProperties=font)
    plt.setp(axs2_xlabel_text, size=20, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=20, weight='bold', color='black')

    plt.show()

if __name__ == '__main__':
    # plotDataSet()
    dataMat, labelMat = loadDataSet()
    # d = gradAscent(a, b)
    weights1, weights_array1 = stocGradAscent2(np.array(dataMat), labelMat)

    weights2, weights_array2 = gradAscent(dataMat, labelMat)
    plotWeights(weights_array1, weights_array2)
    # plotWeights(dataMat, weights_array2)


