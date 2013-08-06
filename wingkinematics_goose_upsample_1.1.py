#!/usr/bin/env python
from numpy import *
from math import *
from scipy import interpolate
import scipy
from Numeric import *
import os
import getopt
import sys
import csv
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def usage(error=1):
	usage = """\
Version # 1.1 4/7/2012

Usage: %s [INPUT_FILE_NAME][INPUT_FILE_NAME]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

LShoulder_X,Y,Z, LWrist_X,Y,Z, LWing_X,Y,Z,LSecond_X,Y,Z,LRoot_X,Y,Z,Head_X,Y,Z,Tail_X,Y,Z

Second file should contain 2 rows, with the data starting in the second row. This should be the frame where Pronation and Supination start. It MUST start with a Pronation and end with a Pronation



Takes Digitized points and timing of the pronation and supination estimated from the videos. Converts from in to cm. Upsamples data set (x10), and returns output file. Also, takes original Pronation Supination points and refines them to reflect the best points for the upsampled data- it goes through 15 iterations before returning the correct Prontion Supination times. Returns upsampled P+S times.


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




    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]),float(temp[18]),float(temp[19]),float(temp[20]))
	
	Data=Data*100	#convert m to cm

############################
#upsample data

	

	Data2= zeros(((((len(lines)-2)*10)+1),21), Float)

	print shape(Data2)

	for n in range(0,21):
	
		time=range(0,len(lines)-1)
		
		a= linspace(0,(len(lines)-2),num=((((len(time))-1)*10)+1))
				
		b= interpolate.splrep(time,Data[:,n])

		c = interpolate.splev(a,b)
	
		Data2[:,n]=c


###########################################################


#	Write Upsampled Coordinates
	Writer = csv.writer(open(file[:-4]+"_upsampled.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['shoulder_x','shoulder_y','shoulder_z','wrist_x','wrist_y','wrist_z','tip_x','tip_y','tip_z','secondary_x','secondary_y','secondary_z','root_x','root_y','root_z','head_x','head_y','head_z','tail_x','tail_y','tail_z']) 
	for N in range(0,len(Data2[:,0])):
		Writer.writerow(Data2[N])


#############################

	temp2= str(lines2[1]).split(',')
	U=[]
	
	for N in range(0,len(temp2)):	
		U.append((int(temp2[N])*10))
	print U		

#############################
	#convert Pro_Sup file for upsampled data




# Define Output Arrays


	Output1= zeros(((U[len(U)-1]-1),6))
	Output= zeros(((U[len(U)-1]-1),8))



# Read data from input array


	LSHOULDER= zeros((((len(lines)-2)*10)+1,3))
	LWRIST= zeros((((len(lines)-2)*10)+1,3))
	LWING= zeros((((len(lines)-2)*10)+1,3))
	LSECOND= zeros((((len(lines)-2)*10)+1,3))
	LROOT= zeros((((len(lines)-2)*10)+1,3))	
	HEAD= zeros((((len(lines)-2)*10)+1,3))
	TAIL= zeros((((len(lines)-2)*10)+1,3))
	

	LSHOULDER[:,0:3]=Data2[:,0:3]
	LWRIST[:,0:3]=Data2[:,3:6]
	LWING[:,0:3]=Data2[:,6:9]
	LSECOND[:,0:3]=Data2[:,9:12]
	LROOT[:,0:3]=Data2[:,12:15]
	HEAD[:,0:3]=Data2[:,15:18]	
	TAIL[:,0:3]=Data2[:,18:21]
	
	


# Center head at 0,0,- = subtract head (XY) coordinates from all vectors 

	Head1=HEAD-HEAD
#	Head[:,2]=HEAD[:,2]
	
	LShoulder1=LSHOULDER-HEAD	
#	LShoulder[:,2]=LSHOULDER[:,2]

	LWrist1=LWRIST-HEAD
#	LWrist[:,2]=LWRIST[:,2]

	LWing1=LWING-HEAD
#	LWing[:,2]=LTIP[:,2]

	LSecond1=LSECOND-HEAD
#	LSecond[:,2]=LSecond[:,2]
	
	LRoot1=LROOT-HEAD
#	LRoot[:,2]=LRoot[:,2]

	Tail1=TAIL-HEAD
#	Tail[:,2]=TAIL[:,2]



# Define global output data matrices
	LShoulder= zeros(((U[len(U)-1]-1),3))
	LWrist= zeros(((U[len(U)-1]-1),3))
	LWing= zeros(((U[len(U)-1]-1),3))
	LSecond= zeros(((U[len(U)-1]-1),3))
	LRoot= zeros(((U[len(U)-1]-1),3))
	Head= zeros(((U[len(U)-1]-1),3))
	Tail= zeros(((U[len(U)-1]-1),3))


	for N in range(0,20):
	
		Time_Wingbeat = ['Time_Wingbeat']
		Time_DS =['Time_DS']
		Time_US	=['Time_US']	


   # Calculate 
	
		for n in range((len(U)-1)):
		
		
		 	A = ((U[n]-1))	
			B = (U[n+1]-1)	
	
			Time_Wingbeat.append(B-A)

			LShoulder[A:B,:]= LShoulder1[A:B,:]
			LWrist[A:B,:]= LWrist1[A:B,:]		
			LWing[A:B,:]= LWing1[A:B,:]
			LSecond[A:B,:]= LSecond1[A:B,:]
			LRoot[A:B,:]= LRoot1[A:B,:]
			Head[A:B,:]= Head1[A:B,:]
			Tail[A:B,:]= Tail1[A:B,:]
	

		for n in range(1,(len(Time_Wingbeat))):

			if n%2==1:
				Time_DS.append(Time_Wingbeat[n])
		
			else:
				Time_US.append(Time_Wingbeat[n])


	
###################################################################################################################################33		
# Body Angle: Head to tail



		BodyXYZ=Head-Tail

		BodyXZ= zeros(((len(BodyXYZ[:,0])),3), Float)
		BodyYZ= zeros(((len(BodyXYZ[:,0])),3), Float)		
	
		BodyXZ[:,0]=BodyXYZ[:,0]
		BodyXZ[:,1]=0
		BodyXZ[:,2]=BodyXYZ[:,2]
	

		LengthBodyXZ=sqrt((BodyXYZ[:,0]**2)+(BodyXYZ[:,2]**2))

		Zaxis=array((0,0,1))
	



		BodyAngleXZ= zeros(((len(BodyXYZ[:,0])),1), Float)


		for n in range(len(BodyXYZ[:,0])):

			if BodyXYZ[n,0]>0:
				BodyAngleXZ[n]= acos((dot(BodyXZ[n,:],Zaxis))/(LengthBodyXZ[n]))
	
			else:
				BodyAngleXZ[n]= -acos((dot(BodyXZ[n,:],Zaxis))/(LengthBodyXZ[n]))
	


		BodyYZ[:,0]=0
		BodyYZ[:,1]=BodyXYZ[:,1]
		BodyYZ[:,2]=BodyXYZ[:,2]

		LengthBodyYZ=sqrt((BodyXYZ[:,1]**2)+(BodyXYZ[:,2]**2))

		BodyAngleYZ= zeros(((len(BodyXYZ[:,0])),1), Float)	


		for n in range(len(BodyXYZ[:,0])):

			if BodyXYZ[n,1]>0:
				BodyAngleYZ[n]= acos((dot(BodyYZ[n,:],Zaxis))/(LengthBodyYZ[n]))
	
			else:
				BodyAngleYZ[n]= -acos((dot(BodyYZ[n,:],Zaxis))/(LengthBodyYZ[n]))

		Output[:,0]=(90-degrees(BodyAngleXZ[:,0]))
		Output[:,1]=(degrees(BodyAngleYZ[:,0]))






##########################################################################################################





# Calculate Angles relative to all strokeplanes

		def StrokeAngle(R,S):
			


	# Calculate Reduced Major Axis Regression using LWing columns X and Z


			correlation_coefficient = corrcoef([LWing[R:S,0],LWing[R:S,2]])
			

			if correlation_coefficient[0,1]<0:
				sign=-1
			else:
				sign=1


			Mean1= mean(LWing[R:S,0])

			Std1= std(LWing[R:S,0],ddof=1)

			Mean2=mean(LWing[R:S,2])
			Std2=std(LWing[R:S,2],ddof=1)

			A= sign*Std2/Std1
			B= Mean2-(A*Mean1)

			x=array((-100,0,100))	
			y=(A*x)+B
			y2=(A*x)

		#angle to horizontal

			Xaxis=array((1,0,0))

			StrokeVector=(x[2],0,y2[2])
			LengthStrokeVector=sqrt((StrokeVector[0]**2)+(StrokeVector[2]**2))

			if StrokeVector[2]>0:
				StrokePlaneAngle= -acos(((dot(StrokeVector,Xaxis))/(LengthStrokeVector)))

			else:
				StrokePlaneAngle= acos(((dot(StrokeVector,Xaxis))/(LengthStrokeVector)))


			RotStrokeAngle = ([(cos(StrokePlaneAngle), 0, -sin(StrokePlaneAngle)),(0,1,0),(sin(StrokePlaneAngle),0,cos(StrokePlaneAngle))])

		
			

		# Rotate around Y axis,


			LShoulder2=transpose(matrixmultiply(RotStrokeAngle,transpose(LShoulder)))
			LWing2=transpose(matrixmultiply(RotStrokeAngle,transpose(LWing)))
			Head2=transpose(matrixmultiply(RotStrokeAngle,transpose(Head)))
			Tail2=transpose(matrixmultiply(RotStrokeAngle,transpose(Tail)))



	# calculate deviation from stroke plane, distance of shoulder to stroke plane



			Deviation=LWing2[:,2]-B
			ShoulderDist=B-LShoulder2[:,2]		






	#position and angle of wing to stroke plane 

		#Project point into XY plane (remember stroke plane has been rotated to be parallel to XY plane)




		
			LWing2XYZ=LWing2-LShoulder2
			LengthLWing2XYZ=sqrt((LWing2XYZ[:,0]**2)+(LWing2XYZ[:,1]**2)+(LWing2XYZ[:,2]**2))	
	
			LWing2XY=LWing2-LShoulder2
			LWing2XY[:,2]=0
			LengthLWing2XY=sqrt((LWing2XY[:,0]**2)+(LWing2XY[:,1]**2)+(LWing2XY[:,2]**2))

			WingAngle=arccos((LWing2XYZ[:,0]*LWing2XY[:,0]+LWing2XYZ[:,1]*LWing2XY[:,1])/((LengthLWing2XYZ)*(LengthLWing2XY)))*np.sign([LWing2XYZ[:,2]])
	


	# calculate position relative to strokeplane
			NegXaxis=(-1,0,0)

		
			Position=arccos((LWing2XY[:,0]*NegXaxis[0]+LWing2XY[:,1]*NegXaxis[1]+LWing2XY[:,2]*NegXaxis[2])/(LengthLWing2XY))





	# position and angle of wing relative to horizontal line through shoulder
		

		#Transform Shoulder and Wingtip to Shoulder centered Frame Of Reference


			LShoulder_Sh = LShoulder-LShoulder
			LWing_Sh = LWing - LShoulder
	


		#Project Wingtip onto XY Plane
	

			LWing_ShXY = LWing - LShoulder
			LWing_ShXY[:,2]=0


			Length_LWing_Sh = sqrt((LWing_Sh[:,0]**2)+(LWing_Sh[:,1]**2)+(LWing_Sh[:,2]**2))
			Length_LWing_ShXY = sqrt((LWing_ShXY[:,0]**2)+(LWing_ShXY[:,1]**2)+(LWing_ShXY[:,2]**2))


			WingAngle_Ground= arccos((LWing_Sh[:,0]*LWing_ShXY[:,0]+LWing_Sh[:,1]*LWing_ShXY[:,1])/((Length_LWing_Sh)*(Length_LWing_ShXY)))*np.sign([LWing_Sh[:,2]])

			Position_Ground= arccos((LWing_ShXY[:,0]*NegXaxis[0]+LWing_ShXY[:,1]*NegXaxis[1]+LWing_ShXY[:,2]*NegXaxis[2])/(Length_LWing_ShXY))
		

			WingAngle_Ground = nan_to_num(WingAngle_Ground)





# Wingtip distance traveled

			Wingtip_Dist_Trav=0

			for n in range(R,S-1):

				
	
				Wingtip_Dist_Trav=Wingtip_Dist_Trav+(sqrt(((LWing[n+1,0]-LWing[n,0])**2)+((LWing[n+1,1]-LWing[n,1])**2)+((LWing[n+1,2]-LWing[n,2])**2)))
	
							

#	Write to output arrays
			Output1[:,0]=(degrees(StrokePlaneAngle))
			Output1[:,1]=(degrees(Position_Ground))
			Output1[:,2]=(degrees(WingAngle_Ground))
			Output1[:,3]=(degrees(Position))
			Output1[:,4]=(degrees(WingAngle))
			Output1[:,5]=(Wingtip_Dist_Trav)



##################################################################################################	


	
#Call programs

	

#####################################################################################################################


# Calculations per upstroke/downstroke
				
		for n in range(len(U)-1):		
		

# left wing
			if n%2==0:
				Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Left'
			else:
				Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Left'

			StrokeAngle((U[n]-1),(U[n+1]-1))



			Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
			Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
			Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
			Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
			Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
			Output[(U[n]-1):(U[n+1]-1),7] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistanceTraveled


#########################################################################################################################


# Calculate New Pronation and Supinations based on the RIGHT and Left wings and export new pronation supination files
		PronationSupinationHeader=['PronationSupinationHeader']
		NewPronationSupinationL=['NewPronationSupinationL']
		NewPronationSupinationL.append(U[0])
			
	
		PronationSupinationHeader.append('P')
	
		Z=[]
		Z.append(int(U[0]))

		for n in range(len(U)-1):		
			
			if n%2==0: 

				NewPronationSupinationL.append(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))
				PronationSupinationHeader.append('S')

				Z.append(int((np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5])+(U[n]))))

			
			else:
				NewPronationSupinationL.append(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5])+(U[n]))
				PronationSupinationHeader.append('P')


				Z.append(int((np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5])+(U[n]))))


		U=[]
		U=Z
		print U



	Writer = csv.writer(open("pro_sup_NEW.csv",'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(PronationSupinationHeader[1:])
	Writer.writerow(NewPronationSupinationL[1:])


###########################################################################################################################

#	clf()
#	plot(LWING[:,1],LWING[:,2],c='b')
#	scatter(HEAD[:,1],HEAD[:,2],c='m')
		
#	for n in range(len(U)-1):
#		scatter(LWING[U[n],1],LWING[U[n],2],c='r')		

	
#	axes().set_aspect('equal', 'datalim')
#	grid(True)
#	show()	
#	savefig('stroke_endpoints_'+file[:-4]+'.svg')

	colors= "k"

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	
	plot(TAIL[:,0],TAIL[:,1],TAIL[:,2],c='m')
	plot(LSECOND[:,0],LSECOND[:,1],LSECOND[:,2],c='g')
	plot(LROOT[:,0],LROOT[:,1],LROOT[:,2],c='r')
	plot(LWRIST[:,0],LWRIST[:,1],LWRIST[:,2],c='c')
	plot(LSHOULDER[:,0],LSHOULDER[:,1],LSHOULDER[:,2],c='k')
	plot(LWING[:,0],LWING[:,1],LWING[:,2],c='b')
	plot(HEAD[:,0],HEAD[:,1],HEAD[:,2],c='#6600CC')

	for n in range(len(U)-1):
		ax.scatter(LWING[U[n],0],LWING[U[n],1],LWING[U[n],2], c="r")

	ax.set_aspect('equal','datalim')

	show()


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
