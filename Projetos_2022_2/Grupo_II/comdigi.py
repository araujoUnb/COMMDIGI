#!/usr/bin/python3

import numpy as np
import random
from matplotlib import pyplot as plt
from locale import windows_locale
import commlib
import channels


if __name__=='__main__':
    Nsym = 50 #numero de bits
    fc = 400
    fs = 200e3
    M = 4 
    k = np.log2(M)
    ctl_phase=np.pi/4
    bitrate=100
    bitstream = [random.randint(0,1) for e in range(Nsym*int(k))]
    s=commlib.MPSK_mod(bitstream, bitrate, fc, fs, M, ctl_phase, False, plt_ctln=True, plt_signals=False)
    rayleigh_data = channels.rayleigh_channel(s)
    print(rayleigh_data)
    print(len(rayleigh_data))
    K = 0 #dB
    rician_data = channels.rician_channel(K, s)
    print(rician_data)
    print(len(rician_data))

    ## Rayleigh test

    hs = rayleigh_data*s[4]
    received=channels.awgn_channel(hs, 0)
    plt.plot(np.real(received), np.imag(received), "r*")
    plt.show()
    
    y = received/rayleigh_data

    plt.plot(np.real(y), np.imag(y), "b*")
    plt.show()

    
