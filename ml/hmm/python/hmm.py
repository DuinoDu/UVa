import numpy as np

class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.B.shape[0]
        self.M = self.B.shape[1]

    def printHMM(self):
        print "=================================================="
        print "HMM content: N =",self.N, ",M =",self.M
        
        print "hmm.A"
        for i in range(self.N):
            print self.A[i,:]

        print "hmm.B"
        for i in range(self.N):
            print self.B[i,:]
        
        print "hmm.pi ",self.pi
        print "=================================================="

    def viterbi(self, O):
        # init variables
        O = np.array(O)
        T = O.shape[0]
        delta = np.zeros((T, self.N), np.float)
        psi = np.zeros((T, self.N), np.float)

        # count delta and psi
        for t in range(T):
            if t == 0:
                for i in range(self.N):
                    delta[t][i] = self.pi[i]*self.B[i][O[t]]
                    psi[t][i] = 0
            else:
                for i in range(self.N):
                    maxPath = 0
                    maxNum = 0
                    for j in range(self.N):
                        tmp = delta[t-1][j] * self.A[j][i]
                        if(maxPath < tmp):
                            maxPath = tmp
                            maxNum = j
                    delta[t][j] = maxPath * self.B[i][O[t]]
                    psi[t][i] = maxNum

        # find I from psi and delta
        I = np.zeros((T), np.uint8)
        for t in range(T-1, -1, -1):
            if t == T-1:
                maxDelta = 0
                for j in range(self.N):
                    if(maxDelta < delta[t][j]):
                        maxDelta = delta[t][j]
                        I[t] = j
            else:
                I[t] = psi[t+1][I[t+1]]
        return I

    def countAlpha(self, O):
        O = np.array(O)
        T = O.shape[0]
        alpha = np.zeros((T,self.N), np.float)
        for t in range(T):
            if t == 0:
                for j in range(self.N):
                    alpha[t][j] = self.pi[j] * self.B[j][O[t]]
            else:
                for j in range(self.N):
                    _sum = 0.0
                    for i in range(self.N):
                        _sum += alpha[t-1][i] * self.A[i][j]
                    alpha[t][j] = _sum * self.B[j][O[t]]
        return alpha

    def countAlphaWithScale(self, O):
        O = np.array(O)
        T = O.shape[0]
        alpha = np.zeros((T,self.N), np.float)
        scale = np.zeros((T), np.float)
        for t in range(T):
            if t == 0:
                for j in range(self.N):
                    alpha[t][j] = self.pi[j] * self.B[j][O[t]]
                    scale[t] += alpha[t][j]
                for j in range(self.N):
                    alpha[t][j] /= scale[t]

            else:
                for j in range(self.N):
                    _sum = 0.0
                    for i in range(self.N):
                        _sum += alpha[t-1][i] * self.A[i][j] 
                    alpha[t][j] = _sum * self.B[j][O[t]]
                    scale[t] += alpha[t][j]
                for j in range(self.N):
                    alpha[t][j] /= scale[t]

        return alpha, scale

    
    def countBeta(self, O):
        O = np.array(O)
        T = O.shape[0]
        beta = np.zeros((T, self.N), np.float)
        
        for t in range(T-1, -1, -1):
            if t == T-1:
                for j in range(self.N):
                    beta[t][j]  = 1.0
            else:
                for j in range(self.N):
                    _sum = 0.0
                    for i in range(self.N):
                        beta[t][j] += self.A[j][i] * beta[t+1][i] * self.B[i][O[t+1]]
        return beta
    
    
    def countBetaWithScale(self, O, scale):
        O = np.array(O)
        T = O.shape[0]
        beta = np.zeros((T, self.N), np.float)
        
        for t in range(T-1, -1, -1):
            if t == T-1:
                for j in range(self.N):
                    beta[t][j]  = 1.0 / scale[t]
            else:
                for i in range(self.N):
                    _sum = 0.0
                    for j in range(self.N):
                        _sum += self.A[i][j] * beta[t+1][j] * self.B[j][O[t+1]]
                    beta[t][i] = _sum 
                for i in range(self.N):
                    beta[t][i] /= scale[t]
        return beta



    def forward_algo(self, O):
        alpha,scale = self.countAlphaWithScale(O)
        p = 0.0
        #for j in range(self.N):
            #p += alpha[len(O)-1][j] # what if p > 1
        for t in range(len(O)):
            p += np.log(scale[t])
        return p

    '''
    def backward_algo(self, O):
        beta = self.countBeta(O);
        p = 0.0
        for j in range(self.N):
            p += self.pi[j] * beta[0][j] * self.B[j][O[0]]
        return p
    '''

    def countGamma(self, T, alpha, beta):
        gamma = np.zeros((T, self.N), np.float)
        for t in range(T):
            denominator = 0.0
            for i in range(self.N):
                gamma[t][i] = alpha[t][i] * beta[i][i];
                denominator += gamma[t][i];
            # why ?
            # because sum(i=0:N-1) of gamma[t] should be 1.
            # we need to make some effort to ensure this.
            for i in range(self.N):
                gamma[t][i] /= denominator
        return gamma


    def countXi(self, T, alpha, beta):
        xi = np.zeros((T, self.N, self.N), np.float)
        for t in range(T-1):
            denominator = 0.0
            for i in range(self.N):
                for j in range(self.N):
                    xi[t][i][j] = alpha[t][i] * self.A[i][j] * self.B[j][O[t+1]] * beta[t+1][j]
                    denominator += xi[t][i][j]
            for i in range(self.N):
                for j in range(self.N):
                    xi[t][i][j] /= denominator
        return xi


    def baum_welch(self, O):
        T = len(O)
        cnt = 0;
        DELTA = 0.001

        P_previous = self.forward_algo(O) 
        # Iteration
        while True:
            alpha,scale = self.countAlphaWithScale(O)
            beta = self.countBetaWithScale(O,scale)
            
            gamma = self.countGamma(T, alpha, beta)
            xi = self.countXi(T, alpha, beta) 
            
            # count pi
            pi = 0.001 + 0.999 * gamma[0]; 
            
            A = np.zeros((self.N, self.N), np.float)
            B = np.zeros((self.N, self.M), np.float)
            for i in range(self.N):
                # count A
                denominatorA = 0.0
                for t in range(T-1):
                    denominatorA += gamma[t][i]
                for j in range(self.N):
                    numeratorA = 0.0
                    for t in range(T-1):
                        numeratorA += xi[t][i][j]
                    A[i][j] = 0.001 + 0.999 * numeratorA / denominatorA   

                # count B
                denominatorB = denominatorA + gamma[T-1][i]
                for k in range(self.M):
                    numeratorB = 0.0
                    for t in range(T):
                        if O[t] == k: # k means v_k, O[t]==V[k]
                            numeratorB += gamma[t][i]
                    B[i][k] = 0.001  + 0.999 * numeratorB / denominatorB

            self.A = np.array(A)
            self.B = np.array(B)
            self.pi = np.array(pi)
            
            P = self.forward_algo(O)
            if(P-P_previous < DELTA):
                break
            P_previous = P
            cnt = cnt + 1;
            if cnt > 200:
                break;
            

if __name__=='__main__':

    A = [[0.5, 0.2, 0.3],
         [0.3, 0.5, 0.2],
         [0.2, 0.3, 0.5]]
    B = [[0.5, 0.5],
         [0.4, 0.6],
         [0.7, 0.3]]
    pi = [0.2,0.4,0.4]
    mHMM = HMM(A, B, pi)
    O = [0,1,0]
    
    # test for viterbi
    #I = mHMM.viterbi(O)
    #print "I should be [2,2,2]"
    #print "I: ",I

    # test for forward_algo backward_algo
    #print "probability should be 0.13022"
    #print "forword_algo: ", mHMM.forward_algo(O)
    #print "backword_algo: ", mHMM.backward_algo(O)

      
    # test for EM
    mHMM.baum_welch(O)
    mHMM.printHMM()
