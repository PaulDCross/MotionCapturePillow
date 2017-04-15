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

%% Save figures
path = 'C:\Users\Paul Cross\Documents\Work\UWE Work\Bristol Robotics Lab\TSP_ProgramsData\MotionCapturePillow\IndividualProject';
rez=200; %resolution (dpi) of final graphic
resolution=get(0,'ScreenPixelsPerInch'); %dont need to change anything here

%% Get data
for k = 1:numfiles
  myfilename = sprintf('Intersection/RxN0%d_resolution30_16.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{1} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RxP0%d_resolution30_16.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{2} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RyN0%d_resolution30_16.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{3} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Intersection/RyP0%d_resolution30_16.txt', k);
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

%% Plot IntersectionTrackingPlot
fig1 = figure(1);
set(fig1,'Position',[0, 0, 1200, 1000]);
clf
axes1 = axes('Parent',fig1,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([270 460 160 360]);
title('Trace of the contact point, tracked using convolution','FontSize',16,'Interpreter','latex');
xlabel('X Coordinate, (pixels)','Interpreter','latex','fontSize',16);
ylabel('Y Coordinate, (pixels)','Interpreter','latex','fontSize',16);
RxN = plot(RxNXmean,RxNYmean,'r.-','DisplayName','Negative rotation around the X axis');
RxP = plot(RxPXmean,RxPYmean,'g.-','DisplayName','Positive rotation around the X axis');
RyN = plot(RyNXmean,RyNYmean,'b.-','DisplayName','Negative rotation around the Y axis');
RyP = plot(RyPXmean,RyPYmean,'k.-','DisplayName','Positive rotation around the Y axis');
legend1 = legend(axes1,'show');
set(legend1,'Location','northwest','Interpreter','latex','FontSize',14);

%% Save IntersectionTrackingPlot
f=fig1; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionTrackingPlot'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionTrackingPlot'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionVarianceRxNegative
fig2 = figure(2);
set(fig2,'Position',[0, 50, 1200, 300]);
clf
axes2 = axes('Parent',fig2,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the NEGATIVE direction around the X axis','FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel('Variance','Interpreter','latex','FontSize',16)
RxNXvarPlot = plot(RxNXvar,'r','DisplayName','Variance of X Coordinate');
RxNYvarPlot = plot(RxNYvar,'b','DisplayName','Variance of Y Coordinate');
legend([RxNXvarPlot RxNYvarPlot], 'Variance of X Coordinate', 'Variance of Y Coordinate', 'Location', 'NorthWest', 'FontSize',16,'Interpreter','latex')
legend2 = legend(axes2,'show');
set(legend2,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save IntersectionVarianceRxNegative
f=fig2; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionVarianceRxNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionVarianceRxNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionVarianceRxPositive
fig3 = figure(3);
set(fig3,'Position',[0, 50, 1200, 300]);
clf
axes3 = axes('Parent',fig3,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the POSITIVE direction around the X axis','FontSize',16,'Interpreter','latex');
xlabel('Image Number','FontSize',16,'Interpreter','latex')
ylabel('Variance','FontSize',16,'Interpreter','latex')
RxPXvarPlot = plot(RxPXvar,'r','DisplayName','Variance of X Coordinate');
RxPYvarPlot = plot(RxPYvar,'b','DisplayName','Variance of Y Coordinate');
legend3 = legend(axes3,'show');
set(legend3,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save IntersectionVarianceRxPositive
f=fig3; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionVarianceRxPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionVarianceRxPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionVarianceRyNegative
fig4 = figure(4);
set(fig4,'Position',[0, 50, 1200, 300]);
clf
axes4 = axes('Parent',fig4,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the NEGATIVE direction around the Y axis','FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel('Variance','Interpreter','latex','FontSize',16)
RyNXvarPlot = plot(RyNXvar,'r','DisplayName','Variance of X Coordinate');
RyNYvarPlot = plot(RyNYvar,'b','DisplayName','Variance of Y Coordinate');
legend4 = legend(axes4,'show');
set(legend4,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save IntersectionVarianceRyNegative
f=fig4; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionVarianceRyNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionVarianceRyNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionVarianceRyPositive
fig5 = figure(5);
set(fig5,'Position',[0, 50, 1200, 300]);
clf
axes5 = axes('Parent',fig5,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 0 100]);
title('Variance across all ten datasets for rotating in the POSITIVE direction around the Y axis','FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel('Variance','Interpreter','latex','FontSize',16)
RyPXvarPlot = plot(RyPXvar,'r','DisplayName','Variance of X Coordinate');
RyPYvarPlot = plot(RyPYvar,'b','DisplayName','Variance of Y Coordinate');
legend5 = legend(axes5,'show');
set(legend5,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save IntersectionVarianceRyPositive
f=fig5; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionVarianceRyPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionVarianceRyPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 






%% Standard Deviation
%% Plot IntersectionStandardDeviationXNegative
fig6 = figure(6);
set(fig6,'Position',[0, 50, 1200, 300]);
clf
axes6 = axes('Parent',fig6,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 40 80]);
title({'Standard deviation of the intersections averaged across all ten datasets','for rotating in the NEGATIVE direction around the X axis'},'FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel({'Standard','deviation'},'Interpreter','latex','FontSize',16)
RxNXstdmeanPlot = plot(RxNXstdmean,'r','DisplayName','Standard deviation of X Coordinate');
RxNYstdmeanPlot = plot(RxNYstdmean,'b','DisplayName','Standard deviation of Y Coordinate');
legend6 = legend(axes6,'show');
set(legend6,'Location','northwest','Interpreter','latex');

%% Save IntersectionStandardDeviationXNegative
f=fig6; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionStandardDeviationXNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionStandardDeviationXNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionStandardDeviationXPositive
fig7 = figure(7);
set(fig7,'Position',[0, 50, 1200, 300]);
clf
axes7 = axes('Parent',fig7,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 40 80]);
title({'Standard deviation of the intersections averaged across all ten datasets', 'for rotating in the POSITIVE direction around the X axis'},'FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel({'Standard','deviation'},'Interpreter','latex','FontSize',16)
RxPXstdmeanPlot = plot(RxPXstdmean,'r','DisplayName','Standard deviation of X Coordinate');
RxPYstdmeanPlot = plot(RxPYstdmean,'b','DisplayName','Standard deviation of Y Coordinate');
legend7 = legend(axes7,'show');
set(legend7,'Location','northwest','Interpreter','latex');

%% Save IntersectionStandardDeviationXPositive
f=fig7; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionStandardDeviationXPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionStandardDeviationXPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionStandardDeviationYNegative
fig8 = figure(8);
set(fig8,'Position',[0, 50, 1200, 300]);
clf
axes8 = axes('Parent',fig8,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 40 80]);
title({'Standard deviation of the intersections averaged across all ten datasets','for rotating in the NEGATIVE direction around the Y axis'},'FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel({'Standard','deviation'},'Interpreter','latex','FontSize',16)
RyNXstdmeanPlot = plot(RyNXstdmean,'r','DisplayName','Standard deviation of X Coordinate');
RyNYstdmeanPlot = plot(RyNYstdmean,'b','DisplayName','Standard deviation of Y Coordinate');
legend8 = legend(axes8,'show');
set(legend8,'Location','northwest','Interpreter','latex');

%% Save IntersectionStandardDeviationYNegative
f=fig8; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionStandardDeviationYNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionStandardDeviationYNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot IntersectionStandardDeviationYPositive
fig9 = figure(9);
set(fig9,'Position',[0, 50, 1200, 300]);
clf
axes9 = axes('Parent',fig9,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([0 100 40 80]);
title({'Standard deviation of the intersections averaged across all ten datasets','for rotating in the POSITIVE direction around the Y axis'},'FontSize',16,'Interpreter','latex');
xlabel('Image Number','Interpreter','latex','FontSize',16)
ylabel({'Standard','deviation'},'Interpreter','latex','FontSize',16)
RyPXstdmeanPlot = plot(RyPXstdmean,'r','DisplayName','Standard deviation of X Coordinate');
RyPYstdmeanPlot = plot(RyPYstdmean,'b','DisplayName','Standard deviation of Y Coordinate');
legend9 = legend(axes9,'show');
set(legend9,'Location','northwest','Interpreter','latex');

%% Save IntersectionStandardDeviationYPositive
f=fig9; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'IntersectionStandardDeviationYPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'IntersectionStandardDeviationYPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 






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