clc
clear 
% while 1
global vxwind  vywind time
n=3000;
endtime=200;
time=linspace(0,endtime,n);
vxwind=50*rand*cos(time)';
vywind=50*rand*cos(time)';

[t,y] = ode45(@vdp1,linspace(0,endtime,n),[0 0 10 0 0 0]);
y(end,:)

plot(t,-y(:,3),'-o')


figure(11)
hold on 
plot(t,y(:,2),'-o')
% title('');
% xlabel('Time t');
% ylabel('Solution y');
% legend('y_1')
% pause
% end





function dXdt = vdp1(t,x)
global vxwind vywind time
vxw=interp1(vxwind,time,t);
vyw=interp1(vywind,time,t);
vxw=02;
vyw=-02;
ro=1.0;
cd=0.03+0.2*rand+0.42*rand;
A=0.006;
vx=x(4);
vy=x(5);
vz=x(6);

Vrel=sqrt((vxw-vx)^2+(vyw-vy)^2+(vz)^2);
vrelz=vz;
vrelx=vxw-vx;
vrely=vyw-vy;

Drag=0.5*ro*(Vrel)^2*cd*A;
Vol=0.22;
rogas=0.164;
g=9.81;
B=(ro-rogas)*g*Vol;
Mtot=1;

dXdt(1)=vx;
dXdt(2)=vy;
dXdt(3)=vz;
dXdt(4)=Drag*(vrelx)/Vrel/Mtot;
dXdt(5)=Drag*vrely/Vrel/Mtot;
dXdt(6)=(0.04*9.81-B+Drag*vrelz/Vrel)/Mtot;

dXdt=dXdt';
end