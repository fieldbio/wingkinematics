#!/usr/bin/env python
from numpy import *
from math import *
import scipy.signal as signal
from Numeric import *
import os
import getopt
import sys
import csv
from pylab import *


def usage(error=1):
	usage = """\
Version # 

Usage: %s [INPUT_FILE_NAME][INPUT_FILE_NAME][FILTERFACTOR_FILE_NAME]




Options:
   -h, --help    Print this message

[written by Paolo Segre, 2011]


""" % os.path.basename(sys.argv[0])

	if error:
		sys.stderr.write(usage)
		sys.exit(1)
	else:
		sys.stdout.write(usage)
		sys.exit()



def main(file,time):

# input files

	inFile = open(file,"r")
    	lines = inFile.readlines()	

	inFile2 = open(time,"r")
	lines2 = inFile2.readlines()	


    	Data= zeros(((len(lines)-1),6), Float)
    	Filter= zeros((1,6), Float)



    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]))
	


#############################

	temp2= str(lines2[1]).split(',')
	
	Filter[0,:]=(float(temp2[0]),float(temp2[1]),float(temp2[2]),float(temp2[3]),float(temp2[4]),float(temp2[5]))

#############################


	fundamental_frequency=40
	sample_rate=1000

	Output=zeros(((len(lines)-1),6), Float)

	for n in range(0,6):
		
		Raw=Data[:,n]
		filter_factor=Filter[0,n]
		Wn=((2*filter_factor*fundamental_frequency)/sample_rate)

		b,a = signal.butter(4,Wn,btype='low')
		Filt = signal.filtfilt(b,a,Raw)

		Output[:,n]=Filt[:]






##############################

	figure(1)
	subplot(331)
	plot(Data[:,0])
	plot(Output[:,0],c='r')
	title('RRoot_X')
	
	subplot(334)
	plot(Data[:,1])
	plot(Output[:,1],c='r')
	title('RRoot_Y')

	subplot(337)
	plot(Data[:,2])
	plot(Output[:,2],c='r')
	title('RRoot_Z')


	p1=subplot(332)
	plot(Data[100:150,0],Data[100:150,1])
	plot(Output[100:150,0],Output[100:150,1],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,0],Data[100:150,2])
	plot(Output[100:150,0],Output[100:150,2],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,1],Data[100:150,2])
	plot(Output[100:150,1],Output[100:150,2],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,0],Data[200:250,1])
	plot(Output[200:250,0],Output[200:250,1],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,0],Data[200:250,2])
	plot(Output[200:250,0],Output[200:250,2],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,1],Data[200:250,2])
	plot(Output[200:250,1],Output[200:250,2],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


##

	figure(2)
	subplot(331)
	plot(Data[:,3])
	plot(Output[:,3],c='r')
	title('LRoot_X')

	subplot(334)
	plot(Data[:,4])
	plot(Output[:,4],c='r')
	title('LRoot_Y')

	subplot(337)
	plot(Data[:,5])
	plot(Output[:,5],c='r')
	title('LRoot_Z')



	p1=subplot(332)
	plot(Data[100:150,3],Data[100:150,4])
	plot(Output[100:150,3],Output[100:150,4],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,3],Data[100:150,5])
	plot(Output[100:150,3],Output[100:150,5],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,4],Data[100:150,5])
	plot(Output[100:150,4],Output[100:150,5],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,3],Data[200:250,4])
	plot(Output[200:250,3],Output[200:250,4],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,3],Data[200:250,5])
	plot(Output[200:250,3],Output[200:250,5],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,4],Data[200:250,5])
	plot(Output[200:250,4],Output[200:250,5],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 



##



	figure(7)
	p=subplot(111)

	plot(Data[:,0],c='r')
	plot(Output[:,0],c='b') #b 
	plot(Data[:,3],c='r') 
	plot(Output[:,3],c='g') #g 

	title('x')

	figure(8)
	plot(Data[:,1],c='r')
	plot(Output[:,1],c='b') #b 
	plot(Data[:,4],c='r') 
	plot(Output[:,4],c='g') #g 
	title('y')


	figure(9)
	plot(Data[:,2],c='r')
	plot(Output[:,2],c='b') #b r
	plot(Data[:,5],c='r') 
	plot(Output[:,5],c='g') #g 

	title('z')

###
	show()


#	Write Coordinates
	Writer = csv.writer(open(file[:-4]+"_filt.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['RRoot_X','RRoot_Y','RRoot_Z','LRoot_X','LRoot_Y','LRoot_Z'])
	for N in range(0,len(Data[:,0])):
		Writer.writerow(Output[N])


######################################################################################################################################################
	


if __name__ == '__main__':

	try:
        	opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	

    	except getopt.error:
        	sys.stderr.write("%s: %s \nTry `%s --help` for more informatIon\n"
        		% (PROGNAME, e, PROGNAME))
        	sys.exit(1)


    	for o in opts:
        	if o in ('-h', '--help'):
        		usage(error=0)

    	if len(args) != 2:
        	usage()

    	main(args[0],args[1])
