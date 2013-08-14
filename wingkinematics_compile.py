#!/usr/bin/env python
import scipy.io
from numpy import *
import scipy
import getopt
import sys
import csv
import os
import re
import glob

# usage: 1 argument= path to folder with multiple csv files (angles_summary). Takes all files in folder and combines them into one file.

def main(path):

	os.system("mkdir %s"% (path+"/compiled/"))

	Writer = csv.writer(open(path+"/compiled/compiled.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

	Writer.writerow(["Bird","Maneuver","Trial_Time","Wingbeat#","Wingbeat_Length_DS", "Travel_Angle_DS", "Body_Angle_Lateral_DS","Body_Angle_Dorsal_DS","R_Stroke_Plane_Angle_DS","L_Stroke_Plane_Angle_DS","R_Avg_Elevation_Angle_Ground_DS","L_Avg_Elevation_Angle_Ground_DS", "R_Amplitude_Stroke_Plane_DS","L_Amplitude_Stroke_Plane_DS","R_Wing_Elevation_Amplitude_Stroke_Plane_DS","L_Wing_Elevation_Amplitude_Stroke_Plane_DS","R_Wingtip_Dist_Traveled_DS(mm)","R_Wingtip_Velocity_DS","L_Wingtip_Dist_Traveled_DS(mm)","L_Wingtip_Velocity_DS","Wingbeat#","Wingbeat_Length_US", "Travel_Angle_US", "Body_Angle_Lateral_US","Body_Angle_Dorsal_US","R_Stroke_Plane_Angle_US","L_Stroke_Plane_Angle_US","R_Avg_Elevation_Angle_Ground_US","L_Avg_Elevation_Angle_Ground_US", "R_Amplitude_Stroke_Plane_US","L_Amplitude_Stroke_Plane_US","R_Wing_Elevation_Amplitude_Stroke_Plane_US","L_Wing_Elevation_Amplitude_Stroke_Plane_US","R_Wingtip_Dist_Traveled_US","R_Wingtip_Velocity_US","L_Wingtip_Dist_Traveled_US","L_Wingtip_Velocity_US","X_vel_DS","Y_vel_DS","Z_vel_DS","Total_vel_DS","X_vel_US","Y_vel_US","Z_vel_US","Total_vel_US"])


	a=1

	for infile in glob.glob(os.path.join(path, '*.csv')):
	# infile stores the complete path of the file

		print infile
		
		infile2 = open(infile,"r")
		lines = infile2.readlines()
		(PATH, FILENAME) = os.path.split(infile)

    		Data= empty(((len(lines))-1,42),float)

    		for N in range(1,len(lines)):

			temp = str(lines[N]).split(',')    		
	
			Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]),float(temp[18]),float(temp[19]),float(temp[20]),float(temp[21]),float(temp[22]),float(temp[23]),float(temp[24]),float(temp[25]),float(temp[26]),float(temp[27]),float(temp[28]),float(temp[29]),float(temp[30]),float(temp[31]),float(temp[32]),float(temp[33]),float(temp[34]),float(temp[35]),float(temp[36]),float(temp[37]),float(temp[38]),float(temp[39]),float(temp[40]),float(temp[41]))

		for N in range(0,len(Data[:,0])): 
			Writer.writerow([FILENAME[26:36],FILENAME[42:47],FILENAME[37:41],Data[N,0],Data[N,1],Data[N,2],Data[N,3],Data[N,4],Data[N,5],Data[N,6],Data[N,7],Data[N,8],Data[N,9],Data[N,10],Data[N,11],Data[N,12],Data[N,13],Data[N,14],Data[N,15],Data[N,16],Data[N,17],Data[N,18],Data[N,19],Data[N,20],Data[N,21],Data[N,22],Data[N,23],Data[N,24],Data[N,25],Data[N,26],Data[N,27],Data[N,28],Data[N,29],Data[N,30],Data[N,31],Data[N,32],Data[N,33],Data[N,34],Data[N,35],Data[N,36],Data[N,37],Data[N,38],Data[N,39],Data[N,40],Data[N,41]])

		a=a+1

############################################################################################################
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

    	if len(args) !=1:
	       	usage()

    	main(args[0])
