fileID = fopen('kml.kml','w');
fprintf(fileID,'%s\n','<?xml version="1.0" encoding="UTF-8"?>');
fprintf(fileID,'%s\n','<kml xmlns="http://earth.google.com/kml/2.1">');
fprintf(fileID,' <Document>\n    <name>Balloon Trajectory %s</name>\n','japan 2020 0404');
fprintf(fileID,'    <Style id="track">\n      <LineStyle>\n        <color>7f00ff00</color>\n      </LineStyle>\n      <PolyStyle>\n        <color>7f00ff00</color>\n      </PolyStyle>\n    </Style>\n');

fprintf(fileID,'    <Style id="place">\n      <IconStyle>\n        <scale>1</scale>\n        <Icon>\n          <href>http://weather.uwyo.edu/icons/purple.gif</href>\n        </Icon>\n      </IconStyle>\n    </Style>');

[lat,lon,h]=ned2geodetic(y(length(y)/2,1),y(length(y)/2,2),y(length(y)/2,3),lat0 ,lon0,h0,spheroid);

fprintf(fileID,'    <LookAt>\n      <longitude>%.10f</longitude>\n      <latitude>%.10f</latitude>\n      <range>200000.000</range>\n      <tilt>50.0</tilt>\n      <heading>10.9920856305692</heading>\n    </LookAt>\n'...
    ,lon,lat);

fprintf(fileID,'    <Placemark>\n      <name>Flight Path</name>\n      <styleUrl>#track</styleUrl>\n      <LineString>\n        <tessellate>1</tessellate>\n        <extrude>1</extrude>\n        <altitudeMode>absolute</altitudeMode>\n        <coordinates>\n');

for i =1:100:length(y)
    if all(y(i,:)==0) && i>1
        break
    end
[lat,lon,h]=ned2geodetic(y(i,1),y(i,2),y(i,3),lat0 ,lon0,h0,spheroid);
fprintf(fileID,'%.5f,%.5f,%.5f\n',lon,lat,h);
end
[lat,lon,h]=ned2geodetic(y(iend,1),y(iend,2),y(iend,3),lat0 ,lon0,h0,spheroid);
fprintf(fileID,'%.5f,%.5f,%.5f\n',lon,lat,h);
latb=lat;
lonb=lon;
hb=h;
for i =1:100:length(x)
   
[lat,lon,h]=ned2geodetic(x(i,1),x(i,2),x(i,3),lat0 ,lon0,h0,spheroid);
fprintf(fileID,'%.5f,%.5f,%.5f\n',lon,lat,h);
end


[lat,lon,h]=ned2geodetic(x(end,1),x(end,2),x(end,3),lat0 ,lon0,h0,spheroid);
fprintf(fileID,'%.5f,%.5f,%.5f\n',lon,lat,h);


fprintf(fileID,'        </coordinates>\n      </LineString>\n    </Placemark>\n');

fprintf(fileID,'   <Placemark>\n<name>Balloon Launch</name>\n<description>Balloon Launch at %.2f, %.2f</description>\n<Point><coordinates> %.2f,%.2f, %.2f</coordinates></Point>\n</Placemark>\n'...
    ,lat0,lon0,lon0,lat0,h0);


fprintf(fileID,'   <Placemark>\n<name>Balloon Burst</name>\n<description>Balloon Burst at %.2f, %.2f</description>\n<Point><coordinates> %.2f,%.2f, %.2f</coordinates></Point>\n</Placemark>\n'...
    ,latb,lonb,lonb,latb,hb);

fprintf(fileID,'   <Placemark>\n<name>Balloon Landing</name>\n<description>Balloon Burst at %.2f, %.2f</description>\n<Point><coordinates> %.2f,%.2f, %.2f</coordinates></Point>\n</Placemark>\n'...
    ,lat,lon,lon,lat,h);

fprintf(fileID,'  </Document>\n</kml>\n');

% fprintf(fileID,'        </coordinates>\n      </LineString>\n    </Placemark>\n  </Document>\n</kml>\n');





























