#!/usr/bin/python

##############################################################
#     MIREX 2015 submission - TFM - Feature Preprocessing    #
#------------------------------------------------------------#
# DATE: 22/06/2015                                           #
# AUTHOR: Leopoldo Pla                                       #
# CHANGES ON THIS VERSION:                                   #
# - Fixed bug trasposing major relatives in minor tonalities #
##############################################################

import sys, getopt,os,csv

def main(argv):
  data = {}
  audiofile = ''
  featuresfolder = ''
  tonality=0
  features_csv = csv.writer(sys.stdout,delimiter=',',lineterminator="\n")
  
  try:
     opts, args = getopt.getopt(argv,"ha:f:",["audiofile=","featuresfolder="])
  except getopt.GetoptError:
    print 'processFeatures.py -a <audiofilename> -f <featuresfolder>' 
    sys.exit(2)
  for opt, arg in opts:
     if opt == '-h':
        print 'processFeatures.py -a <audiofilename> -f <featuresfolder>'
        sys.exit()
     elif opt in ("-a", "--audiofile"):
        audiofile = arg
     elif opt in ("-f", "--featuresfolder"):
        featuresfolder = arg
  
  #Calculate tonality of the fragment "audiofile"
  #Get the perfect cadences of all keys using 1 chroma
  transform_csv = csv.reader(open(featuresfolder+'/'+audiofile+".keystrength1.csv"),delimiter=',')
  tonalityWindow1=[]
  tonalityVotesPC={k: 0 for k in range(25)}
  
  for i in transform_csv:
    maxProb=max(i[2:])
    argMaxProb=i.index(maxProb)-1
    if float(maxProb) < 0.5:
      tonalityWindow1.append(13)
    else:
      tonalityWindow1.append(argMaxProb)

  it=0
  for chord in tonalityWindow1:
     it+=1
     if it == len(tonalityWindow1):
       continue
     
     secondChord=next((obj for obj in tonalityWindow1[it:] if obj!=13),13)
     if chord == 13 or secondChord == 13:
       continue
     if secondChord < 13:
       if (secondChord - (chord%12)) == 1:
         tonalityVotesPC[secondChord-1]+=1
     else:
       if secondChord > 17:
         if ((secondChord-12) - chord) == 5:
           tonalityVotesPC[secondChord-1]+=1
       else:
         if (secondChord - chord) == 5:
           tonalityVotesPC[secondChord-1]+=1
  tonality=max(tonalityVotesPC, key=tonalityVotesPC.get)
  tonality+=1
  if all(val==0 for val in tonalityVotesPC.values()) :
  	tonality=0
  #sys.stderr.write(audiofile + " ; tonality: " + str(tonality))
  
  #Get the highest values of key in 10 chroma
  transform_csv = csv.reader(open(featuresfolder+'/'+audiofile+".keystrength10.csv"),delimiter=',')
  tonalityWindow10=[]
  tonalityVotesChord={k: 0 for k in range(25)}
  
  for i in transform_csv:
    maxProb=max(i[2:])
    argMaxProb=i.index(maxProb)-1
    if float(maxProb) < 0.5:
      tonalityWindow10.append(13)
    else:
      tonalityWindow10.append(argMaxProb)
  
  for chord in tonalityWindow10:
     if chord == 13:
       continue
     tonalityVotesChord[chord-1]+=1
     
  newtonality=max(tonalityVotesChord, key=tonalityVotesChord.get)
  newtonality+=1

  #sys.stderr.write(" ; newtonality: " + str(newtonality))
  
  tonalityVotesPond={k: (tonalityVotesPC[k]*12)+tonalityVotesChord[k] for k in tonalityVotesPC}
  tonalityPond=max(tonalityVotesPond, key=tonalityVotesPond.get)
  tonalityPond+=1
  #sys.stderr.write(" ; newtonalitypond: " + str(tonalityPond) + "\n")
  
  
  #Get the feature 1-POS chord
  unigramChord={k: 0 for k in range(25)}
  for chord in tonalityWindow1:
     if chord == 13:
       continue
     unigramChord[chord-1]+=1
  
  #Traspose the unigramChord based on pondered tonality
  unigramChordT={k: 0 for k in range(25)}
  tonalityPond-=1
  if tonalityPond < 12: 		#If we traspose to major chord
    for i in range(12): 		#For every major chord
      if (i - tonalityPond) < 0:	#If we traspose out of bounds, put in top OF MAJOR, not minor, else, put in place
        unigramChordT[i-tonalityPond+12]=unigramChord[i]
      else: 
        unigramChordT[i-tonalityPond]=unigramChord[i]
    for i in range(13,25):		#For every minor chord
      if (i - tonalityPond) < 13:	#If we traspose out of bounds, put in top OF MINOR, not major, else, put in place
        unigramChordT[i-tonalityPond+12]=unigramChord[i]
      else:
        unigramChordT[i-tonalityPond]=unigramChord[i]
        
  elif tonalityPond > 12:		#If we traspose to minor chord, we need to put minor chord in major's place
    for i in range(12):			#For every major chord
      if (i - (tonalityPond-13)) < 0:	#If we traspose out of bounds, put in top OF MINOR, opposed to the previous case
        unigramChordT[i-(tonalityPond-13)+25]=unigramChord[i]
      else:
        unigramChordT[i-(tonalityPond-13)+13]=unigramChord[i]
    for i in range(13,25):
      if (i - (tonalityPond-13)) < 13:
        unigramChordT[i-tonalityPond+12]=unigramChord[i]
      else:
        unigramChordT[i-tonalityPond]=unigramChord[i]
        
  #sys.stderr.write(audiofile + "unigramChordT: "+str(unigramChordT)+"\n")  
  features_csv.writerow(unigramChordT.values())
  
  #Compute Vamp features after getting tonality
  for file in sorted(os.listdir(featuresfolder)):
    if file.startswith(audiofile):
      transform = file.split('.')[-2]
      transform_csv = csv.reader(open(featuresfolder+'/'+file),delimiter=',')
      if transform+"\n" in open('featuresToExtract').read():
        if transform == "key":
          data = {k: 0 for k in range(1,26)}
          for i in transform_csv:
            data[int(float(i[2]))]+=1
        elif transform == "mode":
          data = {k: 0 for k in range(0,2)}
          for i in transform_csv:
            data[int(float(i[2]))]+=1
        elif transform == "tonic":
          data = {k: 0 for k in range(1,14)}
          for i in transform_csv:
            data[int(float(i[2]))]+=1
        elif transform == "segmentation":
          data = {k: 0 for k in range(1,11)}
          for i in transform_csv:
            data[int(float(i[2]))]+=1
        elif transform == "means":
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 23:
                data[it-2] = j
              it+=1
        #Next features are deprecated
        elif transform == "chromameans":
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 15:
                data[it-2] = j
              it+=1
        elif transform == "chromagram":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 15:
                data[itG+it-2]=j
              it+=1
            itG+=it
        elif transform == "constantq":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 51:
                data[itG+it-2]=j
              it+=1
            itG+=it
        elif transform == "coefficients":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 23:
                data[itG+it-2]=j
              it+=1
            itG+=it
        elif transform == "tcfunction":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 4:
                data[itG+it-2]=j
              it+=1
            itG+=it
        elif transform == "tcstransform":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 9:
                data[itG+it-2]=j
              it+=1
            itG+=it
        elif transform == "keystrength":
          itG = 0
          for i in transform_csv:
            it = 1
            for j in i:
              if it > 2 and it < 28:
                data[itG+it-2]=j
              it+=1
            itG+=it
        if transform != "keystrength1" and transform != "keystrength10":
          #sys.stderr.write(audiofile + " ; " + transform+": "+str(data.values())+"\n")
          features_csv.writerow(data.values()) 
       
if __name__ == "__main__":
   main(sys.argv[1:])
