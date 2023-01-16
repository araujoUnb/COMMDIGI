#!/usr/bin/python3

import numpy as np
import random
from matplotlib import pyplot as plt
from locale import windows_locale

# PULSOS
# Definicao de pulsos retangular e cosseno levantado
# Definicao de energia de pulso

def rect_pulse(amp, t, fs):
    x = np.arange(-t/2, t/2, 1/fs)
    y = np.array([amp if (e>=-t/2) and (e<=t/2) else 0 for e in x])
    return x,y

def cos_pulse(amp, t, fs):
    x = np.arange(-t/2, t/2, 1/fs)
    y = np.array([amp*np.cos(e*2*np.pi/(2*t)) if (e>=-t/2) and (e<=t/2) else 0 for e in x])
    return x,y

def pulse_energy(pulse, Rs, fss):
    p = pulse(1, 1/Rs, fss)
    return np.trapz(p[1]*p[1], dx=1/fss)

# definir pulso base a ser utilizado pela biblioteca
def base_pulse(amp, t, fs):
    return rect_pulse(amp, t, fs)

# pulso unitario baseado na freq de amostragem (oversampling * freq. portadora) e no bitrate Rs


# CODIFICACAO GRAY E CONVERSAO DE BITSTREAM PARA SEQUENCIA DE SIMBOLOS
# (sem memoria)

def gray(n):
    if (n==1) or (n==0):
        return ['0','1']
    l_old = gray(n-1)
    l_new = l_old
    l_new.reverse()
    l_old = ['0'+i for i in l_old]
    l_new = ['1'+i for i in l_new]
    l_old.reverse()
    return l_old+l_new

def convert_bitstream_to_symbols(bitstream, mod, Rs, fss):
    k = np.log2(mod) # qtde de bits/simbolo
    sym_length = len(bitstream)/k # qtde de simbolos no bitstream
    code_set = gray(k) # obter codigo gray de com k bits

    # conjunto dos simbolos possiveis
    sym_set = [2*m-1-mod for m in range(1, mod+1)] 
    # tabela relacionando simbolos possiveis com o codigo gray
    # (simbolos adjacentes tem transicao de somente 1 bit)
    sym_table = {code_set[i]:sym_set[i] for i in range(0, mod)}

    stream = np.array([])
    stream_t = np.arange(0, sym_length/Rs, Rs)
    sym = ''
    count = 0
    # le o bitstream a cada k bits e converte em simbolo de acordo
    # com o codigo gray
    for bit in bitstream:
        sym = sym + str(bit)
        #print("count", count, "sym", sym)
        if count == (k-1):
            count = 0
            stream = np.concatenate((stream, np.array([sym_table[sym]])))
            sym = ''
            continue
        count += 1

    # criar forma de onda com os simbolos consecutivos
    # criar a base temporal da forma de onda
    base_sig = np.array([])
    base_sig_t = np.array([])
    Tsym = 1/Rs
    count = 1
    for a in stream:
        p = base_pulse(a, Tsym, fss)
        base_sig = np.concatenate((base_sig, p[1]))
        base_sig_t = np.concatenate((base_sig_t, p[0]+count*Tsym))
        count += 1

    base_sig_t -= Tsym/2

    return base_sig_t, base_sig

# COMPONENTES EM FASE E QUADRATURA (PSK) E CONSTELACAO
# sinais de banda base
def smi_psk(m, M, phase, Rs, fss):
    return np.sqrt(pulse_energy(base_pulse, Rs, fss)/2)*np.cos(2*np.pi/M*(m-1)+phase)

def smq_psk(m, M, phase, Rs, fss):
    return -np.sqrt(pulse_energy(base_pulse, Rs, fss)/2)*np.sin(2*np.pi/M*(m-1)+phase)

# sinais de banda passante
def smic_psk(m, M, phase, fc, timebase, Rs, fss):
    return smi_psk(m, M, phase, Rs, fss)*np.sqrt(2/pulse_energy(base_pulse, Rs, fss))*np.cos(2*np.pi*fc*timebase)

def smqc_psk(m, M, phase, fc, timebase, Rs, fss, offt=0):
    return -smq_psk(m, M, phase, Rs, fss)*np.sqrt(2/pulse_energy(base_pulse, Rs, fss))*np.sin(2*np.pi*fc*(timebase-offt))


def plot_constellation(M, Rs, fss):
    sym_set = np.array([e for e in range(1,M+1)])
    x = smi_psk(sym_set, M, 0, Rs, fss)
    y = smq_psk(sym_set, M, 0, Rs, fss)
    plt.plot(x, y, 'o')

# MODULACAO M-PSK
def MPSK_mod(bstream, bitrate, fc, fs, M=4, ctl_phase=0, offt=False, plt_ctln=False, plt_signals=False):
    # bstream = bitstream
    # bitrate = bitrate
    # fc = carrier frequency
    # fs = sampling frequency for graphs
    # constel = show constellation graph
    # signals = show signal graphs vs. time

    # retorna: [vetor tempo, vetor sinali transmitido, componentes em fase, componentes em quadratura]

    # constellation
    plt.rcParams['figure.figsize'] = [5, 5]
    sym_set = np.array([e for e in range(1,M+1)])
    i = smi_psk(sym_set, M, ctl_phase, bitrate, fs)
    q = smq_psk(sym_set, M, ctl_phase, bitrate, fs)
    if plt_ctln:
        plt.plot(i, q, 'o')
        plt.xlabel("Componente em fase $s_i$")
        plt.ylabel("Componente em quadratura $s_q$")

    k = np.log2(M)
    # symbol rate
    Rs = bitrate/k
    Tsym = 1/Rs
    unit_pulse = base_pulse(1, 1/Rs, fs) # define unit pulse with length 1/Rs
    pulse_e = pulse_energy(base_pulse, Rs, fs)

    base_t, base_sig= convert_bitstream_to_symbols(bstream, M, Rs, fs)

    m = 0.5*(base_sig+M+1)

    a1 = smi_psk(0.5*(base_sig+M+1), M, ctl_phase, bitrate, fs)
    a2 = smq_psk(0.5*(base_sig+M+1), M, ctl_phase, bitrate, fs)

    if plt_signals:

        fig0, ax0 = plt.subplots(1,1)
        fig0.suptitle("Cadeia de símbolos enviados")
        ax0.set_ylabel("Amplitude $A_m(t)$")
        ax0.set_xlabel("tempo (s)")

        ax0.plot(base_t, base_sig)

    inphase = smic_psk(m, M, ctl_phase, fc, base_t, bitrate, fs)
    qphase = smqc_psk(m, M, ctl_phase, fc, base_t, bitrate, fs)

    r = [None, None, None, None, None]
    if offt:
        last_sym = base_sig[-4]
        offt_base_sig = np.concatenate((base_sig, np.ones(int(Tsym/2*fs))*last_sym))
        offt_base_sig = offt_base_sig[int(Tsym/2*fs)-1:base_t.size+int(Tsym/2*fs)-1]

        offt_m = 0.5*(offt_base_sig+M+1)

        qphase_o = smqc_psk(offt_m, M, ctl_phase, fc, base_t, Rs, fs)

        r[0] = base_t
        r[1] = inphase+qphase
        r[2] = inphase+qphase_o

        if plt_signals:
            plt.rcParams['figure.figsize'] = [20, 20]
            fig, ax = plt.subplots(5, 2)
            b1 = smi_psk(0.5*(base_sig+M+1), M, ctl_phase, Rs, fs)
            b2 = smq_psk(0.5*(offt_base_sig+M+1), M, ctl_phase, Rs, fs)

            ax[0,1].plot(base_t, b1)
            ax[0,1].set_title("Símbolos em fase")
            ax[1,1].plot(base_t, b2)
            ax[1,1].set_title("Símbolos em quadratura")
            ax[2,1].plot(base_t, inphase)
            ax[2,1].set_ylabel("$s_i(t)$")
            ax[3,1].plot(base_t, qphase_o)
            ax[3,1].set_ylabel("$s_q(t)$")
            ax[4,1].plot(base_t, inphase+qphase_o)
            ax[4,1].set_ylabel("$s(t)")
            ax[4,1].set_xlabel("tempo (s)")

            ax[0,0].plot(base_t, a1)
            ax[0,0].set_title("Símbolos em fase")
            ax[1,0].plot(base_t, a2)
            ax[1,0].set_title("Símbolos em quadratura")
            ax[2,0].plot(base_t, inphase)
            ax[2,0].set_ylabel("$s_i(t)$")
            ax[3,0].plot(base_t, qphase)
            ax[3,0].set_ylabel("$s_q(t)$")
            ax[4,0].plot(base_t, inphase+qphase)
            ax[4,0].set_ylabel("s(t)")
            ax[4,0].set_xlabel("tempo (s)")

    elif plt_signals:
        fig, ax = plt.subplots(5, 1)
        plt.rcParams['figure.figsize'] = [20, 20]
        ax[0].plot(base_t, a1)
        ax[0].set_title("Símbolos em fase")
        ax[1].plot(base_t, a2)
        ax[1].set_title("Símbolos em quadratura")
        ax[2].plot(base_t, inphase)
        ax[2].set_ylabel("$s_i(t)$")
        ax[3].plot(base_t, qphase)
        ax[3].set_ylabel("$s_q(t)$")
        ax[4].plot(base_t, inphase+qphase)
        ax[4].set_ylabel("s(t)")
        ax[4].set_xlabel("tempo (s)")

    else:
        r[2] = a1

    r[0] = base_t
    r[1] = inphase+qphase
    r[3] = a2
    plt.rcParams['figure.figsize'] = [5, 5]
    return r

# DEMODULAÇÃO M-PSK, COM/SEM OFFSET

def phi1(fc, timebase, Rs, fss):
    return np.sqrt(pulse_energy(base_pulse, Rs, fss)/2)*np.cos(2*np.pi*fc*timebase)

def phi2(fc, timebase, Rs, fss):
  return -np.sqrt(pulse_energy(base_pulse, Rs, fss)/2)*np.sin(2*np.pi*fc*timebase)

# signal: sinal de entrada
# timebase: eixo do tempo para o sinal de entrada
# phase: rotacao da constelação em radianos
# fc: freq. da portadora
# fs: freq. de amostragem do programa
def MPSK_dem(signal, timebase, cphase, M, fc, bitrate, fs):
    Rs = bitrate/np.log2(M)
    phase = phi1(fc, timebase, Rs, fs)*signal
    quad = -phi2(fc, timebase, Rs, fs)*signal
    onefill = np.ones(int(fs/fc)*2)
    n = onefill.size
    # Fazer produtos internos com as funcoes de base phi1 e phi2
    phase = np.convolve(onefill, phase)[n:-(n-1)]
    # Remover bordas devido à convolução. Convoluir um sinal de tamanho N com
    # outro sinal de tamanho M gera um sinal de tamanho N+M-2.
    quad = np.convolve(onefill, quad)[n:-(n-1)] 

    # Amostrar as componentes em fase e quadratura. Comecar em Tsimbolo/2
    # e amostrar a cada Tsimbolo.
    Tsym = 1/float(Rs)
    
    # Depois de amostrados, normalizar os valores para que se possa comparar com
    # a constelação de referência
    phase = np.round(phase[int(Tsym*fs/2):phase.size-1:int(Tsym*fs)])
    aux = np.max(np.abs(phase)) if np.max(np.abs(phase))!=0 else 1
    phase = phase/aux

    quad = np.round(quad[int(Tsym*fs/2):quad.size-1:int(Tsym*fs)])
    aux = np.max(np.abs(quad)) if np.max(np.abs(quad))!=0 else 1
    quad = quad/aux

    plt.plot(phase, quad, 'o')

    # Obter codigo gray de log2(M) bits 
    k = np.log2(M)
    code_set = gray(k)
    m_set = np.array(range(1, M+1))
    sym_set = np.array([2*m-1-M for m in m_set])
    # tabela relacionando o m-zinho ao codigo gray correspondente
    sym_table_m = {int(i):code_set[int(i)-1] for i in m_set}

    # gerar constelação de referencia 
    i = np.sqrt(2/pulse_energy(base_pulse, Rs, fs))*smi_psk(m_set, M, -cphase, Rs, fs)
    q = np.sqrt(2/pulse_energy(base_pulse, Rs, fs))*smq_psk(m_set, M, -cphase, Rs, fs)

    # relacionar cada par ordenado (fase, quadratura) da constelacao de ref.
    # com o seu símbolo correspondente
    lut = dict(zip(zip(i, q), m_set))
    for point in lut.keys():
        plt.plot(*point, marker='*', color='red')
        text = str(lut[point]) + ':' + str(sym_table_m[lut[point]])
        plt.annotate(text, point)

    demodulated = ''
    # calcular distancia entre pontos da constelacao de ref. e pontos
    # dos sinais de fase e quadratura obtidos anteriormente
    for s in zip(phase, quad):
        dists = dict()
        for ref in lut:
          d = np.sqrt((s[0]-ref[0])**2+(s[1]-ref[1])**2)
          dists[d] = lut[ref]
        ks = np.array(list(dists.keys()))
        # obter o símbolo com menor distância
        demodulated += sym_table_m[dists[np.min(ks)]][::-1] 
    demodulated = [int(i) for i in list(demodulated)]
    return demodulated

# PLOTAGEM DE PSD

def plotWelchPSD(x,fs,fc,ax = None,color='b', label=None):
    """
    Plot PSD of a carrier modulated signal using Welch estimate
    Parameters:mk
    x : signal vector (numpy array) for which the PSD is plotted
    fs : sampling Frequency
    fc : center carrier frequency of the signal
    ax : Matplotlib axes object reference for plotting
    color : color character (format string) for the plot
    """
    from scipy.signal import welch, windows
    from numpy import log10
    nx = max(x.shape)
    na = 16 # averaging factor to plot averaged welch spectrum
    w = windows.hann(nx//na) #// is for integer floor division
    # Welch PSD estimate with Hanning window and no overlap
    f, Pxx = welch(x,fs,window = w,noverlap=0)
    indices = (f>=fc) & (f<4*fc) # To plot PSD from Fc to 4*Fc
    Pxx = Pxx[indices]/Pxx[indices][0] # normalized psd w.r.t Fc
    ax.plot(f[indices]-fc,10*log10(Pxx),color,label=label) #Plot in the given axes


