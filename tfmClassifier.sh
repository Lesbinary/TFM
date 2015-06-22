#!/bin/bash

##############################################################
#        MIREX 2015 submission - TFM - Classifier            #
#------------------------------------------------------------#
# DATE: 07/06/2015                                           #
# AUTHOR: Leopoldo Pla                                       #
# CHANGES ON THIS VERSION:                                   #
# - Initial release                                          #
##############################################################

VERSION_NUMBER="0.1"
NUMTHREADS=4

SCRATCHFOLDER=""
FELISTFILE=""


if [ $1 == "-numThreads" ]; then
  NUMTHREADS=$2
  SCRATCHFOLDER=$3
  FELISTFILE=$4
  OUTPUTLISTFILE=$5
else
  SCRATCHFOLDER=$1
  FELISTFILE=$2
  OUTPUTLISTFILE=$3
fi

mkdir $SCRATCHFOLDER/classify

> $OUTPUTLISTFILE
> $SCRATCHFOLDER/classify/allfiles.features.csv
> $SCRATCHFOLDER/classify/classification_names.txt

echo "Extracting features from classification data"
bash tfmFeatureExtractor.sh -numThreads $NUMTHREADS $SCRATCHFOLDER/classify $FELISTFILE

for AUDIOFILE in `cat $FELISTFILE`; do
  cat $SCRATCHFOLDER/classify/allfe.`basename $AUDIOFILE`.csv >> $SCRATCHFOLDER/classify/allfiles.features.csv
done

echo "Classifying songs using the neural network"
~/matlab/bin/matlab -nodesktop -nosplash -nojvm -r "OUTPUT='$SCRATCHFOLDER';classifyDBN;exit"
for CLASS in `cat $SCRATCHFOLDER/classify/classification.csv`; do
  CLASSNAME=""
  case "$CLASS" in
    
  1)  CLASSNAME="Bach"
           ;;
  2)  CLASSNAME="Beethoven"
                ;;
  3)  CLASSNAME="Brahms"
             ;;
  4)  CLASSNAME="Chopin"
             ;;
  5)  CLASSNAME="Dvorak"
             ;;
  6)  CLASSNAME="Handel"
             ;;
  7)  CLASSNAME="Haydn"
            ;;
  8)  CLASSNAME="Mendelssohn"
                  ;;
  9)  CLASSNAME="Mozart"
             ;;
  10)  CLASSNAME="Schubert"
               ;;
  11)  CLASSNAME="Vivaldi"
              ;;
  *)  echo "Class label is not correct"
      ;;
  esac
  echo $CLASSNAME >> $SCRATCHFOLDER/classify/classification_names.txt
done

paste $FELISTFILE $SCRATCHFOLDER/classify/classification_names.txt > $OUTPUTLISTFILE

echo "Done :)"
