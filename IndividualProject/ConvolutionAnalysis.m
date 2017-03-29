%% Initialise
close all
clear
numfiles = 10;
mydata = cell(1, numfiles);
RxNX = zeros(100,10);
RxNY = zeros(100,10);
RxPX = zeros(100,10);
RxPY = zeros(100,10);
RyNX = zeros(100,10);
RyNY = zeros(100,10);
RyPX = zeros(100,10);
RyPY = zeros(100,10);

%% Save figures
path = 'C:\Users\Paul Cross\Documents\Work\UWE Work\Bristol Robotics Lab\TSP_ProgramsData\MotionCapturePillow\IndividualProject';
rez=200; %resolution (dpi) of final graphic
resolution=get(0,'ScreenPixelsPerInch'); %dont need to change anything here

%% Get data
for k = 1:numfiles
  myfilename = sprintf('Convolution/RxN0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{1} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Convolution/RxP0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{2} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Convolution/RyN0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{3} = mydata;

for k = 1:numfiles
  myfilename = sprintf('Convolution/RyP0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{4} = mydata;

%% Manage Data
for i = 1:numfiles
RxNX(:,i) = type{1}{i}(:,2);
RxNY(:,i) = type{1}{i}(:,3);
RxPX(:,i) = type{2}{i}(:,2);
RxPY(:,i) = type{2}{i}(:,3);
RyNX(:,i) = type{3}{i}(:,2);
RyNY(:,i) = type{3}{i}(:,3);
RyPX(:,i) = type{4}{i}(:,2);
RyPY(:,i) = type{4}{i}(:,3);
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

%% Plot ConvolutionTrackingPlot
fig1 = figure(1);
set(fig1,'Position',[0, 0, 1200, 1000]);
clf
axes1 = axes('Parent',fig1,'XMinorTick','on','YMinorTick','on','TickLabelInterpreter','latex','fontSize',16);
grid on;
hold on;
axis([270 450 180 320]);
title('Trace of the contact point, tracked using convolution','FontSize',16,'Interpreter','latex');
xlabel('X Coordinate, (pixels)','Interpreter','latex','fontSize',16);
ylabel('Y Coordinate, (pixels)','Interpreter','latex','fontSize',16);
RxN = plot(RxNXmean,RxNYmean,'r.-','DisplayName','Negative rotation around the X axis');
RxP = plot(RxPXmean,RxPYmean,'g.-','DisplayName','Positive rotation around the X axis');
RyN = plot(RyNXmean,RyNYmean,'b.-','DisplayName','Negative rotation around the Y axis');
RyP = plot(RyPXmean,RyPYmean,'k.-','DisplayName','Positive rotation around the Y axis');
legend1 = legend(axes1,'show');
set(legend1,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save ConvolutionTrackingPlot
f=fig1; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'ConvolutionTrackingPlot'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'ConvolutionTrackingPlot'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot ConvolutionVarianceRxNegative
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
legend([RxNXvarPlot RxNYvarPlot],'Variance of X Coordinate','Variance of Y Coordinate','Location','NorthWest','FontSize',16,'Interpreter','latex')
legend2 = legend(axes2,'show');
set(legend2,'Location','northwest','Interpreter','latex','FontSize',16);

%% Save ConvolutionVarianceRxNegative
f=fig2; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'ConvolutionVarianceRxNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'ConvolutionVarianceRxNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot ConvolutionVarianceRxPositive
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

%% Save ConvolutionVarianceRxPositive
f=fig3; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'ConvolutionVarianceRxPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'ConvolutionVarianceRxPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot ConvolutionVarianceRyNegative
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

%% Save ConvolutionVarianceRyNegative
f=fig4; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'ConvolutionVarianceRyNegative'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'ConvolutionVarianceRyNegative'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 

%% Plot ConvolutionVarianceRyPositive
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

%% Save ConvolutionVarianceRyPositive
f=fig5; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
print(f,fullfile(path,'ConvolutionVarianceRyPositive'),'-depsc',['-r',num2str(rez)],'-opengl') %save file 
print(f,fullfile(path,'ConvolutionVarianceRyPositive'),'-dpng',['-r',num2str(rez)],'-opengl') %save file 



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
%         axis([200 500 150 350]);
%         hold on
%     end
% end