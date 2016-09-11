function Result = pso_v3(objfnc, lb, ub, intVar, varargin)

%--------------------------------------------------------------------------
% # Standard PSO algorithm (gbest) for minimizing a function
%--------------------------------------------------------------------------



% >>>>>>>>>>>>>>>>>>>>>>>>>>[ PSO OPTIONS ]>>>>>>>>>>>>>>>>>>>> User inputs
     
% * Population size
swarm_size = 5;       %  number of the swarm particles

% * Termination Conditions
maxIter    = 1000;       %  maximum number of iterations
maxFO      = realmax;     %  maximun number of function evaluations

maxIterNoImprov = realmax;  % maximun number of iterations without improving the objective function
maxTime         = realmax; % time limit in seconds [s]

tol_x   = 1e-5;          % tolerance in x (norm 2)
tol_fnc = 1e-5;          % tolerance in objective function

% * PSO parameters
inertia_w       = 0.72;  % Inertia weigth
acceleration_c1 = 1.49;  % Acceleration coefficient (cognitive)
acceleration_c2 = 1.49;  % Acceleraton coefficient (social)
v_max = 2;            % Maximun velocity in absolute value
break_coeff = 0.05;      % Break factor for the worst particle
Red_acceleration_c1 = 2; % Reduction factor of accelaration c1 coefficient for the worst particle


% * Algorithm options
print_freq = 10;
plotPSO    = 'on';
% >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End inputs


% ········· PARTICLE SWARM OPTIMIZATION ALGORITHM CODE ····················

% # Preprocessing Operations ##############################################
n_variables = length(lb); % # variables

lb = lb(:); lb_original = lb; % Lower and upper bounds must be column vectors. 
ub = ub(:); ub_original = ub;


% #  Initialization #######################################################

% 01. Set new bounds on the integer variables -----------------------------
% NOTE1: Bounds on integer variables must be integer numbers
% NOTE2: New bounds are established in order to give the same probability
%        to the variable bounds when round MATLAB function is used.    
if isvector(intVar)
    lb(intVar) = lb(intVar) - 0.49;
    ub(intVar) = ub(intVar) + 0.49;
end

% 02. Set the initial position of the particles ---------------------------
aux1 =  (ub - lb);
x = lb(:,ones(1,swarm_size)) + aux1(:,ones(1,swarm_size)).*rand(n_variables, swarm_size);
x(intVar,:) = round(x(intVar,:));

% 03. Set initial velocity for particles ----------------------------------
v = zeros(n_variables, swarm_size);

% 04. Evaluation of each particle -----------------------------------------
% NOTE3: It is not possible to perform a vectorized version since our
%        objective function can be a black box (e.g. process simulator) 

tic;
fval = zeros(1,swarm_size);
for iParticle = 1:swarm_size
    fval(iParticle) = objfnc(x(:,iParticle));
end

% 05. Best particle position and global best particle position and fitness-
pbest_position             = x;
pbest_fitness              = fval;

[gbest_fitness, gbest_ind] = min(fval);
gbest_position             = x(:,gbest_ind);

iter1_time = toc;

% 06. Print Results -------------------------------------------------------

% * Worst particle in each iteration
[pworst_fitness, pworst_ind] = max(pbest_fitness);
pworst_position = pbest_position(:,pworst_ind);

error_x   = norm(pworst_position - gbest_position, 2);
error_fnc = norm(pworst_fitness - gbest_fitness, 2);

print_results(1, swarm_size, gbest_fitness, pworst_fitness, ...
              error_fnc, error_x, swarm_size, n_variables, intVar,...
                    print_freq);                                           % Aux Fnc # 01 ###

             
% 07. Plot Particles and Objective Function -------------------------------

if strcmp(plotPSO, 'on') == 1
    if n_variables == 2
        plot_3D(objfnc, lb_original, ub_original, x, fval, 1);             % Aux Fnc # 02 ###
    elseif n_variables == 1
    else
        warning(' Only 2D and 3D plots are possible !!! ')
    end 
end


% #########################################################################
% ####### Main Body of the Algorithm ### ##################################
% #########################################################################

% * Control parameters & Preallocation arrays
iter                     = 1;
timeLimit                = iter1_time;
FO_evaluations           = swarm_size;
iter_fitness_improvement = 0;

v_new  = v;
x_new  = x;
x_plot = x;


tic;
while 1
    
    for iP = 1:swarm_size
        
        % 08. Update velocity for all particles -----------------------------------
        
        if iter > 1 && iP == pworst_ind
            
            v_new(:,iP) = break_coeff * inertia_w * v(:,iP) +...
                acceleration_c1 * rand(n_variables,1) .* (pbest_position(:,iP) - x(:,iP))/Red_acceleration_c1 + ...
                acceleration_c2 * rand(n_variables,1) .* (gbest_position - x(:,iP));
        else
            v_new(:,iP) = inertia_w * v(:,iP) +...                                              % inertial  part
                acceleration_c1 * rand(n_variables,1) .* (pbest_position(:,iP) - x(:,iP)) + ... % cognitive part
                acceleration_c2 * rand(n_variables,1) .* (gbest_position - x(:,iP));            % social    part
        end
        
% 09. Velocity control ----------------------------------------------------
        v_new(v_new > v_max) =  v_max;
        v_new(v_new < -v_max) = -v_max;
        
% 10. Update position for all particlespbes -------------------------------
        x_new(:,iP) = x(:,iP) + v_new(:,iP);
        
% 11. Position control ----------------------------------------------------
        
        % * Lower bound
        x_new(:,iP) = (x_new(:,iP) < lb).*lb + (x_new(:,iP) >= lb).*x_new(:,iP);                   
                   
        % * Upper bound
        x_new(:,iP)  = (x_new(:,iP) > ub).*ub + (x_new(:,iP) <= ub).*x_new(:,iP);
             
        
% 12. Round integer variables to the nearest integer ----------------------
% NOTE4: we need an aux var for the position in order to round the integer
%        variables keeping unalterd x_new for next iterations
        x_iP = x_new(:,iP);
        x_iP(intVar) = round(x_iP(intVar));
        x_plot(:,iP) = x_iP;

        
% 13. Function evaluation & update personal best particle (pbest) so far --
        fval(iP) = objfnc(x_iP);
            
        if fval(iP) < pbest_fitness(iP)
            pbest_fitness(iP)    = fval(iP);
            pbest_position(:,iP) =  x_iP;
        end
            
% 14. Update global best particle (gbest) ---------------------------------
        if pbest_fitness(iP) < gbest_fitness
            gbest_fitness  = pbest_fitness(iP);
            gbest_position = x_iP;
            iter_fitness_improvement = 0;
        else
            iter_fitness_improvement = iter_fitness_improvement + 1;
        end
    end % for loop in range 1:size_swarm ##################################
        % #################################################################

    iter_time = toc;

% 15. Print Results -------------------------------------------------------
    iter = iter + 1;
    FO_evaluations = FO_evaluations + swarm_size;
    
    timeLimit = timeLimit + iter_time;
    
    % * Worst particle in each iteration
    [pworst_fitness, pworst_ind] = max(pbest_fitness);
    pworst_position = pbest_position(:,pworst_ind);
    
    error_x   = norm(pworst_position - gbest_position, 2);
    error_fnc = norm(pworst_fitness - gbest_fitness, 2);  
    
    print_results(iter, FO_evaluations, gbest_fitness, pworst_fitness, ...
                  error_fnc, error_x, swarm_size, n_variables, intVar,...
                        print_freq );                                      % Aux Fnc # 01 ###
                    
% 16. Plot Particles and Objective Function -------------------------------

if strcmp(plotPSO, 'on') == 1
    if n_variables == 2
        plot_3D(objfnc, lb_original, ub_original, x_plot, fval, iter);            % Aux Fnc # 02 ###
    elseif n_variables == 1
    end 
end

% 17. Check Termination Criterias -----------------------------------------
    
    if iter >= maxIter
        termination = 'Stop due to maximum number of major iterations.';
        break
    elseif FO_evaluations >= maxFO
        termination = 'Stop due to maximum number of function evaluations.';
        break
    elseif iter_fitness_improvement >= maxIterNoImprov
        termination = 'Number of generations without fitness improvement Reached. The objective function is under specified tolerance';
        break
    elseif timeLimit >= maxTime;
        termination = 'The solver was interrupted because it reached the time limit.';
        break
        
    elseif error_fnc <= tol_fnc 
        termination = ' The objective function is under specified tolerance ';
        break
    elseif error_x <= tol_x 
        termination = ' The tolerance between best and worse particles is under specification';
        break
    end
    
    % * Position and velocity for next iteration
    x = x_new;
    v = v_new;

end

Result.xopt  = gbest_position;
Result.FO    = gbest_fitness;
Result.exit  = termination;

end

% # Auxiliari function ####################################################

% # 01 ## Print Results====================================================
function  print_results(iter, FO_evaluations, gbest, pworst, ...
                        error_fnc, error_x, swarm_size, n_variables,...
                        intVar, print_freq )

if iter == 1
    fprintf(' \n')
    fprintf('  # STANDARD PARTICLE SWARM OPTIMIZATION ALGORITHM - gbest version ### \n');
    fprintf('       * Swarm size ................. %i\n', swarm_size)
    fprintf('       * # Continuous Variables ..... %i\n', n_variables - length(intVar));
    fprintf('       * # Integer Variables .......  %i\n', length(intVar))
    fprintf(' \n')
end


if (iter == 1) || (iter/(print_freq) == round(iter/(print_freq)))
    if (iter == 1) || (iter/(print_freq*20) == round(iter/(print_freq)))
        fprintf('  --------------------------------------------------------------------------------------------\n')
        fprintf('   Iteration \t FO_evals \t gBest Fitness \t pWorst Fitness\t   error_FO \t error_x\n')
        fprintf('  --------------------------------------------------------------------------------------------\n')
    end
    
    fprintf('%8.0f \t\t %5.0f \t %15.3e \t %11.3e \t %11.3e \t %6.3e  \n', ...
            iter, FO_evaluations, gbest,  pworst, error_fnc, error_x)
    
end


end

% # 02 ## Plot Particles and Objective Function ===========================
function plot_3D(objfnc, lb_original, ub_original, x, fval, iter)
global X Y Z
if iter == 1
    
    % * Plot Objective Function
    X = linspace(lb_original(1), ub_original(1));
    Y = linspace(lb_original(2), ub_original(2));
    [X,Y] = meshgrid(X,Y);
    [npoints] = length(X);
    
    for i=1:npoints;
        for j=1:npoints;
            Z(i,j) = objfnc([X(i,j), Y(i,j)]');
        end
    end
    
    fh = figure(1);
    set( fh,'color', 'white');
    
    colormap winter
 
    meshc(X, Y, Z); hold on  
    
    % * Plot particles
    Px = x(1,:);
    Py = x(2,:);
    Pz = fval;
    
    puntos3D = plot3(Px, Py, Pz, 'r.','MarkerSize',25);
    puntos2D = plot3(Px, Py, zeros(size(Pz)), 'b.','MarkerSize',25);
    pause(0.1)
else
    set(gca,'NextPlot','replacechildren');
    colormap winter
    meshc(X, Y, Z)
    % * Plot particles
    Px = x(1,:);
    Py = x(2,:);
    Pz = fval;
    
    set(gca,'NextPlot','add');
    puntos3D = plot3(Px, Py, Pz, 'r.','MarkerSize',25);
    puntos2D = plot3(Px, Py, zeros(size(Pz)), 'b.','MarkerSize',25);
    pause(0.05)
end



end



































