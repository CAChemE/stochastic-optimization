x = -2:0.1:2;
y = -2:0.1:2;
z = -2:0.1:2;

[X,Y,Z] = meshgrid(x, y, z);

C =  zeros(length(x),length(y),length(z));

for i = 1:length(X)
    for j = 1:length(Y)
        for k = 1:length(Z)
            C(i,j,k) = F_Ackley(X(i,j,k),Y(i,j,k),Z(i,j,k));
        end
    end
end

i = 1;
scatter3( X(i,j,k),Y(i,j,k),Z(i,j,k),10,C(i,j,k),'filled')
hold on

for i = 1:length(X)
    for j = 1:length(Y)
        for k = 1:length(Z)
        scatter3( X(i,j,k),Y(i,j,k),Z(i,j,k),10,C(i,j,k),'filled');
        end
    end
end
