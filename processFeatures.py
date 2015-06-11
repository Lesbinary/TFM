#!/usr/bin/python

##############################################################
#     MIREX 2015 submission - TFM - Feature Preprocessing    #
#------------------------------------------------------------#
# DATE: 04/06/2015                                           #
# AUTHOR: Leopoldo Pla                                       #
# CHANGES ON THIS VERSION:                                   #
# - Initial release                                          #
##############################################################

import sys, getopt,os,csv

def main(argv):
  audiofile = ''
  featuresfolder = ''
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
  for file in sorted(os.listdir(featuresfolder)):
    if file.startswith(audiofile):
      data = {}
      transform = file.split('.')[-2]
      transform_csv = csv.reader(open(featuresfolder+'/'+file),delimiter=',')
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
      elif transform == "chromameans":
        for i in transform_csv:
          it = 1
          for j in i:
            if it > 2 and it < 15:
              data[it-2] = j
            it+=1
      sys.stderr.write(audiofile + " ; " + transform+": "+str(data.values())+"\n")
      features_csv = csv.writer(sys.stdout,delimiter=',',lineterminator="\n")
      features_csv.writerow(data.values()) 
       
if __name__ == "__main__":
   main(sys.argv[1:])
