find /home/leopoldo/tfm/audio/ -type f > featureExtractionFiles.txt
cat featureExtractionFiles.txt | cut -f 6 -d '/' > tmp
paste featureExtractionFiles.txt tmp > trainingFiles.txt
find /home/leopoldo/tfm/audio-testing/ -type f > classifyFiles.txt
cat classifyFiles.txt | cut -f 6 -d '/' > tmp
paste classifyFiles.txt tmp > expectedResult.txt
