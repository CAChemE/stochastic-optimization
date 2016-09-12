x = -2:1:2;
y = -2:1:2;
X = zeros(length(x),length(y));
Y = zeros(length(x),length(y));
Z =  zeros(length(x),length(y));

for i = 1:length(x)
    for j = 1:length(y) 
        X(i,j) = x(i,j);
        Y(i,j) = y(i,j);
        Z(i,j) = F_Ackley([x(i),y(i)]);
    end
end

plot3(X,Y,Z)
