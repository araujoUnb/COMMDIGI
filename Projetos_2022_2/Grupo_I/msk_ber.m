
clear
N = 5*10^5; % número de bits / simbolos

fsHz = 1; % período de amostragem
T    = 4; % duração do símbolo

Eb_N0_dB = [0:10]; % multiplos valores Eb/N0
ct = cos(pi*[-T:N*T-1]/(2*T));
st = sin(pi*[-T:N*T-1]/(2*T));

for ii = 1:length(Eb_N0_dB)

    % transmissor MSK
    ipBit = rand(1,N)>0.5; % 0s e 1s com igual probabilidade
    ipMod =  2*ipBit - 1; % 0->-1 e 1->0

    ai = kron(ipMod(1:2:end),ones(1,2*T));  % bit par
    aq = kron(ipMod(2:2:end),ones(1,2*T));  % bit ímpar

    ai = [ai zeros(1,T)  ]; % igualar as dimensões das matrizes
    aq = [zeros(1,T) aq ];  % Delay na quadratura

    % forma de onda a ser transmitida
    xt = 1/sqrt(T)*[ai.*ct + j*aq.*st];

    % AWGN
    nt = 1/sqrt(2)*[randn(1,N*T+T) + j*randn(1,N*T+T)]; % variancia 0db

    % ruído
    yt = xt + 10^(-Eb_N0_dB(ii)/20)*nt; % AWGN

    %% receptor
    % multiplicar pelas senóides
    xE = conv(real(yt).*ct,ones(1,2*T));
    xO = conv(imag(yt).*st,ones(1,2*T));

    bHat = zeros(1,N);
    bHat(1:2:end) = xE(2*T+1:2*T:end-2*T) > 0 ; % bits pares
    bHat(2:2:end) = xO(3*T+1:2*T:end-T) > 0 ;  % bits ímpares

    % contagem de erros
    nErr(ii) = size(find([ipBit - bHat]),2);

end

simBer = nErr/N; % ber simulada
theoryBer = 0.5*erfc(sqrt(10.^(Eb_N0_dB/10))); % ber teorica

% plot
close all
figure
semilogy(Eb_N0_dB,theoryBer,'bs-','LineWidth',2);
hold on
semilogy(Eb_N0_dB,simBer,'mx-','LineWidth',2);
axis([0 10 10^-5 0.5])
grid on
legend('theory - bpsk', 'simulation - msk',"fontsize", 20);
xlabel('Eb/No, dB',"fontsize",24);
ylabel('Bit Error Rate',"fontsize", 24);
title('Probabilidade de erro de bit - MSK',"fontsize", 20);
