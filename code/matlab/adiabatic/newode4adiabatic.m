% close all
clc
clear
% while 1
global  time kt wind  spheroid  Pold Told Vold Vol0 hnext

Vol0=2.99;
Pold =100e3;
Told =100;
Vold=Vol0;
spheroid = referenceEllipsoid('GRS 80');
hnext=0

wind=[];
time=[];
n=16000;
kt=0;
endtime=16000;
t=linspace(0,endtime,n);

%% start point in lat0 long0 h0 refrence of NED sys
global lat0 lon0 h0
lat0=44;
lon0=66;
h0=0;
kt=0;
x0=0;
y0=0;
z0=0;



[y] = ode4(@vdp1,t,[x0 y0 z0 0 0 0]);
y(end,:)


figure(1)
hold on
plot(t,y(:,1),'-.')
ylabel('north')


figure(2)
hold on
plot(t,y(:,2),'-.')
ylabel('east')

figure(3)
hold on
plot(t,-y(:,3),'-.')
ylabel('-down')

figure(4)
hold on
plot(y(:,2),y(:,1),'-.')
xlabel('east')
ylabel('north')

figure(5)
hold on
plot(y(:,2),-y(:,3),'-.')
xlabel('east')
ylabel('d')


figure(6)
hold on
plot(t,-y(:,6),'-.')
xlabel('time')
ylabel('RC')


% title(''); xlabel('Time t'); ylabel('Solution y'); legend('y_1') pause
% end
%%
function dXdt = vdp1(t,x)

global kt lat0 lon0 h0 wind time  spheroid rogasold  Pold Told Vold Vol0 hnext vxwold vywold
import matlab.net.*
import matlab.net.http.*
r = RequestMessage;

if abs(x(3))<1
    x(3)=-1;
end

[lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid);

if abs(h)>hnext || abs(h)>1e4
    r = RequestMessage;
    urll=strcat('http://localhost:8080/allvalue/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/0');
    uri = URI(urll);
    resp = send(r,uri);
    f=str2num(resp.Body.Data(1));
    pamb=f(4);
    tamb=f(3);
    vxw=f(1);
    vyw=f(2);
    hnext=f(5);
else
    pamb=Pold;
    tamb=Told;
    vxw=vxwold;
    vyw=vywold;
    
end

Ramb=287 ;
roamb=pamb/(Ramb*tamb);
% roamb=1.22
Rhel=2077.1;




% wind=[wind; vxw vyw];



% 
% time=[time; t];
%%
% vxw=5.5*(cos(t/33))+2;
% vyw=2.5/(t+4)
% x(3)
t

kt=kt+1;
vx=x(4);
vy=x(5);
vz=x(6);

Vrel=sqrt((vxw-vx)^2+(vyw-vy)^2+(vz)^2);
vrelz=0-vz;
vrelx=vxw-vx;
vrely=vyw-vy;
ro=roamb;
rogas=0.164;

rogasvir=pamb*1.15/(Rhel*tamb);
rogasold=rogasvir;
mgas=rogas*Vol0;
gama=1.66   ;
Vol=(Pold/pamb)^(1/gama)*Vold;
rogasvir=mgas/Vol;
%rogasold=rogasvir;
g=9.81;
B=(ro-rogasvir)*g*Vol;



L = (Vol*3/4/pi)^(1/3);
A=pi*L^2;
visco=1.81* 10^-5;
Re=roamb*Vrel*L/visco;

mbalon=1200/1000;
mpay=1050/1000;

Mtot=mgas+mbalon+mpay;
Mgros=mbalon+mpay;

cd= 4.808*(log(Re))^2/100 - 1.406*log(Re) + 10.490;
% cd =0.75;
if cd >0.85
    cd =0.6;
end
%
% figure(34)
% plot(-x(3),Re,'*')
% hold on
% figure(35)
% plot(-x(3),cd,'*')
% hold on
%
%


Drag=0.5*ro*(Vrel)^2*cd*A;
Drag=0;


dXdt(1)=vx;
dXdt(2)=vy;
dXdt(3)=vz;
dXdt(4)=Drag*(vrelx)/Vrel/Mtot;
dXdt(5)=Drag*vrely/Vrel/Mtot;
dXdt(6)=(Mgros*9.81-B+Drag*vrelz/Vrel)/Mtot;

% 
% figure(33)
% plot(-x(3),vz,'v')
% ylabel('vz')
% hold on
%
% figure(323)
% plot(-x(3),vx,'*')
% ylabel('vx')
% hold on
%
% figure(313)
% plot(-x(3),vy,'*')
% ylabel('vy')
% hold on

 B
vz
% figure(22)
% plot(-x(3),dXdt(6),'*')
% hold on
%
% figure(353)
% plot(-x(3),Vol,'*')
% ylabel('vol')
% % hold on
%
% figure(2221)
% plot(-x(3),A,'*')
% ylabel('A')
% hold on
%
% figure(223)
% plot(-x(3),B,'*')
% ylabel('Bync')
% % hold on
%
% figure(2319)
% plot(t,Mgros*9.81+Drag*vrelz/Vrel,'*')
% ylabel('Grav + Dragz')
% hold on


% figure(565)
% plot(-x(3),roamb,'*')
% ylabel('ro density')
% hold on

if abs(x(3))>30e3
    dXdt= [0 0 0 0 0 0 ]' ;
    return;
end


Pold=pamb;
Vold=Vol;

Told=tamb;
vxwold=vxw;
vywold=vyw;

dXdt=dXdt';
end