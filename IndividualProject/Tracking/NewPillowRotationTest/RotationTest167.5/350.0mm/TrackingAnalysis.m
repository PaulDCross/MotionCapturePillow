close all
numfiles = 1;
mydata = cell(1, numfiles);

types = cell(1,4);

for k = 1:numfiles
  myfilename = sprintf('RxN0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{1} = mydata;

for k = 1:numfiles
  myfilename = sprintf('RxP0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{2} = mydata;

for k = 1:numfiles
  myfilename = sprintf('RyN0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{3} = mydata;

for k = 1:numfiles
  myfilename = sprintf('RyP0%d.txt', k);
  M = importdata(myfilename);
  mydata{k} = M.data;
end
type{4} = mydata;


count = 0;
for j = 2:3
    count = count + 1;
    subplot((21*10)+count)
    for i = 1:numfiles
        plot(mydata{i}(:,1), mydata{i}(:,j), '-x');
        hold on
    end
end

figure
for k = 1:length(type)
for i = 1:numfiles
    plot(type{k}{i}(1:5:100,2), type{k}{i}(1:5:100,3), '-x');
    axis([200 500 150 350]);
    hold on
end
end