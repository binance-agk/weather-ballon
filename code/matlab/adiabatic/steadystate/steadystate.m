close all
clc
clear
% while 1
global   kt   spheroid  Pold Told Vold Vol0 hnext  vxwold vywold

Pold =100e3;
Told =100;
spheroid = referenceEllipsoid('GRS 80');
hnext=0;

bname={'TA 200','TA 300','TA 350','TA 450','TA 500','TA 600','TA 700','TA 800','TA 1000','TA 1200','TA 1500','TA 2000','TA 3000','TX 800','TX 1000','TX 1200','TX 2000','TX 3000'};

mbs=[200,300,350,450,500,600,700,800,1000,1200,1500,2000,3000,800,1000,1200,2000,3000]/1000;
mps=[250,250,250,250,250,250,250,250,250,1050,1050,1050,1050,250,250,1050,1050,1050]/1000;
vol0s=[.83 .97 1.03 1.16 1.22 1.5 1.63 .76 2.01 2.99 3.33 3.89 4.97 1.76 2.01 2.99 3.89 4.97];
dbs=[300 378 412 472 499 605 653 700 786 863 944 1054 1300 738 828 910 1079 1331]/100;

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


mvol=(Vburst-Vol0)/(38300);
n=16000;
kt=0;
endtime=16000;
t=linspace(0,endtime,n);
%% start point in lat0 long0 h0 refrence of NED sys

lat=33;
lon=41;

kt=0;
x0=0;
y0=0;
z0=0;

import matlab.net.*
import matlab.net.http.*
r = RequestMessage;
h=0;

while 1
    
    if abs(h)>=hnext
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
    
    kt=kt+1;
    
    ro=roamb;
    
    rogasvir=pamb*1.15/(Rhel*tamb);
    rogasold=rogasvir;
    
    gama=1.06;
    
    
    Vol=(Pold/pamb)^(1/gama)*Vold;
    
    Voll=mvol*h+Vol0;
    %     Vol=Voll
    L = (Vol*3/4/pi)^(1/3)
    
    figure(3)
    hold on
    plot(h,Vol,'o',h,Voll,'v')
    
    
    rogasvir=mgas/Vol;
    g=9.81;
    B=(ro-rogasvir)*g*Vol;
    A=pi*L^2;
    visco=1.81* 10^-5;
    Vrel=10;
    Re=roamb*Vrel*L/visco;
    
    
    cd= 4.808*(log(Re))^2/100 - 1.406*log(Re) + 10.490
    % cd =0.75;
    if cd >0.85
        cd =1.85;
    end
 
    if Vol>=Vburst
        2*L
        h
        Vol
        Voll
        burst=1
      break
    end   
    FL=-Mgros*9.81+B
    V2=(FL)/(0.5*ro*cd*A) ;
    V=V2^0.5;
    
    if ~isreal(V)
        h
    end
    
    figure(3323)
    plot(h,V,'o')
    hold on
    pause(0.001)
    Pold=pamb;
    Vold=Vol;
    Told=tamb;
    kt=kt+1;
    h=h+500;
    
end

