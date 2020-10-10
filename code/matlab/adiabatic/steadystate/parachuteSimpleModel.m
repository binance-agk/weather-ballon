clear x
global lat0 lon0 h0 spheroid
mpar=70/1000;
dcan=   94/100;
mpay=300/1000;
decent=3.7;%FOR 300GR LOAD
Apar=pi*dcan^2/4;
rogr=1.225;
h0=0;
Cd0=2*9.81*(mpar+mpay)/(Apar*rogr*decent^2);
Cd0=1.22/2;
dt=1;
x=[];
x(1,1)= y(iend,1);%north pos
x(1,2)= y(iend,2);%north pos
x(1,3)= y(iend,3);%north pos
x(1,4)= y(iend,4);%north pos
x(1,5)= y(iend,5);%north pos
x(1,6)= y(iend,6);%north pos

[lat,lon,h]=ned2geodetic(x(1),x(2),x(3),lat0 ,lon0,h0,spheroid);
hnext =h+1e9;
k=1;

spheroid = referenceEllipsoid('GRS 80');
while abs(h)>40
   
    import matlab.net.*
    import matlab.net.http.*
    r = RequestMessage;
    
    [lat,lon,h]=ned2geodetic(x(k,1),x(k,2),x(k,3),lat0 ,lon0,h0,spheroid);
    if mod(k-1,50)==0
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
        figure(33)
        plot(-x(k,3),x(k,6),'*k')
        ylabel('vz')
        hold on
    else
        pamb=Pold;
        tamb=Told;
        vxw=vxwold;
        vyw=vywold;
        
    end
    
    Ramb=287 ;
    roamb=pamb/(Ramb*tamb);
    
    
     k=k+1;
    Cd=Cd0+rand*0.02*Cd0+1*rand*Cd0
     h
    vz=(2*9.81*(mpar+mpay)/(Apar*roamb*Cd))^0.5;
    
    x(k,1)=x(k-1,1)+vxw*dt;
    x(k,2)=x(k-1,2)+vyw*dt;
    x(k,3)=x(k-1,3)+vz*dt;
    x(k,4)=vxw;
    x(k,5)=vyw;
    x(k,6)=vz;

    Pold  =pamb;
    Told =tamb;
    vxwold  =vxw;
    vywold   =vyw;
end






