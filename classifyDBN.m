%Leopoldo Pla, MUIARFID 2015, TFM (Roberto Paredes)
%OUTPUT='/home/leopoldo/tfm/scratch/';
addpath(genpath('DeepLearnToolbox'))

%% DBN test only

test_x = csvread (strcat(OUTPUT,'/classify/allfiles.features.csv'));

load(strcat(OUTPUT,'machineTFMconfig.mat'))

test_x = normalize(test_x, mu, sigma);

% Scale data between 0 and 1
[rows,cols]=size(test_x);
colMax=max(abs(test_x),[],1);
test_x=test_x./repmat(colMax,rows,1);
test_x=(test_x+1)/2;

test_x(isnan(test_x))=0;

load(strcat(OUTPUT,'/machineTFM.mat'));

labels = nnpredict(nn, test_x);
dlmwrite(strcat(OUTPUT,'/classify/classification.csv'),labels);
