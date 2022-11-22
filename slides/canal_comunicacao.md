---
marp: true
theme: gaia
color: #000
paginate: true
footer: 'Comunicação Digital '
header: '![h:60px](../Figs/UNBS-300x150.png)'
---

<style>
    section {
          width: 1280px;
          font-size: 30px;
          padding: 40px;
          background-color: #ffffff;
    }
    section::after {
        content: 'Page ' attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
        color: #000080
    }

    h1 {
       font-size: 60px ;
       color: #306030
    }

    h2 {
       font-size: 40px ;
       color: #306030
    }

    header {
        left: 29cm;
        height: 2cm;
    }

    header {
        top: 5px;
        color: #000080
    }

    footer {
     bottom: 10px;
    }

    </style>
<!-- _class: lead -->


# Canais de Comunicação
Prof. Daniel Costa Araújo

---

## Definições

* Relação sinal ruído
  $$
    \gamma = \frac{P_r}{N_0B}
  $$

* Relação energia de símbolo de ruído
   $$
    \gamma _s = \frac{E_s}{N_0B} = k \frac{E_b}{N_0B} = \log_2(M) \gamma _b 
   $$

   * $\gamma _s$ é a SNR por símbolo
   * $\gamma _b$ é a SNR por bit


---

## Modelo de Canal AWGN

![bg auto](Figs/awgn.png)

---

## Framework de avaliação

![bg auto](Figs/framework.png)

--- 
## Desempenho das Modulações em Canais AWGN

![bg auto](Figs/tabela_ber.png)

---
## Comparativo entre modulações

![bg auto w:80%](Figs/psk.png)
![bg auto w:80%](Figs/pam.png)

---
## Canais com desvanecimento: Representação Física


![bg auto w:60%](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.0mad4VSRqeYMPcHkaz-ZowHaE5%26pid%3DApi&f=1&ipt=29eb222de83d4a12826f4e7fd88ebd6711f48b71bf4d30986e5d1a3c02d12bc5&ipo=images)

![bg auto w:90%](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi1.wp.com%2Fwww.gaussianwaves.com%2Fgaussianwaves%2Fwp-content%2Fuploads%2F2019%2F06%2Fpower_delay_profile.png%3Fw%3D825%26ssl%3D1&f=1&nofb=1&ipt=96e97262334f07709466c6a846a33a5bdfd5843a9534ffbd2f1ac0811b8daacc&ipo=images)

---
## Canais com desvanecimento
* Características
  * Distorção em fase e frequência
  * Interferência intersimbólica
  * Canais variantes e invariantes no tempo