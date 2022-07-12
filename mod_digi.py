from cgi import test
from itertools import starmap
import numpy as np 
from scipy.signal import upfirdn
import matplotlib.pyplot as plt

def bpsk_mod(ak,L):

    # ak -> bits de entrada 
    # L  -> Fator de sobre amostragem (Tb/Ts) 
    # Ts -> período de amostragem
    # Tb -> período de bit

    s_bb = upfirdn(h = np.ones(L),x=2*ak-1,up = L) # codificador NRZ
    t = np.arange(start=0,stop=len(ak)*L)

    return (s_bb, t)



def bpsk_demod(r_bb,L):

    # r_bb : sinal recebido na entrada do receptor (front end)
    # L    : taxa de sobre amostragem (Tsym/T)
    # Tsym : Período de símbolo

    x = np.real(r_bb)
    x = np.convolve(x,np.ones(L))
    x = x[L-1:-1:L]
    ak_hat = (x>0).transpose()
    return ak_hat

def awgn(s,SNRdB,L):

        gamma = 10**(SNRdB/10)
        if s.ndim == 1:
            P = L*np.sum(np.abs(s)**2)/len(s)
        else: # Sinais multidimensionais
            P = L*np.sum(np.sum(np.abs(s)**2))/len(s)

        N0 = P/gamma
        if np.isrealobj(s):
            n = np.sqrt(N0/2)*np.random.randn(len(s))
        else:
            n = np.sqrt(N0/2)*(np.random.randn(len(s)) + 1j*np.random.randn(len(s)))
        
        r = s + n

        return r

 
class simulBPSK :

    def __init__(self,N,L,EbNoVec,Fc):

        self.N = N
        self.EbNoVec = EbNoVec
        self.L = L 
        self.Fc = Fc
        self.Fs = self.L * self.Fc
        self.ak = np.random.randint(2,size = N)
   
    def plotData(self):

        (s_bb,t)= bpsk_mod(self.ak,self.L)
        s = s_bb*np.cos(2*np.pi*self.Fc*t/self.Fs)

        fig1, axs = plt.subplots(2, 2)
        axs[0, 0].plot(t,s_bb)
        axs[0, 0].set_xlabel('t(s)')
        axs[0, 1].set_ylabel(r'$s_{bb}(t)$-baseband')

        axs[0, 0].set_xlim(0,10*self.L)
        axs[0, 1].set_xlim(0,10*self.L)        
        
        axs[0, 1].plot(t,s)
        axs[0, 1].set_xlabel('t(s)')
        axs[0, 1].set_ylabel('s(t)-with carrier')

        # Constelação do sinal
        axs[1, 0].plot(np.real(s_bb),np.imag(s_bb),'o')
        axs[1, 0].set_xlim(-1.5,1.5)
        axs[1, 0].set_ylim(-1.5,1.5)
        plt.show()

    

    def desemepnho(self):
        BER = np.zeros(len(self.EbNoVec))
        (s_bb,t)= bpsk_mod(self.ak,self.L)
        s = s_bb*np.cos(2*np.pi*self.Fc*t/self.Fs)

        for ii, EbNo in enumerate(self.EbNoVec):

            r = awgn(s,EbNo,L)

            r_bb = r*np.cos(2*np.pi*self.Fc*t/self.Fs)
            ak_hat = bpsk_demod(r_bb,L)
            BER[ii] = np.sum(self.ak != ak_hat)/self.N


        fig, ax1 = plt.subplots(nrows=1,ncols = 1) 
        ax1.semilogy(self.EbNoVec,BER,'-k*',label='Simulated') # simulated BER 
        ax1.set_xlabel(r'$E_b/N_0$ (dB)') 
        ax1.set_ylabel(r'BER - $P_b$') 
        ax1.set_title(['BER para transmissão BPSK']) 
        ax1.legend()
        fig.show()


        







if __name__ == "__main__":

    N = 1000
    L =16 
    EbNo = np.arange(start=-4,stop=11,step=2)
    Fc = 800


    teste = simulBPSK(N,L,EbNo,Fc)
    teste.plotData()
    teste.desemepnho()




    
