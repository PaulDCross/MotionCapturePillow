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



%% Plot data
figure(1)
grid on;
hold on;
axis([0 900 0 500]);
plot(RxNXmean, RxNYmean, 'k.-')
plot(RxPXmean, RxPYmean, 'k.-')
plot(RyNXmean, RyNYmean, 'k.-')
plot(RyPXmean, RyPYmean, 'k.-')

figure(2)
grid on;
hold on;
subplot(411)
% plot(RxNXvar)
plot(RxNYvar)
subplot(412)
% plot(RxPXvar)
plot(RxPYvar)
subplot(413)
plot(RyNXvar)
% plot(RyNYvar)
subplot(414)
plot(RyPXvar)
% plot(RyPYvar)

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