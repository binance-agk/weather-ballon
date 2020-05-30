close all
clc
clear
% while 1
global   kt   spheroid  Pold Told Vold Vol0 hnext terminate iend
terminate=false;
Pold =100e3;
Told =100;
spheroid = referenceEllipsoid('GRS 80');
hnext=-1000;

n=22000;
iend=n;
endtime=15000;
t=linspace(0,endtime,n);

%% start point in lat0 long0 h0 refrence of NED sys
global lat0 lon0 h0 mgas Mtot Mgros Vburst
lat0=36
lon0=-55;
h0=0;
kt=0;
x0=0;
y0=0;
z0=0;
mbs=[3000,800,1200]/1000;
mps=[1050,250,1050]/1000;
vol0s=[4.97,1.76,2.99];
dbs=[1331,738,910]/100;
i=1;

mbalon=mbs(i);
mpay=mps(i);
Vol0=vol0s(i);
Vold=Vol0;
DBurst=dbs(i);
Vburst=pi*DBurst^3/6;
rogas=0.164;
mgas=rogas*Vol0;
Mtot=mgas+mbalon+mpay;
Mgros=mbalon+mpay;


%%
[y] = ode4(@vdp1,t,[x0 y0 z0 0 0 0]);
%%
plots

%%

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function dXdt = vdp1(t,x)
global Vburst kt lat0 lon0 h0 terminate  spheroid rogasold  Pold Told Vold Vol0 hnext vxwold vywold mgas Mtot Mgros
import matlab.net.*
import matlab.net.http.*
r = RequestMessage;

if abs(x(3))<=1
    x(3)=-1;
end

[lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid);

if abs(h-hnext)>500
    r = RequestMessage;
    urll=strcat('http://localhost:8080/allvalue/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/0');
    uri = URI(urll);
    resp = send(r,uri);
    f=str2num(resp.Body.Data(1));
    pamb=f(4);
    tamb=f(3);
    vxw=f(1);
    vyw=f(2);
    hnext=h;
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

gama=1.06;

Vol=(Pold/pamb)^(1/gama)*Vold;
rogasvir=mgas/Vol;
%rogasold=rogasvir;
g=9.81;
B=(ro-rogasvir)*g*Vol;



L = (Vol*3/4/pi)^(1/3);
A=pi*L^2;
visco=1.81*10^-5;
Re=roamb*Vrel*L/visco;


cd= 4.808*(log(Re))^2/100 - 1.406*log(Re) + 10.490;
% cd =0.75;
if cd >0.9
    cd =0.85
end
cd=0.05*rand*cd+cd-0.05*rand*cd;
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

if Vol>=Vburst
    dXdt=dXdt';
    Vol
    terminate =true;
    return;
end


if abs(x(3))>49e3
    dXdt=dXdt';
    terminate =true;
    return;
end
if vz>0
    vz
end

h
Pold=pamb;
Vold=Vol;

Told=tamb;
vxwold=vxw;
vywold=vyw;

dXdt=dXdt';
end