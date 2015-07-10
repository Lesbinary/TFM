%Leopoldo Pla, MUIARFID 2015, TFM (Roberto Paredes)

%OUTPUT='/home/leopoldo/tfm/scratch/';
addpath(genpath('DeepLearnToolbox'))

%% Load data and normalize
training_x = csvread (strcat(OUTPUT,'allfiles.features.csv'));
training_y = csvread (strcat(OUTPUT,'allfiles.classes.csv'));
%test_x = csvread (strcat(OUTPUT,'/classify/allfiles.features.csv'));
%test_y = csvread (strcat(OUTPUT,'/classify/allfiles.classes.csv'));

% normalize with zscore
[training_x, mu, sigma] = zscore(training_x);
%test_x = normalize(test_x, mu, sigma);
save(strcat(OUTPUT,'machineTFMconfig.mat'),'mu','sigma');


% Scale data between 0 and 1
[rows,cols]=size(training_x);
colMax=max(abs(training_x),[],1);
training_x=training_x./repmat(colMax,rows,1);
training_x=(training_x+1)/2;

training_x(isnan(training_x))=0;

cols 

%[rows,cols]=size(test_x);
%colMax=max(abs(test_x),[],1);
%test_x=test_x./repmat(colMax,rows,1);
%test_x=(test_x+1)/2;

%test_x(isnan(test_x))=0;

[N,~]=size(training_x);
K=1:N;
D = K(rem(N,K)==0);
[~,numberFactors] = size(D);
if numberFactors > 8
    batch_size=D(numberFactors-7);
else
    batch_size=N;
end


%% train DBN and use its weights to initialize a NN
rand('state',331)
%dbn.sizes = [15];
%opts.numepochs =  0;
%opts.batchsize = batch_size;
%opts.momentum  =   0;
%opts.alpha     =   1;
%dbn = dbnsetup(dbn, training_x, opts);
%dbn = dbntrain(dbn, training_x, opts);

%unfold dbn to nn
%nn = dbnunfoldtonn(dbn, 11);

nn = nnsetup([cols 44 11]);

%nn.dropoutFraction = 0.5;           %  Dropout fraction 
% nn.weightPenaltyL2 = 1e-4;          %  L2 weight decay
nn.activation_function = 'sigm';    %  Sigmoid activation function
nn.learningRate = 0.5;                %  Sigm require a lower learning rate
nn.output = 'softmax';              %  use softmax output
opts.numepochs =  450;               %  Number of full sweeps through data
opts.batchsize = batch_size;               %  Take a mean gradient step over this many samples
opts.plot = 0;                      %  enable plotting


%nn = nntrain(nn, training_x, training_y, opts, test_x, test_y);
nn = nntrain(nn, training_x, training_y, opts);
save(strcat(OUTPUT,'machineTFM.mat'),'nn');

%[er, bad] = nntest(nn, test_x, test_y);
%er*size(test_x, 1)
