clc
clear
% while 1 
global  time kt wind  spheroid 

spheroid = referenceEllipsoid('GRS 80');


wind=[]
time=[]
n=100;
kt=0;
endtime=2500;
t=linspace(0,endtime,n); 

%% start point in lat0 long0 h0 refrence of NED sys
global lat0 lon0 h0 
lat0=44
lon0=122
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


% title(''); xlabel('Time t'); ylabel('Solution y'); legend('y_1') pause
% end
%%
%%
function dXdt = vdp1(t,x)

global kt lat0 lon0 h0 wind time  spheroid 
import matlab.net.*
import matlab.net.http.*
r = RequestMessage;


[lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid);

uri = URI(strcat('http://localhost:8080/value/u-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
resp = send(r,uri);
vyw=str2double(resp.Body.Data);

uri = URI(strcat('http://localhost:8080/value/v-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
resp = send(r,uri);
vxw=str2double(resp.Body.Data);
wind=[wind; vxw vyw];

time=[time; t];
%%
% vxw=5.5*(cos(t/33))+2;
% vyw=2.5/(t+4)
t
kt=kt+1;
ro=1.2;
cd=0.03+0.45;
A=0.01;
vx=x(4);
vy=x(5);
vz=x(6);

Vrel=sqrt((vxw-vx)^2+(vyw-vy)^2+(vz)^2);
vrelz=0-vz;
vrelx=vxw-vx;
vrely=vyw-vy;

Drag=0.5*ro*(Vrel)^2*cd*A;
Vol=0.12;
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