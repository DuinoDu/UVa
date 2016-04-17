import numpy as np

class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.A.shape[0]
        self.M = self.B.shape[1]

    def printhmm(self):
        print "=================================================="
        print "HMM content: N =",self.N, ",M= ",self.M
        for i in range(self.N):
            if i==0:
                print "hmm.A ", self.A[i,:]," hmm.B ",self.B[i,:]
            else:
                print "      ", self.A[i,:],"       ",self.B[i,:]
        print "hmm.pi ",self.pi
        print "=================================================="

    def ForwardWithScale(self, T, O, alpha, scale, pprob):
        scale[0] = 0.0
        # 1.Initialization
        for i in range(self.N):
            alpha[0,i] = self.pi[i] * self.B[i, O[0]]
            scale[0] += alpha[0,i]
        
        for i in range(self.N):
            alpha[0,i] /= scale[0]
    
        # 2.Induction
        for t in range(T-1):
            scale[t+1] = 0.0
            for j in range(self.N):
                _sum = 0.0
                for i in range(self.N):
                    _sum += alpha[t,i] * self.A[i,j]
                
                alpha[t+1,j] = _sum * self.B[j, O[t+1]]
                scale[t+1] += alpha[t+1, j]
            
            for j in range(self.N):
                alpha[t+1, j] /= scale[t+1]
       
        # 3.Termination
        for t in range(T):
            pprob[0] += np.log(scale[t])

    def BackwardWithScale(self, T, O, beta, scale):
        # 1.Initialization
        for i in range(self.N):
            beta[T-1, i] = 1.0

        # 2.Induction
        for t in range(T-2, -1, -1):
            for i in range(self.N):
                _sum = 0.0
                for j in range(self.N):
                    _sum += self.A[i,j] * self.B[j, O[t+1]] * beta[t+1, j]
                beta[t,i] = _sum / scale[t+1]

    def ComputeGamma(self, T, alpha, beta, gamma):
        for t in range(T):
            denominator = 0.0
            for j in range(self.N):
                gamma[t,j] = alpha[t,j] * beta[t,j]
                denominator += gamma[t,j]
            for i in range(self.N):
                gamma[t,i] = gamma[t,i] / denominator

    def ComputeXi(self, T, O, alpha, beta, gamma, xi):
        for t in range(T-1):
            _sum = 0.0
            for i in range(self.N):
                for j in range(self.N):
                    xi[t,i,j] = alpha[t,i] * beta[t+1,j] * self.A[i,j] * self.B[j, O[t+1]]
                    _sum += xi[t,i,j]
            for i in range(self.N):
                for j in range(self.N):
                    xi[t,i,j] /= _sum
        

    def BaumWelch(self, L, T, O, alpha, beta, gamma):
        print "BaumWelch"
        
        DELTA = 0.01; _round = 0; flag = 1; probf = [0.0]
        delta = 0.0; deltaprev = 10e-70; probprev = 0.0; ratio = 0.0;

        xi = np.zeros((T, self.N, self.N))
        pi = np.zeros((T), np.float)
        denominatorA = np.zeros((self.N), np.float)
        denominatorB = np.zeros((self.N), np.float)
        numeratorA = np.zeros((self.N, self.N), np.float)
        numeratorB = np.zeros((self.N, self.N), np.float)
        scale = np.zeros((T), np.float)

        while True:
            probf[0] = 0

            # E-step
            for l in range(L):
                self.ForwardWithScale(T, O[l], alpha, scale, probf)
                self.BackwardWithScale(T, O[l], beta, scale)
                self.ComputeGamma(T, alpha, beta, gamma)
                self.ComputeXi(T, O[l], alpha, beta, gamma, xi)
                for i in range(self.N):
                    pi[i] += gamma[0,i]
                    for t in range(T-1):
                        denominatorA[i] += gamma[t,i]
                        denominatorB[i] += gamma[t,i]
                    denominatorB[i] += gamma[T-1, i]

                    for j in range(self.N):
                        for t in range(T-1):
                            numeratorA[i,j] += xi[t,i,j]
                    for k in range(self.M):
                        for t in range(T):
                            if O[l][k] == k:
                                numeratorB[i,k] += gamma[t,i]

            # M-step

            for i in range(self.N):
                self.pi[i] = 0.001/self.N + 0.999*pi[i]/L
                for j in range(self.N):
                    self.A[i,j] = 0.001/self.N + 0.999*numeratorA[i,j]/denominatorA[i]
                    numeratorA[i,j] = 0.0
                
                for k in range(self.M):
                    self.B[i,k] = 0.001/self.M + 0.999*numeratorB[i,k]/denominatorB[i]
                    numeratorB[i,j] = 0.0

                pi[i] = denominatorA[i] = denominatorB[i] = 0.0
           
            '''
            print self.A
            print self.B
            print self.pi
            break
            '''
            if flag == 1:
                flag = 0
                probprev = probf[0]
                ratio = 1
                continue

            delta = probf[0] - probprev
            ratio = delta / deltaprev
            probprev = probf[0]
            deltaprev = delta
            _round +=1

            print "ratio:",ratio

            if ratio <= DELTA:
                print "num iteration ", _round
                break

            if _round > 20:
                break


if __name__ == '__main__':
    print "python my HMM"
    
    A = [[0.500, 0.375, 0.125], 
         [0.250, 0.125, 0.625],
         [0.250, 0.375, 0.375]]
    B = [[0.60, 0.20, 0.15, 0.05],
         [0.25, 0.25, 0.25, 0.25],
         [0.05, 0.10, 0.35, 0.60]]
    pi = [0.63, 0.17, 0.20]

    hmm = HMM(A, B, pi)

    #O = [[1,0,0,1,1,0,0,0,0],
    #     [1,1,0,1,0,0,1,1,0],
    #     [1,1,0,1,0,0,1,1,0],
    #     [0,0,1,1,0,0,1,1,1]]
    
    #O = [[0,1,2,3]]

    
    A = [[0.5, 0.2, 0.3],
         [0.3, 0.5, 0.2],
         [0.2, 0.3, 0.5]]
    B = [[0.5, 0.5],
         [0.4, 0.6],
         [0.7, 0.3]]
    pi = [0.2,0.4,0.4]
    hmm = HMM(A, B, pi)
    
    O = [[0,1,0]]
    
    L = len(O)
    T = len(O[0])
    alpha = np.zeros((T, hmm.N), np.float)
    beta = np.zeros((T, hmm.N), np.float)
    gamma = np.zeros((T, hmm.N), np.float)
    hmm.BaumWelch(L,T,O,alpha, beta, gamma)
    hmm.printhmm()
