# Trabajo de Final de Máster - Master's Final Work
## MIREX 2015 - Audio Classical Composer Identification

Based on musicological fundaments of classical authors, I used their compositive features to train a neural network using author profiling techniques in a real task of the MIREX 2015 contest.

- Command line calling format for all executables including examples: based on the second example of the Wiki (http://www.music-ir.org/mirex/wiki/2015:Audio_Classification_%28Train/Test%29_Tasks#Example_submission_calling_formats):
	extractFeatures.sh /path/to/scratch/folder /path/to/featureExtractionListFile.txt
	Train.sh /path/to/scratch/folder /path/to/trainListFile.txt 
	Classify.sh /path/to/scratch/folder /path/to/testListFile.txt /path/to/outputListFile.txt

In this exact case (which I used for testing), the commands are:
	tfmFeatureExtractor.sh -numThreads 8 ~/tfm/scratch/ ~/tfm/trunk/featureExtractionFiles.txt
	tfmTrainer.sh -numThreads 8 ~/tfm/scratch/ ~/tfm/trunk/trainingFiles.txt
	tfmClassifier.sh -numThreads 8 ~/tfm/scratch/ ~/tfm/trunk/classifyFiles.txt  ~/tfm/trunk/finalResult

- Number of threads/cores used or whether this should be specified on the command line: the default threads are 4 (as the Wiki specifies as the maximum) and can be set with the parameter "-numThreads" (see previous example).
- Expected memory footprint: With my Dataset it used 80MB. I suppose that Matlab will use 100-150MB in MIREX.
- Expected runtime: With my own dataset, 7 minutes. In MIREX I suppose that 20-40 minutes
- Approximately how much scratch disk space will the submission need to store any feature/cache files?: 100MB I suppose (depending of the input files)
- Any required environments/architectures (and versions) such as Matlab, Java, Python, Bash, Ruby etc.: Matlab (I tested with 2014a in clean install of Ubuntu 15.04), Java (used for Matlab to work, I don't mind the version), Python (I used 2.7, default in clean install of Ubuntu 15.04), Bash (I don't mind, I used the default Bash in Ubuntu 15.04).
- Any special notice regarding to running your algorithm: It will output some .log files into the scratch folder, if needed.
