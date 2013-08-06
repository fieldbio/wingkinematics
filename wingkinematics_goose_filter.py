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

Usage: %s [INPUT_FILE_NAME][FILTERFACTOR_FILE_NAME]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

LShoulder_X,Y,Z, LWrist_X,Y,Z, LWing_X,Y,Z,LSecond_X,Y,Z,LRoot_X,Y,Z,Head_X,Y,Z,Tail_X,Y,Z

Second file should contain 2 rows, with the data starting in the second row. This should be the filter factors used for xyz coordinates. Larger numbers = less smoothing.



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


    	Data= zeros(((len(lines)-1),21), Float)
    	Filter= zeros((1,21), Float)



    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]),float(temp[18]),float(temp[19]),float(temp[20]))
	


#############################

	temp2= str(lines2[1]).split(',')
	
	Filter[0,:]=(float(temp2[0]),float(temp2[1]),float(temp2[2]),float(temp2[3]),float(temp2[4]),float(temp2[5]),float(temp2[6]),float(temp2[7]),float(temp2[8]),float(temp2[9]),float(temp2[10]),float(temp2[11]),float(temp2[12]),float(temp2[13]),float(temp2[14]),float(temp2[15]),float(temp2[16]),float(temp2[17]),float(temp2[18]),float(temp2[19]),float(temp2[20]))

#############################


	fundamental_frequency=40
	sample_rate=1000

	Output=zeros(((len(lines)-1),21), Float)

	for n in range(0,21):
		
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
	title('LShoulder_X')
	
	subplot(334)
	plot(Data[:,1])
	plot(Output[:,1],c='r')
	title('LShoulder_Y')

	subplot(337)
	plot(Data[:,2])
	plot(Output[:,2],c='r')
	title('LShoulder_Z')


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
	title('LWrist_X')

	subplot(334)
	plot(Data[:,4])
	plot(Output[:,4],c='r')
	title('LWrist_Y')

	subplot(337)
	plot(Data[:,5])
	plot(Output[:,5],c='r')
	title('LWrist_Z')



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

	figure(3)
	subplot(331)
	plot(Data[:,6])
	plot(Output[:,6],c='r')
	title('LTip_X')

	subplot(334)
	plot(Data[:,7])
	plot(Output[:,7],c='r')
	title('LTip_Y')

	subplot(337)
	plot(Data[:,8])
	plot(Output[:,8],c='r')
	title('LTip_Z')


	p1=subplot(332)
	plot(Data[100:150,6],Data[100:150,7])
	plot(Output[100:150,6],Output[100:150,7],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,6],Data[100:150,8])
	plot(Output[100:150,6],Output[100:150,8],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,7],Data[100:150,8])
	plot(Output[100:150,7],Output[100:150,8],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,6],Data[200:250,7])
	plot(Output[200:250,6],Output[200:250,7],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,6],Data[200:250,8])
	plot(Output[200:250,6],Output[200:250,8],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,7],Data[200:250,8])
	plot(Output[200:250,7],Output[200:250,8],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


##
	figure(4)
	subplot(331)
	plot(Data[:,9])
	plot(Output[:,9],c='r')
	title('LSecond_X')

	subplot(334)
	plot(Data[:,10])
	plot(Output[:,10],c='r')
	title('LSecond_Y')

	subplot(337)
	plot(Data[:,11])
	plot(Output[:,11],c='r')
	title('LSecond_Z')

	p1=subplot(332)
	plot(Data[100:150,9],Data[100:150,10])
	plot(Output[100:150,9],Output[100:150,10],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,9],Data[100:150,11])
	plot(Output[100:150,9],Output[100:150,11],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,10],Data[100:150,11])
	plot(Output[100:150,10],Output[100:150,11],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,9],Data[200:250,10])
	plot(Output[200:250,9],Output[200:250,10],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,9],Data[200:250,11])
	plot(Output[200:250,9],Output[200:250,11],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,10],Data[200:250,11])
	plot(Output[200:250,10],Output[200:250,11],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 








##
	figure(5)
	subplot(331)
	plot(Data[:,12])
	plot(Output[:,12],c='r')
	title('LRoot_X')

	subplot(334)
	plot(Data[:,13])
	plot(Output[:,13],c='r')
	title('LRoot_Y')

	subplot(337)
	plot(Data[:,14])
	plot(Output[:,14],c='r')
	title('LRoot_Z')


	p1=subplot(332)
	plot(Data[100:150,12],Data[100:150,13])
	plot(Output[100:150,12],Output[100:150,13],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,12],Data[100:150,14])
	plot(Output[100:150,12],Output[100:150,14],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,13],Data[100:150,14])
	plot(Output[100:150,13],Output[100:150,14],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,12],Data[200:250,13])
	plot(Output[200:250,12],Output[200:250,13],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,12],Data[200:250,14])
	plot(Output[200:250,12],Output[200:250,14],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,13],Data[200:250,14])
	plot(Output[200:250,13],Output[200:250,14],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 




##

	figure(6)
	subplot(331)
	plot(Data[:,15])
	plot(Output[:,15],c='r')
	title('Head_X')

	subplot(334)
	plot(Data[:,16])
	plot(Output[:,16],c='r')
	title('Head_Y')

	subplot(337)
	plot(Data[:,17])
	plot(Output[:,17],c='r')
	title('Head_Z')



	p1=subplot(332)
	plot(Data[100:150,15],Data[100:150,16])
	plot(Output[100:150,15],Output[100:150,16],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,15],Data[100:150,17])
	plot(Output[100:150,15],Output[100:150,17],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,16],Data[100:150,17])
	plot(Output[100:150,16],Output[100:150,17],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,15],Data[200:250,16])
	plot(Output[200:250,15],Output[200:250,16],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,15],Data[200:250,17])
	plot(Output[200:250,15],Output[200:250,17],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,16],Data[200:250,17])
	plot(Output[200:250,16],Output[200:250,17],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 

##

	figure(7)
	subplot(331)
	plot(Data[:,18])
	plot(Output[:,18],c='r')
	title('Tail_X')

	subplot(334)
	plot(Data[:,19])
	plot(Output[:,19],c='r')
	title('Tail_Y')

	subplot(337)
	plot(Data[:,20])
	plot(Output[:,20],c='r')
	title('Tail_Z')



	p1=subplot(332)
	plot(Data[100:150,18],Data[100:150,19])
	plot(Output[100:150,18],Output[100:150,19],c='r')
	title('100-150_XY')
	p1.set_aspect('equal', adjustable='datalim') 
	
	p2=subplot(335)
	plot(Data[100:150,18],Data[100:150,19])
	plot(Output[100:150,18],Output[100:150,19],c='r')
	title('100-150_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(338)
	plot(Data[100:150,19],Data[100:150,20])
	plot(Output[100:150,19],Output[100:150,20],c='r')
	title('100-150_YZ')
	p3.set_aspect('equal', adjustable='datalim') 


	p1=subplot(333)
	plot(Data[200:250,18],Data[200:250,19])
	plot(Output[200:250,18],Output[200:250,19],c='r')
	title('200-250_XY')
	p1.set_aspect('equal', adjustable='datalim') 

	p2=subplot(336)
	plot(Data[200:250,18],Data[200:250,20])
	plot(Output[200:250,18],Output[200:250,20],c='r')
	title('200-250_XZ')
	p2.set_aspect('equal', adjustable='datalim') 

	p3=subplot(339)
	plot(Data[200:250,19],Data[200:250,20])
	plot(Output[200:250,19],Output[200:250,20],c='r')
	title('200-250_YZ')
	p3.set_aspect('equal', adjustable='datalim') 



	figure(8)
	p=subplot(111)

	plot(Data[:,0],c='r')
	plot(Output[:,0],c='y') #y shoulder
	plot(Data[:,3],c='r') 
	plot(Output[:,3],c='k') #g wrist
	plot(Data[:,6],c='r')
	plot(Output[:,6],c='b') #k tip
	plot(Data[:,9],c='r')
	plot(Output[:,9],c='g') #c second
	plot(Data[:,12],c='r')
	plot(Output[:,12],c='c') #m root
	plot(Data[:,15],c='r')
	plot(Output[:,15],c='m') #y head
	plot(Data[:,18],c='r')
	plot(Output[:,18],c='b') #y tail
	title('x')

	figure(8)
	plot(Data[:,1],c='r')
	plot(Output[:,1],c='y') #y shoulder
	plot(Data[:,4],c='r') 
	plot(Output[:,4],c='k') #k wrist
	plot(Data[:,7],c='r')
	plot(Output[:,7],c='b') #b tip
	plot(Data[:,10],c='r')
	plot(Output[:,10],c='g') #g second
	plot(Data[:,13],c='r')
	plot(Output[:,13],c='c') #c root
	plot(Data[:,16],c='r')
	plot(Output[:,16],c='m') #m head
	plot(Data[:,19],c='r')
	plot(Output[:,19],c='b') #b tail
	title('y')


	figure(9)
	plot(Data[:,2],c='r')
	plot(Output[:,2],c='y') #y shoulder
	plot(Data[:,5],c='r') 
	plot(Output[:,5],c='k') #k wrist
	plot(Data[:,8],c='r')
	plot(Output[:,8],c='b') #b tip
	plot(Data[:,11],c='r')
	plot(Output[:,11],c='g') #g second
	plot(Data[:,14],c='r')
	plot(Output[:,14],c='c') #c root
	plot(Data[:,17],c='r')
	plot(Output[:,17],c='m') #m head
	plot(Data[:,20],c='r')
	plot(Output[:,20],c='b') #b tail
	title('z')

###
	show()


#	Write Coordinates
	Writer = csv.writer(open(file[:-4]+"_filt.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['Shoulder_X','Shoulder_Y','Shoulder_Z','Wrist_X','Wrist_Y','Wrist_Z','Tip_X','Tip_Y','Tip_Z','Second_X','Second_Y','Second_Z','Root_X', 'Root_Y','Root_Z','Head_X','Head_Y','Head_Z','Tail_X','Tail_Y','Tail_Z'])
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
