import numpy as np 
import matplotlib.pyplot as plt 
from scipy.signal import lfilter

L = 50 # oversampling factor 
Tb = 0.5 # bit period in seconds 
fs = L/Tb # sampling frequency in Hertz 
fc = 2/Tb # carrier frequency 
N = 8 # number of bits to transmit 
h = 1 # modulation index

b = 2*np.random.randint(2, size=N)-1 # random information sequence


