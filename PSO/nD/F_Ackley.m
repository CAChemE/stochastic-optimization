function y = F_Ackley(x,varargin)

n = length(x);
y = -20*exp(-0.2*(1/n*sum(x.^2))^0.5) - ...
    exp(1/n*sum(cos(2*pi*x))) + 20 + exp(1);