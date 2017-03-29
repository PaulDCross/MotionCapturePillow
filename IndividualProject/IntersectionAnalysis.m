%% Initialise
close all
clear
numfiles = 10;
mydata = cell(1, numfiles);
RxNX = zeros(100,10);
RxNY = zeros(100,10);
RxNXstd = zeros(100,10);
RxNYstd = zeros(100,10);
RxPX = zeros(100,10);
RxPY = zeros(100,10);
RxPXstd = zeros(100,10);
RxPYstd = zeros(100,10);
RyNX = zeros(100,10);
RyNY = zeros(100,10);
RyNXstd = zeros(100,10);
RyNYstd = zeros(100,10);
RyPX = zeros(100,10);
RyPY = zeros(100,10);
RyPXstd = zeros(100,10);
RyPYstd = zeros(100,10);

%% Get data
for k = 1:numfiles
  myfilename = sprintf('Intersection/RxN0%d_resolution180_100.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{1} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RxP0%d_resolution180_100.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{2} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RyN0%d_resolution180_100.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{3} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RyP0%d_resolution180_100.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{4} = mydata;


%% Manage Data
for i = 1:numfiles
RxNX(:,i) = type{1}{i}(:,2);
RxNY(:,i) = type{1}{i}(:,3);
RxNXstd(:,i) = type{1}{i}(:,4);
RxNYstd(:,i) = type{1}{i}(:,5);
RxPX(:,i) = type{2}{i}(:,2);
RxPY(:,i) = type{2}{i}(:,3);
RxPXstd(:,i) = type{2}{i}(:,4);
RxPYstd(:,i) = type{2}{i}(:,5);
RyNX(:,i) = type{3}{i}(:,2);
RyNY(:,i) = type{3}{i}(:,3);
RyNXstd(:,i) = type{3}{i}(:,4);
RyNYstd(:,i) = type{3}{i}(:,5);
RyPX(:,i) = type{4}{i}(:,2);
RyPY(:,i) = type{4}{i}(:,3);
RyPXstd(:,i) = type{4}{i}(:,4);
RyPYstd(:,i) = type{4}{i}(:,5);
end

RxNXmean = mean(RxNX,2);
RxNYmean = mean(RxNY,2);
RxPXmean = mean(RxPX,2);
RxPYmean = mean(RxPY,2);
RyNXmean = mean(RyNX,2);
RyNYmean = mean(RyNY,2);
RyPXmean = mean(RyPX,2);
RyPYmean = mean(RyPY,2);

% variance
RxNXvar = var(RxNX,0,2);
RxNYvar = var(RxNY,0,2);
RxPXvar = var(RxPX,0,2);
RxPYvar = var(RxPY,0,2);
RyNXvar = var(RyNX,0,2);
RyNYvar = var(RyNY,0,2);
RyPXvar = var(RyPX,0,2);
RyPYvar = var(RyPY,0,2);

% Standard deviation
RxNXstdmean = mean(RxNXstd,2);
RxNYstdmean = mean(RxNYstd,2);
RxPXstdmean = mean(RxPXstd,2);
RxPYstdmean = mean(RxPYstd,2);
RyNXstdmean = mean(RyNXstd,2);
RyNYstdmean = mean(RyNYstd,2);
RyPXstdmean = mean(RyPXstd,2);
RyPYstdmean = mean(RyPYstd,2);

%% Plot data
fig1 = figure(1);
axes1 = axes('Parent',fig1,'XMinorTick','on', 'TickLabelInterpreter','latex');
clf
grid on;
hold on;

axis([270 460 160 360]);
xlabel('X Coordinate, (pixels)','Interpreter','latex');
ylabel('Y Coordinate, (pixels)','Interpreter','latex');
plot(RxNXmean, RxNYmean, 'k.-')
annotation(fig1,'textbox',...
    [0.56 0.778045253531166 0.150796480500052 0.0637903145202788],...
    'String',{'Positive rotation','around the x axis'},...
    'LineStyle',':',...
    'Interpreter','latex',...
    'FontSize',16);
plot(RxPXmean, RxPYmean, 'k.-')
annotation(fig1,'textbox',...
    [0.56 0.178045253531166 0.150796480500052 0.0637903145202789],...
    'String',{'Negative rotation','around the x axis'},...
    'LineStyle',':',...
    'Interpreter','latex',...
    'FontSize',16);
plot(RyNXmean, RyNYmean, 'k.-')
annotation(fig1,'textbox',...
    [0.75 0.438045253531166 0.150796480500052 0.0637903145202789],...
    'String',{'Negative rotation','around the y axis'},...
    'LineStyle',':',...
    'Interpreter','latex',...
    'FontSize',16);
plot(RyPXmean, RyPYmean, 'k.-')
annotation(fig1,'textbox',...
    [0.25 0.438045253531166 0.150796480500052 0.0637903145202789],...
    'String',{'Positive rotation','around the y axis'},...
    'LineStyle',':',...
    'Interpreter','latex',...
    'FontSize',16);

%%
fig2 = figure(2);
clf
RxN = subplot(211);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the NEGATIVE direction around the X axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel('Variance', 'Interpreter','latex', 'FontSize',16)
RxNXvarPlot = plot(RxNXvar);
RxNYvarPlot = plot(RxNYvar);
legend([RxNXvarPlot RxNYvarPlot], 'Variance of X Coordinate', 'Variance of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

RxP = subplot(212);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the POSITIVE direction around the X axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'FontSize',16)
ylabel('Variance', 'FontSize',16)
RxPXvarPlot = plot(RxPXvar);
RxPYvarPlot = plot(RxPYvar);
legend([RxPXvarPlot RxPYvarPlot], 'Variance of X Coordinate', 'Variance of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

fig3 = figure(3);
RyN = subplot(211);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the NEGATIVE direction around the Y axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel('Variance', 'Interpreter','latex', 'FontSize',16)
RyNXvarPlot = plot(RyNXvar);
RyNYvarPlot = plot(RyNYvar);
legend([RyNXvarPlot RyNYvarPlot], 'Variance of X Coordinate', 'Variance of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

RyP = subplot(212);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the POSITIVE direction around the Y axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel('Variance', 'Interpreter','latex', 'FontSize',16)
RyPXvarPlot = plot(RyPXvar);
RyPYvarPlot = plot(RyPYvar);
legend([RyPXvarPlot RyPYvarPlot], 'Variance of X Coordinate', 'Variance of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

%%
fig3 = figure(4);
clf
RxN = subplot(211);
grid on;
hold on;
axis([0 100 40 80]);
title('Standard deviation of the intersections averaged across all ten datasets for rotating in the NEGATIVE direction around the X axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel({'Standard','deviation'}, 'Interpreter','latex', 'FontSize',16)
RxNXvarPlot = plot(RxNXstdmean);
RxNYvarPlot = plot(RxNYstdmean);
legend([RxNXvarPlot RxNYvarPlot], 'Standard deviation of X Coordinate', 'Standard deviation of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

RxP = subplot(212);
grid on;
hold on;
axis([0 100 40 80]);
title('Standard deviation of the intersections averaged across all ten datasets for rotating in the POSITIVE direction around the X axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel({'Standard','deviation'}, 'Interpreter','latex', 'FontSize',16)
RxPXvarPlot = plot(RxPXstdmean);
RxPYvarPlot = plot(RxPYstdmean);
legend([RxPXvarPlot RxPYvarPlot], 'Standard deviation of X Coordinate', 'Standard deviation of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

figure(5);
RyN = subplot(211);
grid on;
hold on;
axis([0 100 40 80]);
title('Standard deviation of the intersections averaged across all ten datasets for rotating in the NEGATIVE direction around the Y axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel({'Standard','deviation'}, 'Interpreter','latex', 'FontSize',16)
RyNXvarPlot = plot(RyNXstdmean);
RyNYvarPlot = plot(RyNYstdmean);
legend([RyNXvarPlot RyNYvarPlot], 'Standard deviation of X Coordinate', 'Standard deviation of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)

RyP = subplot(212);
grid on;
hold on;
axis([0 100 40 80]);
title('Standard deviation of the intersections averaged across all ten datasets for rotating in the POSITIVE direction around the Y axis',...
    'FontSize',16,...
    'Interpreter','latex');
xlabel('Image Number', 'Interpreter','latex', 'FontSize',16)
ylabel({'Standard','deviation'}, 'Interpreter','latex', 'FontSize',16)
RyPXvarPlot = plot(RyPXstdmean);
RyPYvarPlot = plot(RyPYstdmean);
legend([RyPXvarPlot RyPYvarPlot], 'Standard deviation of X Coordinate', 'Standard deviation of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16)




% figure(3)
% clf
% count = 0;
% for j = 2:3
%     count = count + 1;
%     subplot((210)+count)
%     for i = 1:numfiles
%         plot(mydata{i}(:,1), mydata{i}(:,j), '-x');
%         hold on
%     end
% end
% 
% figure
% for k = 1:length(type)
%     for i = 1:numfiles
%         plot(type{k}{i}(1:5:100,2), type{k}{i}(1:5:100,3), '-x');
%         axis([200 500 100 400]);
%         hold on
%     end
% end