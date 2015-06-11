#!/bin/bash

##############################################################
#     MIREX 2015 submission - TFM - Trainer                  #
#------------------------------------------------------------#
# DATE: 06/06/2015                                           #
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
else
  SCRATCHFOLDER=$1
  FELISTFILE=$2
fi
IFS=$'\n'
> $SCRATCHFOLDER/allfiles.features.csv
> $SCRATCHFOLDER/allfiles.classes.csv

for LINE in `cat $FELISTFILE`; do
  AUDIOFILE=`echo $LINE | cut -f 1`
  CLASSNAME=`echo $LINE | cut -f 2`
  CLASS=0
  case "$CLASSNAME" in

  
  "Bach")  CLASS=1
           ;;
  "Beethoven")  CLASS=2
                ;;
  "Brahms")  CLASS=3
             ;;
  "Chopin")  CLASS=4
             ;;
  "Dvorak")  CLASS=5
             ;;
  "Handel")  CLASS=6
             ;;
  "Haydn")  CLASS=7
            ;;
  "Mendelssohn")  CLASS=8
                  ;;
  "Mozart")  CLASS=9
             ;;
  "Schubert")  CLASS=10
               ;;
  "Vivaldi")  CLASS=11
              ;;
  *)  echo "Class label is not correct: $CLASSNAME"
      ;;
  esac
  echo "0,0,0,0,0,0,0,0,0,0,0" | sed s/0/1/$CLASS > $SCRATCHFOLDER/class.`basename $AUDIOFILE`.csv
  cat $SCRATCHFOLDER/class.`basename $AUDIOFILE`.csv >> $SCRATCHFOLDER/allfiles.classes.csv
  cat $SCRATCHFOLDER/allfe.`basename $AUDIOFILE`.csv >> $SCRATCHFOLDER/allfiles.features.csv
done
echo "Training the neural network"
~/matlab/bin/matlab -nodesktop -nosplash -nojvm -r "OUTPUT='$SCRATCHFOLDER';trainDBN;exit"

