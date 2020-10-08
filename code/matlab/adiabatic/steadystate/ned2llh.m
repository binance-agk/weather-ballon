tg=x;
ff=length(x);
fileID = fopen('exp.txt','w');
fprintf(fileID,'%6s %12s\n','x','exp(x)');
for i= 1 :100:ff
    [lat,lon,h]=ned2geodetic(tg(i,1),tg(i,2),tg(i,3),lat0 ,lon0,h0,spheroid);
   fprintf(fileID,'%2.6f,%2.6f,%5.3f\n',lon,lat,h); 
    
end
