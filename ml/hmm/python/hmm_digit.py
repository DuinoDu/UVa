import hmm
import numpy as np

def readInitHMM():
    HMM = np.loadtxt('init.hmm')
    A = HMM[0:16, :]
    B = HMM[16:31, :]
    pi = HMM[32,:]
    return A,B,pi

def convertToAngle(X):
    angle = np.zeros((22,110), dtype = np.float)
    for i in range(22):
        cnt_angle = 0
        for j in range(110-1):
            if( (X[i,j,1] != X[i,j+1,1]) or (X[i,j,0] != X[i,j+1,0])):
                if(X[i,j+1,0] > X[i,j,0]):# p2 is in the right of p1
                    tmp = np.arctan(1.0*(X[i,j+1,1] - X[i,j,1])/(X[i,j+1,0] - X[i,j,0]))
                    angle[i,cnt_angle] = -1.0*tmp/np.pi*180
                elif(X[i,j+1,0] < X[i,j,0]): # p2 is in the left of p1
                    tmp = np.arctan(1.0*(X[i,j+1,1] - X[i,j,1])/(X[i,j+1,0] - X[i,j,0]))
                    angle[i,cnt_angle] = 180-1.0*tmp/np.pi*180
                elif(X[i,j+1,0] == X[i,j,0]): # p2 is in the same x-axis as p1
                    if(X[i,j+1,1] > X[i,j,1]):
                        angle[i,cnt_angle] = -90
                    else:
                        angle[i,cnt_angle] = 90
                angle[i,cnt_angle] += 90
                angle[i,cnt_angle] = np.floor(angle[i,cnt_angle] / 22.5) + 1
                cnt_angle += 1
    return angle 

def readUJI(path):
    X = np.zeros((220,110,2))
    j = 0
    for m in range(1,12):
        if m < 10:
            fileStr = open(path+"/UJIpenchars-w0"+str(m)).read().replace('\n',' ').split(' ')
        else:
            fileStr = open(path+"/UJIpenchars-w"+str(m)).read().replace('\n',' ').split(' ')
       
        # delete '' in fileStr
        i = 0
        while(i < len(fileStr)):
            if(fileStr[i] == ''):
                fileStr.remove(fileStr[i])
            else:
                i += 1

        # read digit data from specific position in fileStr
        cnt_digit = 0
        i = k = 0
        while(i < len(fileStr)):
            if(fileStr[i] == '.SEGMENT'):
                while(fileStr[i] != '.PEN_DOWN'):
                    i += 1
                cnt_digit += 1
                if( ((cnt_digit >= 53) and (cnt_digit <= 62)) or ((cnt_digit >= 115) and (cnt_digit <= 124)) ):
                    while(fileStr[i+1] != '.PEN_UP'):
                        i += 1
                        X[j,k,0] = eval(fileStr[i])
                        i += 1
                        X[j,k,1] = eval(fileStr[i])
                        k += 1

                    k = 0
                    j += 1 #add a digit
            i += 1   
    
    for i in range(10):
        X_save = np.zeros((22,110,2), dtype=np.int32)
        for j in range(22):
            X_save[j,:,:] = X[i+j*10, :, :]
        angle = convertToAngle(X_save)
        
        f = open('./data/'+str(i)+'.txt','w+')
        for j in range(22):
            s = ""
            for k in range(110):
                if(angle[j,k]!=0):
                    s += str(int(angle[j,k]))
                    s += ' '
            s += "\n"
            f.write(s)
        f.close()

def readObs(filename):
    O = []
    for line in open(filename):
        O1 = []
        for each in line[:-2].split(' '):
            O1.append(eval(each)-1)
        O.append(O1)
    return O



if __name__ == '__main__':

    # Read data form ./data/UJIpenchars-w** and tranform to ./data/*.txt
    # Each *.txt contains 22 records for one digit.
    #  
    #readUJI('./data')

    A,B,pi = readInitHMM()
    mHMMs = []
    O = []
    for i in range(10):
        O.append(readObs('./data/'+str(i)+'.txt'))
    # learning
    for i in range(10):
        A_ave = np.zeros((16,16))
        B_ave = np.zeros((16,16))
        pi_ave = np.zeros((16))
        for j in range(11):
            mHMM = hmm.HMM(A, B, pi)
            mHMM.baum_welch(O[i][j])
            A_ave += mHMM.A
            B_ave += mHMM.B
            pi_ave += mHMM.pi
        A_ave /= 11.0
        B_ave /= 11.0
        pi_ave /= 11.0 
        bestHMM = hmm.HMM(A_ave, B_ave, pi_ave)
        mHMMs.append(bestHMM) 

    # test
    for k in range(10):
        print "###### Test for number ",k
        for j in range(11,22):
            maxP = mHMMs[i].forward_algo(O[k][1]) 
            y = 0
            for i in range(10):
                pro = mHMMs[i].forward_algo(O[k][j]) 
                if pro > maxP:
                    maxP = pro
                    y = i
            print "data O[",j,"] is ",y
