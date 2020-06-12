from math import exp

educationSpeed = 0.001

alphach = 1
weights1 = [0 for i in range(0, 1200)]  ##600 элементов
weights2 = [0 for i in range(0, 9000)]  ##2250 элементов
weights3 = [0 for i in range(0, 180)]  ##90 элементов

sigma3Error = [0, 0]
sigma2Error = [0 for i in range(0, 90)]
sigma1Error = [0 for i in range(0, 100)]

fullTable = []
f = open("file.txt", "r")
fullTable = [line.split() for line in f]
nefullTable = fullTable.copy()
for i in range(len(fullTable)):
    nefullTable[i] = fullTable[i][:-2:]

input = nefullTable[0]  ##12 значений атрибутов
neurons1 = [0 for i in range(0, 100)]  ##50 (1ый скрытый слой)
neurons2 = [0 for i in range(0, 90)]  ##45 элементов(2ой скрытый)
neurons3 = [0 for i in range(2)]  ##2 (выходной слой)


def activation(s):
    return 1 / (1 + exp(-1 * alphach * s))


def layerActivationCounting(neurons, weights):
    num = len(weights) // len(neurons)
    s = [0 for i in range(num)]
    for j in range(0, num):
        for i in range(len(neurons)):
            s[j] += float(neurons[i]) * float(weights[i + len(neurons) * j])
        s[j] = float(activation(s[j]))
    return s


def totalError(nefullTable, weights1, weights2, weights3, fullTable):
    errorG_total = 0
    errorKGF = 0
    for i in range(0, 40):
        input = nefullTable[i]
        neurons1 = layerActivationCounting(input, weights1)
        neurons2 = layerActivationCounting(neurons1, weights2)
        neurons3 = layerActivationCounting(neurons2, weights3)
        if(float(fullTable[i][-2])!= 0):
            errorG_total += (neurons3[0] - float(fullTable[i][-2])) ** 2
        errorKGF += (neurons3[1] - float(fullTable[i][-1])) ** 2
    return max(errorG_total, errorKGF) / 2


def derivative(y):
    return y * (1 - y)


def sigmaCounting(weight, previousErrors, neurons):
    currentError = [0 for i in range(len(neurons))]
    for i in range(len(neurons)):
        s = 0
        for j in range(len(previousErrors)):
            s += previousErrors[j] * weight[i + len(neurons) * j]  ##мб ошибка
        currentError[i] = s * derivative(neurons[i])
    return currentError


def weightCorrection(weight, sigmaError, neurons):
    for i in range(len(sigmaError)):
        for j in range(len(neurons)):
            weight[j + i * len(neurons)] -= educationSpeed * float(sigmaError[i]) * float(neurons[j])
    return weight

currentError = totalError(nefullTable, weights1, weights2, weights3, fullTable)
j = 0

while (currentError > 0.01):
    for i in range(0, 40):
        input = nefullTable[i]
        neurons1 = layerActivationCounting(input, weights1)
        neurons2 = layerActivationCounting(neurons1, weights2)
        neurons3 = layerActivationCounting(neurons2, weights3)
        if(float(fullTable[i][-2])!=0):
            sigma3Error[0] = (neurons3[0] - float(fullTable[i][-2])) * derivative(neurons3[0])
        else:
            sigma3Error[0] = 0
        sigma3Error[1] = (neurons3[1] - float(fullTable[i][-1])) * derivative(neurons3[1])
        sigma2Error = sigmaCounting(weights3, sigma3Error, neurons2)
        sigma1Error = sigmaCounting(weights2, sigma2Error, neurons1)
        weights1 = weightCorrection(weights1, sigma1Error, input)
        weights2 = weightCorrection(weights2, sigma2Error, neurons1)
        weights3 = weightCorrection(weights3, sigma3Error, neurons2)

    currentError = totalError(nefullTable, weights1, weights2, weights3, fullTable)
    j += 1
    print("Текущая ошибка: " + str(currentError) + " текущая итерация:" + str(j))
    ##fjvlnds
