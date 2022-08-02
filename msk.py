import numpy as np
from numpy import sum,isrealobj,sqrt
from numpy.random import standard_normal
import matplotlib.pyplot as plt
from scipy.signal import upfirdn,lfilter



#modulador
def msk_mod(a, fc, OF, enable_plot = False):
  """
  Modulate an incoming binary stream using MSK
  Parameters:
  a : input binary data stream (0's and 1's) to modulate
  fc : carrier frequency in Hertz
  OF : oversampling factor (at least 4 is better)
  Returns:
  result : Dictionary containing the following keyword entries:
  s(t) : MSK modulated signal with carrier
  sI(t) : baseband I channel waveform(no carrier)
  sQ(t) : baseband Q channel waveform(no carrier)
  t: time base
  """
  ak = 2*a-1 # NRZ encoding 0-> -1, 1->+1
  ai = ak[0::2]; aq = ak[1::2] # split even and odd bit streams
  L = 2*OF # represents one symbol duration Tsym=2xTb
  #upsample by L the bits streams in I and Q arms
  from scipy.signal import upfirdn, lfilter
  ai = upfirdn(h=[1], x=ai, up = L)
  aq = upfirdn(h=[1], x=aq, up = L)
  aq = np.pad(aq, (L//2,0), 'constant') # delay aq by Tb (delay by L/2)
  ai = np.pad(ai, (0,L//2), 'constant') # padding at end to equal length of Q
  #construct Low-pass filter and filter the I/Q samples through it
  Fs = OF*fc;Ts = 1/Fs;Tb = OF*Ts
  t = np.arange(0,2*Tb+Ts,Ts)
  h = np.sin(np.pi*t/(2*Tb))# LPF filter
  sI_t = lfilter(b = h, a = [1], x = ai) # baseband I-channel
  sQ_t = lfilter(b = h, a = [1], x = aq) # baseband Q-channel
  t=np.arange(0, Ts*len(sI_t), Ts) # for RF carrier
  sIc_t = sI_t*np.cos(2*np.pi*fc*t) #with carrier
  sQc_t = sQ_t*np.sin(2*np.pi*fc*t) #with carrier
  s_t = sIc_t - sQc_t# Bandpass MSK modulated signal
  if enable_plot:
    fig, (ax1,ax2,ax3) = plt.subplots(3, 1)
    ax1.plot(t,sI_t);ax1.plot(t,sIc_t,'r')
    ax2.plot(t,sQ_t);ax2.plot(t,sQc_t,'r')
    ax3.plot(t,s_t,'--')
    ax1.set_ylabel('$s_I(t)$');ax2.set_ylabel('$s_Q(t)$')
    ax3.set_ylabel('s(t)')
    ax1.set_xlim([-Tb,20*Tb]);ax2.set_xlim([-Tb,20*Tb])
    ax3.set_xlim([-Tb,20*Tb])
    fig.show()
  result = dict()
  result['s(t)']=s_t;result['sI(t)']=sI_t;result['sQ(t)']=sQ_t;result['t']=t
  return result


  #demodulador
def msk_demod(r,N,fc,OF):
  """
  MSK demodulator
  Parameters:
  r : received signal at the receiver front end
  N : number of symbols transmitted
  fc : carrier frequency in Hertz
  OF : oversampling factor (at least 4 is better)
  Returns:
  a_hat : detected binary stream
  """
  L = 2*OF # samples in 2Tb duration
  Fs=OF*fc;Ts=1/Fs;Tb = OF*Ts; # sampling frequency, durations
  t=np.arange(-OF, len(r) - OF)/Fs # time base
  # cosine and sine functions for half-sinusoid shaping
  x=abs(np.cos(np.pi*t/(2*Tb)));y=abs(np.sin(np.pi*t/(2*Tb)))
  u= r*x*np.cos(2*np.pi*fc*t) # multiply I by half cosines and cos(2pifct)
  v=-r*y*np.sin(2*np.pi*fc*t) # multiply Q by half sines and sin(2pifct)
  iHat = np.convolve(u,np.ones(L)) # integrate for L (Tsym=2*Tb) duration
  qHat = np.convolve(v,np.ones(L)) # integrate for L (Tsym=2*Tb) duration
  iHat= iHat[L-1::L]         # I- sample at the end of every symbol
  qHat= qHat[L+L//2-1::L] # Q-sample from L+L/2th sample
  a_hat = np.zeros(N)
  a_hat[0::2] = iHat > 0 # thresholding - odd bits
  a_hat[1::2] = qHat > 0 # thresholding - even bits
  return a_hat







if __name__ == "__main__":


    fc = 80
    OF = 4
    N = 100000
    a = np.random.randint(2, size=N)

    r = msk_mod(a, fc, OF, enable_plot = True)


    r2 = r['s(t)']
    #r2 = r['t'] 
    s = msk_demod(r2, N, fc, OF) 


