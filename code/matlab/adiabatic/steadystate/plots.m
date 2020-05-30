

figure(1)
hold on
plot(t(1:iend),y(1:iend,1),'-.')
ylabel('north')


figure(2)
hold on
plot(t(1:iend),y(1:iend,2),'-.')
ylabel('east')

figure(3)
hold on
plot(t(1:iend),-y(1:iend,3),'-.')
ylabel('-down')

figure(4)
hold on
plot(y(1:iend,2),y(1:iend,1),'-.')
xlabel('east')
ylabel('north')

figure(5)
hold on
plot(y(1:iend,2),-y(1:iend,3),'-.')
xlabel('east')
ylabel('d')


figure(6)
hold on
plot(t(1:iend),-y(1:iend,6),'-.')
xlabel('time')
ylabel('RC')

figure(7)
hold on
plot(-y(1:iend,6),-y(1:iend,3),'-*')
xlabel('RC')
ylabel('Km/1000')
