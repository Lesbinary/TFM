%Leopoldo Pla, MUIARFID 2015, TFM (Roberto Paredes)
%OUTPUT='/home/leopoldo/tfm/scratch/';
addpath(genpath('DeepLearnToolbox'))

%% Load data and normalize
training_x = csvread (strcat(OUTPUT,'allfiles.features.csv'));
training_y = csvread (strcat(OUTPUT,'allfiles.classes.csv'));
test_x = [];
test_y = [];

% Scale data between 0 and 1
[~,ncol]=size(training_x);
for i = 1:ncol
training_x(:,i) = mat2gray(training_x(:,i));
end

[~,ncol]=size(test_x);
for i = 1:ncol
test_x(:,i) = mat2gray(test_x(:,i));
end
training_y = double(training_y);
test_y = double(test_y);


[N,~]=size(training_x);
K=1:N;
D = K(rem(N,K)==0);
[~,numberFactors] = size(D);
if numberFactors > 8
    batch_size=D(numberFactors-5);
else
    batch_size=N;
end


%% train DBN and use its weights to initialize a NN
rand('state',331)
dbn.sizes = [300 500];
opts.numepochs =   20;
opts.batchsize = batch_size;
opts.momentum  =   0;
opts.alpha     =   1;
dbn = dbnsetup(dbn, training_x, opts);
dbn = dbntrain(dbn, training_x, opts);


%unfold dbn to nn
nn = dbnunfoldtonn(dbn, 11);

%nn.dropoutFraction = 0.5;           %  Dropout fraction 
% nn.weightPenaltyL2 = 1e-4;          %  L2 weight decay
nn.activation_function = 'sigm';    %  Sigmoid activation function
nn.learningRate = 1.0;                %  Sigm require a lower learning rate
nn.output = 'softmax';              %  use softmax output
opts.numepochs =  400;               %  Number of full sweeps through data
opts.batchsize = batch_size;               %  Take a mean gradient step over this many samples
opts.plot = 0;                      %  enable plotting


%nn = nntrain(nn, training_x, training_y, opts, test_x, test_y);
nn = nntrain(nn, training_x, training_y, opts);

save(strcat(OUTPUT,'machineTFM.mat'),'nn');

