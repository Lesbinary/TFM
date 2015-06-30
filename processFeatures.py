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
  
  #sys.stderr.write(audiofile + " Tonality window: " + str(tonalityWindow1) + "\n")
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
  
  
  #Traspose the chord window to later use it to get n-gram POS chords
  trasposedWindow1 = []
  for value in tonalityWindow1:
    if value == 13:
      trasposedWindow1.append(13)
    else:

      if tonalityPond < 13: 			#If we traspose to major chord
        if value < 13:	 			#For every major chord
          if (value - tonalityPond) < 0:	#If we traspose out of bounds, put in top OF MAJOR, not minor, else, put in place
            trasposedWindow1.append(value-tonalityPond+13)
          else: 
            trasposedWindow1.append(value-tonalityPond+1)
        if value > 13 and value < 26:		#For every minor chord
          if (value - tonalityPond) < 13:	#If we traspose out of bounds, put in top OF MINOR, not major, else, put in place
            trasposedWindow1.append(value-tonalityPond+13)
          else:
            trasposedWindow1.append(value-tonalityPond+1)

      elif tonalityPond > 13:			#If we traspose to minor chord, we need to put minor chord in major's place
        if value < 13:				#For every major chord
          if (value - (tonalityPond-13)) < 0:	#If we traspose out of bounds, put in top OF MINOR, opposed to the previous case
            trasposedWindow1.append(value-(tonalityPond-13)+26)
          else:
            trasposedWindow1.append(value-(tonalityPond-13)+14)
        if value > 13 and value < 26:		#For every minor chord
          if (value - (tonalityPond-13)) < 13:
            trasposedWindow1.append(value-tonalityPond+13)
          else:
            trasposedWindow1.append(value-tonalityPond+1)
  
  #sys.stderr.write(audiofile + " trasposedWindow1: "+str(trasposedWindow1)+"\n")
    
  #Get the feature 1-gram POS chord
  unigramChord={k: 0 for k in range(25)}
  for chord in trasposedWindow1:
    if chord == 13:
      continue
    unigramChord[chord-1]+=1
    
  unigramChord.pop(13, None)
  #sys.stderr.write(audiofile + " unigramChord: "+str(unigramChord)+"\n")  
  
  
  #Get the features bigram POS chord
  bigramChord={k: 0 for k in range(13)}

  aux=-1
  for value in trasposedWindow1:
    if value == 13:
      continue
    if aux == -1:
      aux = value
      continue
    else:
      #Major cadences
      if tonalityPond < 13:
        if value == 1 and aux == 12: #perfect authentic cadence
          bigramChord[0]+=1
        elif value == 1 and aux == 2: #perfect plagal cadence
          bigramChord[1]+=1
        elif value == 12 and aux == 11: #Half cadence
          bigramChord[2]+=1
        elif value == 12 and aux == 15: #Half cadence
          bigramChord[3]+=1
        elif value == 12 and aux == 14: #Half cadence
          bigramChord[4]+=1
        elif value == 12 and aux == 2: #Half cadence
          bigramChord[5]+=1
        elif value == 12 and aux == 1: #Half cadence
          bigramChord[6]+=1
        elif value == 14 and aux == 12: #Interrupcted (deceptive) cadence
          bigramChord[7]+=1
        elif value == 1 and aux == 18: #plagal cadence
          bigramChord[8]+=1
        aux = value
      #Minor cadences
      else:
        if value == 1 and aux == 16: #perfect authentic cadence (minor)
          bigramChord[9]+=1
        elif value == 1 and aux == 12: #modal authentic cadence (minor)
          bigramChord[10]+=1
        elif value == 1 and aux == 2: #perfect plagal cadence (minor)
          bigramChord[11]+=1
        elif value == 1 and aux == 18: #plagal cadence (minor)
          bigramChord[11]+=1
        aux = value
  
  
  
  #sys.stderr.write(audiofile + " bigramChord: "+str(bigramChord.values())+"\n")
  
  
  
  #Get the features trigram POS chord
  trigramChord={k: 0 for k in range(10)}

  auxprime=-1
  auxprime2=-1
  for value in trasposedWindow1:
    if value == 13:
      continue
    if auxprime == -1:
      auxprime = value
      continue
    elif auxprime2 == -1:
      auxprime2 = value
      continue
    else:
      #Major cadences
      if tonalityPond < 14:
        if value == 2 and auxprime == 1 and auxprime2 == 2:
          trigramChord[0]+=1
        elif value == 1 and auxprime == 12 and auxprime2 == 2:
          trigramChord[1]+=1
        elif value == 12 and auxprime == 2 and auxprime2 == 12:
          trigramChord[2]+=1
        elif value == 2 and auxprime == 15 and auxprime2 == 12:
          trigramChord[3]+=1
        elif value == 2 and auxprime == 14 and auxprime2 == 12:
          trigramChord[4]+=1
        elif value == 1 and auxprime == 2 and auxprime2 == 12:
          trigramChord[5]+=1
        elif value == 12 and auxprime == 2 and auxprime2 == 25:
          trigramChord[6]+=1
        auxprime2 = auxprime
        auxprime = value
      #Minor cadences
      else:
        if value == 2 and auxprime == 1 and auxprime2 == 2:
          trigramChord[7]+=1
        elif value == 1 and auxprime == 12 and auxprime2 == 2:
          trigramChord[8]+=1
        elif value == 1 and auxprime == 12 and auxprime2 == 11:
          trigramChord[9]+=1
        auxprime2 = auxprime
        auxprime = value
  

  
  #sys.stderr.write(audiofile + " trigramChord: "+str(trigramChord.values())+"\n")
  
  features_csv.writerow(bigramChord.values())
  features_csv.writerow(trigramChord.values())
  features_csv.writerow([tonalityPond])
  features_csv.writerow(unigramChord.values())
  #features_csv.writerow(trasposedWindow1)
  #Deleted this last feature because of possibility of variance in MIREX
  
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
