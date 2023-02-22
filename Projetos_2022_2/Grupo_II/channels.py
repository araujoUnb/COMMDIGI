#!/usr/bin/python3

import numpy as np
from numpy import random
from matplotlib import pyplot as plt
from locale import windows_locale


def awgn_channel(s, SNRdB, L=1):

    gamma = 10**(SNRdB/10) #convertendo de dB para linear 

    if s.ndim==1: #se a entrada é um vetor unidimensional
        P=L*np.sum(abs(s)**2)/len(s) #Potência do sinal unidimensional
    else:
        P=L*np.sum(np.sum(abs(s)**2))/len(s) #Potência de um sinal multidimensional

    N0 = P/gamma #Densidade do ruído

    if np.isrealobj(s): # Se o vetor for real
        n = random.normal(0, np.sqrt(N0/2), s.shape)
    else:
        n = random.normal(0, np.sqrt(N0/2), s.shape)+ \
            1j*random.normal(0, np.sqrt(N0/2), s.shape)
    r = s + n
    return r


def rayleigh_channel(N):

    #Filtro gaussiano com 1 tap
    sigma = 1/np.sqrt(2)
    h = random.normal(0, sigma, N)+1j*random.normal(0, sigma, N)
    return abs(h)


def rician_channel(K_dB, N):
    K = 10**(K_dB/10)
    mu = np.sqrt(K/(2*(K+1)))
    sigma = np.sqrt(1/(2*(K+1)))
    h = random.normal(mu, sigma, N)+1j*random.normal(mu, sigma, N)
    return abs(h)


if __name__=='__main__':
    Nsym = 50 #numero de bits
    fc = 400
    fs = 200e3
    M = 4 
    k = np.log2(M)
    ctl_phase=np.pi/4
    bitrate=100
    bitrate = [random.randint(0,1) for e in range(Nsym*int(k))]
    s=commlib.MPSK_mod(bitstream, bitrate, fc, fs, M, ctl_phase, False, plt_ctln=True, plt_signals=True)
    rayleigh_data = rayleigh_channel(s)
    print(rayleigh_data)
    print(len(rayleigh_data))
    K = 0 #dB
    rician_data = rician_channel(K, s)
    print(rician_data)
    print(len(rician_data))
