clc
clear
% while 1
global  time kt wind  spheroid rogasold

spheroid = referenceEllipsoid('GRS 80');


wind=[];
time=[];
n=100;
kt=0;
endtime=2500;
t=linspace(0,endtime,n);

%% start point in lat0 long0 h0 refrence of NED sys
global lat0 lon0 h0
lat0=4;
lon0=122;
h0=0;
kt=0;
x0=0;
y0=0
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
%%
function dXdt = vdp1(t,x)

global kt lat0 lon0 h0 wind time  spheroid rogasold
import matlab.net.*
import matlab.net.http.*
r = RequestMessage;


[lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid);
%
% uri = URI(strcat('http://localhost:8080/value/u-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
% resp = send(r,uri);
% vyw=str2double(resp.Body.Data);
%
% uri = URI(strcat('http://localhost:8080/value/v-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
% resp = send(r,uri);
% vxw=str2double(resp.Body.Data);

%%
r = RequestMessage;
urll=strcat('http://localhost:8080/allvalue/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/0');
uri = URI(urll);
resp = send(r,uri);
f=str2num(resp.Body.Data(1));
pamb=f(end);
tamb=f(end-1);
vxw=f(1);
vyw=f(2);

Ramb=287 ;
roamb=pamb/(Ramb*tamb);
Rhel=2077.1;




wind=[wind; vxw vyw];




time=[time; t];
%%
% vxw=5.5*(cos(t/33))+2;
% vyw=2.5/(t+4)
t
kt=kt+1;
cd=0.03+0.45;
A=0.01;
vx=x(4);
vy=x(5);
vz=x(6);

Vrel=sqrt((vxw-vx)^2+(vyw-vy)^2+(vz)^2);
vrelz=0-vz;
vrelx=vxw-vx;
vrely=vyw-vy;

ro=roamb;
Drag=0.5*ro*(Vrel)^2*cd*A;

Vol0=0.35833658960019887374;
rogas=0.164;

rogasvir=pamb/(Rhel*tamb);
rogasold=rogasvir;
mgas=rogas*Vol0;

Vol= mgas/rogasvir
% rogasold=rogasvir;
g=9.81;
B=(ro-rogasvir)*g*Vol;
Mtot=1;

vrel=Vol/Vol0


dXdt(1)=vx;
dXdt(2)=vy;
dXdt(3)=vz;
dXdt(4)=Drag*(vrelx)/Vrel/Mtot;
dXdt(5)=Drag*vrely/Vrel/Mtot;
dXdt(6)=(0.3*9.81-B+Drag*vrelz/Vrel)/Mtot;

if abs(x(3))>30e3
   dXdt= [0 0 0 0 0 0 ]' ;
   return;
end
dXdt=dXdt';
end