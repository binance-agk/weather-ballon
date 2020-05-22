global k
k=0
tspan = 0:0.5:20;
[y] = ode4(@vdp1,tspan,[2 0]);
hold on 
plot(tspan,y(:,1)   );
hold on
plot(tspan,y(:,2));



function dydt = vdp1(t,y)
global k
%VDP1  Evaluate the van der Pol ODEs for mu = 1
%
%   See also ODE113, ODE23, ODE45.

%   Jacek Kierzenka and Lawrence F. Shampine Copyright 1984-2014 The
%   MathWorks, Inc.
k=k+1
t
dydt = [y(2); (1-y(1)^2)*y(2)-y(1)];
end