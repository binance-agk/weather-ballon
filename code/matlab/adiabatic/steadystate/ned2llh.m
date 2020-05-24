global iend 

fileID = fopen('exp.txt','w');
fprintf(fileID,'%6s %12s\n','x','exp(x)');
for i= 1 :100:iend
    [lat,lon,h]=ned2geodetic(y(i,1),y(i,2),y(i,3),lat0 ,lon0,h0,spheroid);
   fprintf(fileID,'%2.6f,%2.6f,%5.3f\n',lon,lat,h); 
    
end
