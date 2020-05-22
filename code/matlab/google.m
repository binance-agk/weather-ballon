clc
clear
% while 1 global vxwind  vywind time
n=20;
endtime=20000;
% time=linspace(0,endtime,n); vxwind=50*rand*cos(time)';
% vywind=50*rand*cos(time)';

%%start point in lat0 long0 h0 refrence of NED sys
global lat0 lon0 h0
lat0=35.69
lon0=51.6
h0=0;

x0=0;
y0=0
z0=0;



[t,y] = ode45(@vdp1,linspace(0,endtime,n),[x0 y0 z0 0 0 0]);
y(end,:)


figure(1)
plot(t,-y(:,3),'-o')
figure(11)
plot(t,y(:,2),'-o')
figure(31)
plot(t,y(:,1),'-o')
% title(''); xlabel('Time t'); ylabel('Solution y'); legend('y_1') pause
% end


function dXdt = vdp1(t,x)
%%
% global lat0 lon0 h0
% import matlab.net.*
% import matlab.net.http.*
% spheroid = referenceEllipsoid('GRS 80');
% 
% [lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid)
% r = RequestMessage;
% uri = URI(strcat('http://localhost:8080/value/u-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
% resp = send(r,uri);
% vxw=str2num(resp.Body.Data)
% 
% uri = URI(strcat('http://localhost:8080/value/v-component_of_wind_isobaric/',num2str(lat),'/',num2str(lon),'/',num2str(h),'/0/1'));
% resp = send(r,uri);
% vyw=str2num(resp.Body.Data)
%%
vxw=55*rand*tanh(cos(t));
vyw=25*rand*sin(t)+0.02*rand;

ro=1.0;
cd=0.03+0.2*rand+0.42*rand;
A=0.009;
vx=x(4);
vy=x(5);
vz=x(6);

Vrel=sqrt((vxw-vx)^2+(vyw-vy)^2+(vz)^2);
vrelz=0-vz;
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