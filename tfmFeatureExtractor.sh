#!/bin/bash

##############################################################
#     MIREX 2015 submission - TFM - Feature Extractor        #
#------------------------------------------------------------#
# DATE: 17/06/2015                                           #
# AUTHOR: Leopoldo Pla                                       #
# CHANGES ON THIS VERSION:                                   #
# - Add feature configuration using n3 files                 #
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
> $SCRATCHFOLDER/sonic.log;
> $SCRATCHFOLDER/processF.log

echo "Extracting features"
for AUDIOFILE in `cat $FELISTFILE`; do
  for FEATURE in `cat featuresToExtract`; do
    if [ "${FEATURE:0:1}" != "#" ]; then 
      FEATURENAME=`echo $FEATURE | cut -f 4 -d ':'`
      #echo "Extracting '$FEATURE' feature from $AUDIOFILE"
      if [ -f $SCRATCHFOLDER/`basename $AUDIOFILE`.${FEATURENAME}.csv ]; then
        continue
      else
        if [ -f featuresConfig/$FEATURE.n3 ]; then
          ./sonic-annotator -t featuresConfig/$FEATURE.n3 $AUDIOFILE -w csv --csv-stdout > $SCRATCHFOLDER/`basename $AUDIOFILE`.${FEATURENAME}.csv 2>> $SCRATCHFOLDER/sonic.log &
        else
          ./sonic-annotator -d $FEATURE $AUDIOFILE -w csv --csv-stdout > $SCRATCHFOLDER/`basename $AUDIOFILE`.${FEATURENAME}.csv 2>> $SCRATCHFOLDER/sonic.log &
        fi
        NPROC=$(($NPROC+1))
        if [ "$NPROC" -ge $NUMTHREADS ]; then
          wait
          NPROC=0
        fi
      fi
    fi
  done
  wait
  #echo "Processing all audio features for $AUDIOFILE"
  python processFeatures.py --audiofile `basename $AUDIOFILE` --featuresfolder $SCRATCHFOLDER | tr '\n' ',' | sed 's/,$/\n/' > $SCRATCHFOLDER/allfe.`basename $AUDIOFILE`.csv 2>> $SCRATCHFOLDER/processF.log &
done
wait
