x = -2:0.01:2;
y =  zeros(1,length(x));

for i = 1:length(x)
   y(i) = F_Ackley(x(i));
end

plot(x,y)
