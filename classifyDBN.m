%Leopoldo Pla, MUIARFID 2015, Biometría (Roberto Paredes)
addpath(genpath('DeepLearnToolbox'))

%% DBN test only

test_x = csvread (strcat(OUTPUT,'/classify/allfiles.features.csv'));

% Scale data between 0 and 1
test_x = bsxfun (@rdivide, double(test_x), double(max(test_x)+1));

load(strcat(OUTPUT,'/machineTFM.mat'));

labels = nnpredict(nn, test_x);
dlmwrite(strcat(OUTPUT,'/classify/classification.csv'),labels);
