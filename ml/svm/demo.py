import numpy as np
import random

def loadDataSet(filename):
    dataMat = []; labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def selectJrand(i,m):
    j=i
    while(j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj
       

def smoSimple(dataMatIn, classLabel, C, toler, maxIter):
    dataMatrix = np.mat(dataMatIn)  
    labelMat = np.mat(classLabel).transpose()
    b = 0; m,n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m,1)))
    iter = 0

    while (iter < maxIter):
        alphaPairsChanged = 0

        for i in range(m):
            fXi = float(np.multiply(alphas, labelMat).T * (dataMatrix*dataMatrix[i,:].T)) + b  
            Ei = fXi - float(labelMat[i])
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                fXj = float(np.multiply(alphas, labelMat).T * (dataMatrix*dataMatrix[j,:].T)) + b  
                Ej = fXj - float(labelMat[i])

                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if (labelMat[i]!=labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C+alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] -C)
                    H = min(C, C+alphas[j] + alphas[i])
                if L==H: 
                    print "L=H"
                    continue
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]* dataMatrix[j,:].T
                if eta >= 0:
                    print "eta >=0"
                    continue

                alphas[j] -= labelMat[j] * (Ei-Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if( abs(alphas[j] - alphaJold) < 0.00001):
                    #print "j not moving enough"
                    continue
                alphas[i] += labelMat[j] * labelMat[i] *(alphaJold - alphas[j])
                
                b1 = b - Ei - labelMat[i] * (alphas[i]-alphaIold) * dataMatrix[i,:] * dataMatrix[i,:].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i,:] * dataMatrix[j,:].T
            
                b2 = b - Ei - labelMat[i] * (alphas[i]-alphaIold) * dataMatrix[i,:] * dataMatrix[j,:].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j,:] * dataMatrix[j,:].T

                if (alphas[i] > 0) and (alphas[i] < C):
                    b = b1

                elif (alphas[j] > 0) and (alphas[j] < C):
                    b = b2

                else:
                    b = (b1+b2)/2.0
                
                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged)
        
        if(alphaPairsChanged == 0):
            iter += 1
        else:
            iter = 0
        print "iteration number: %d" % iter
    return b, alphas
            
if __name__ == '__main__':
    dataArr, labelArr = loadDataSet('./data/testSet.txt')
    b,alphas = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)
    print b, alphas
