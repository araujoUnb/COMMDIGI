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


def rayleigh_channel(s):

    #Filtro gaussiano com 1 tap
    N = len(s)
    sigma = 1/np.sqrt(2)
    h = random.normal(0, sigma, N)+1j*random.normal(0, sigma, N)
    return abs(h)


def rician_channel(K_dB, s):

    N = len(s)
    K = 10**(K_dB/10)
    mu = np.sqrt(K/(2*(K+1)))
    sigma = np.sqrt(1/(2*(K+1)))
    h = random.normal(mu, sigma, N)+1j*random.normal(mu, sigma, N)
    return abs(h)

if __name__='__main__':
   
