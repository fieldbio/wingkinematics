#!/usr/bin/env python
from numpy import *
from math import *
from scipy import interpolate
import scipy
import os
import getopt
import sys
import csv
from pylab import *


def usage(error=1):
	usage = """\
Version # 1.0 6/23/2011

Usage: %s [INPUT_FILE_NAME][INPUT_FILE_NAME]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

RShoulder_X, RShoulder_Y, RShoulder_Z, RWing_X, RWing_Y, RWing_Z, LShoulder_X, LShoulder_Y, LShoulder_Z, LWing_X, LWing_Y, LWing_Z, Head_X, Head_Y, Head_Z, Tail_X, Tail_Y, TAIL_Z

Second file should contain 2 rows, with the data starting in the second row. This should be the frame where Pronation and Supination start. It MUST start with a Pronation and end with a Pronation



Takes Digitized points and timing of the pronation and supination estimated from the videos. Converts from in to mm. Upsamples data set (x10), and returns output file. Also, takes original Pronation Supination points and refines them to reflect the best points for the upsampled data- it goes through 15 iterations before returning the correct Prontion Supination times. Returns P+S times in two files: Left and Right individually (for EMG analysis) and the LR average (for wingkinematics).


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
	seterr(all='ignore')
# input files

	inFile = open(file,"r")
    	lines = inFile.readlines()	

	inFile2 = open(time,"r")
	lines2 = inFile2.readlines()	


    	Data= zeros(((len(lines)-1),18), float)




    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]))
	
	Data=Data*25.4	#convert in to mm

############################
#upsample data


	Data2= zeros(((((len(lines)-2)*10)+1),18), float)



	for n in range(0,18):
	
		time=range(0,len(lines)-1)
		
		a= linspace(0,(len(lines)-2),num=((((len(time))-1)*10)+1))
				
		b= interpolate.splrep(time,Data[:,n])

		c = interpolate.splev(a,b)
	
		Data2[:,n]=c


###########################################################


#	Write Upsampled Coordinates
	Writer = csv.writer(open(file[:-4]+"_upsampled.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['RShoulder_X','RShoulder_Y','RShoulder_Z','RWing_X','RWing_Y','RWing_Z','LShoulder_X','LShoulder_Y','LShoulder_Z','LWing_X', 'LWing_Y','LWing_Z','Head_X','Head_Y','Head_Z','Tail_X','Tail_Y','Tail_Z'])
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
	Output= zeros(((U[len(U)-1]-1),14))



# Read data from input array


	RSHOULDER= zeros((((len(lines)-2)*10)+1,3))
	RWING= zeros((((len(lines)-2)*10)+1,3))
	LSHOULDER= zeros((((len(lines)-2)*10)+1,3))
	LWING= zeros((((len(lines)-2)*10)+1,3))
	HEAD= zeros((((len(lines)-2)*10)+1,3))
	TAIL= zeros((((len(lines)-2)*10)+1,3))
	

	RSHOULDER[:,0:3]=Data2[:,0:3]
	RWING[:,0:3]=Data2[:,3:6]
	LSHOULDER[:,0:3]=Data2[:,6:9]
	LWING[:,0:3]=Data2[:,9:12]
	HEAD[:,0:3]=Data2[:,12:15]
	TAIL[:,0:3]=Data2[:,15:18]	





# Center head at 0,0,- = subtract head (XY) coordinates from all vectors 

	Head1=HEAD-HEAD
	Head1[:,2]=HEAD[:,2]
	
	RShoulder1=RSHOULDER-HEAD	
	RShoulder1[:,2]=RSHOULDER[:,2]

	RWing1=RWING-HEAD
	RWing1[:,2]=RWING[:,2]

	
	LShoulder1=LSHOULDER-HEAD
	LShoulder1[:,2]=LSHOULDER[:,2]
	LWing1=LWING-HEAD
	LWing1[:,2]=LWING[:,2]
	Tail1=TAIL-HEAD
	Tail1[:,2]=TAIL[:,2]



# Define global output data matrices
	RShoulder= zeros(((U[len(U)-1]-1),3))
	RWing= zeros(((U[len(U)-1]-1),3))
	LShoulder= zeros(((U[len(U)-1]-1),3))
	LWing= zeros(((U[len(U)-1]-1),3))
	Head= zeros(((U[len(U)-1]-1),3))
	Tail= zeros(((U[len(U)-1]-1),3))



# Transform all coordinates to Wingtip frame
	for N in range(0,20):

		Rotation_Angle = ['Rotation_Angle']
		Rotation_Angle_DS = ['Rotation_Angle_DS']
		Rotation_Angle_US =['Rotation_Angle_US']	
		Time_Wingbeat = ['Time_Wingbeat']
		Time_DS =['Time_DS']
		Time_US	=['Time_US']	


   # Calculate Rotation angle for every downstroke and upstroke
	
		for n in range((len(U)-1)):
		
		
		 	A = ((U[n]-1))	
			B = (U[n+1]-1)	
			Midpoint_Start = (RWing1[A]+LWing1[A])/2
			Midpoint_Start[2]=0

			Midpoint_End = (RWing1[B]+LWing1[B])/2
			Midpoint_End[2] = 0

			if n%2==0:
				Mid = (Midpoint_End-Midpoint_Start)
			else:
				Mid = (Midpoint_Start-Midpoint_End)
			
			LengthMid= sqrt(Mid[0]**2 + Mid[1]**2)
	
			Xaxis=(1,0,0)
		
	
		
   # Calculate rotation angle between Midpoint and Xaxis vector. Create adjustment factor for acos: if Y is positive, subtract angle from 360 degrees to find rotation angle		
		
			if Mid[1]<0:
				ZRotationAngle= radians(360)-acos(((dot(Mid,Xaxis))/(LengthMid)))
		
			else: 
				ZRotationAngle= acos(((dot(Mid,Xaxis))/(LengthMid)))


			Rotation_Angle.append(360-(degrees(ZRotationAngle)))
			Time_Wingbeat.append(B-A)
	

#	Create rotation matrix, and multiply times Body1 and RShoulder1 vectors

			RotZ = array(((cos(ZRotationAngle),sin(ZRotationAngle),0),(-sin(ZRotationAngle),cos(ZRotationAngle),0),(0,0,1)))
		
			RShoulder2=dot(RotZ,transpose(RShoulder1[A:B,:]))
			RWing2=dot(RotZ,transpose(RWing1[A:B,:]))
			LShoulder2=dot(RotZ,transpose(LShoulder1[A:B,:]))
			LWing2=dot(RotZ,transpose(LWing1[A:B,:]))
			Head2=dot(RotZ,transpose(Head1[A:B,:]))
			Tail2=dot(RotZ,transpose(Tail1[A:B,:]))

			RShoulder3=transpose(RShoulder2)
			RWing3=transpose(RWing2)
			LWing3=transpose(LWing2)
			LShoulder3=transpose(LShoulder2)		
			Head3=transpose(Head2)
			Tail3=transpose(Tail2)

			RShoulder[A:B,:]=RShoulder3[:,:]
			RWing[A:B,:]=RWing3[:,:]
			LShoulder[A:B,:]=LShoulder3[:,:]
			LWing[A:B,:]= LWing3[:,:]
			Head[A:B,:]= Head3[:,:]
			Tail[A:B,:]=Tail3[:,:]



# Create output array for transformed coordinates
		
			Transformed=hstack((RShoulder, RWing, LShoulder, LWing, Head, Tail))
	
		
#TRANSFORMATION COMPLETED

##############################################################################################################################

		
	
	
		for n in range(1,(len(Rotation_Angle)-1)):
			if n%2==1:
		
				if (Rotation_Angle[n+1]-Rotation_Angle[n])<-180:			
					Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n]+360)
	
				elif (Rotation_Angle[n+1]-Rotation_Angle[n])>180:
					Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n]-360)
	
				else:
					Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n])



		 	else:	

				if (Rotation_Angle[n+1]-Rotation_Angle[n])<-180:			
					Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n]+360)

				elif (Rotation_Angle[n+1]-Rotation_Angle[n])>180:
					Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n]-360)

				else:
					Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n])	
		

				

		for n in range(1,(len(Time_Wingbeat))):
			if n%2==1:
				Time_DS.append(Time_Wingbeat[n])
		
			else:
				Time_US.append(Time_Wingbeat[n])
	
###################################################################################################################################33		
# Body Angle: Head to tail

		Body= ((RShoulder+LShoulder)/2)

		BodyXYZ=Head-Tail

		BodyXZ= zeros(((len(Body)),3), float)
		BodyYZ= zeros(((len(Body)),3), float)		
	
		BodyXZ[:,0]=BodyXYZ[:,0]
		BodyXZ[:,1]=0
		BodyXZ[:,2]=BodyXYZ[:,2]
	

		LengthBodyXZ=sqrt((BodyXYZ[:,0]**2)+(BodyXYZ[:,2]**2))

		Zaxis=array((0,0,1))
	



		BodyAngleXZ= zeros(((len(Body)),1), float)	


		for n in range(len(Body)):
			
			if BodyXYZ[n,0]>0:
				BodyAngleXZ[n]= acos((dot(BodyXZ[n,:],Zaxis))/(LengthBodyXZ[n]))
	
			else:
				BodyAngleXZ[n]= -acos((dot(BodyXZ[n,:],Zaxis))/(LengthBodyXZ[n]))
	


		BodyYZ[:,0]=0
		BodyYZ[:,1]=BodyXYZ[:,1]
		BodyYZ[:,2]=BodyXYZ[:,2]

		LengthBodyYZ=sqrt((BodyXYZ[:,1]**2)+(BodyXYZ[:,2]**2))

		BodyAngleYZ= zeros(((len(Body)),1), float)	


		for n in range(len(Body)):

			if BodyXYZ[n,1]>0:
				BodyAngleYZ[n]= acos((dot(BodyYZ[n,:],Zaxis))/(LengthBodyYZ[n]))
	
			else:
				BodyAngleYZ[n]= -acos((dot(BodyYZ[n,:],Zaxis))/(LengthBodyYZ[n]))

		Output[:,0]=(90-degrees(BodyAngleXZ[:,0]))
		Output[:,1]=(degrees(BodyAngleYZ[:,0]))






##########################################################################################################





# Calculate Angles relative to all strokeplanes

		def StrokeAngle(R,S,T):


	# Calculate Reduced Major Axis Regression using RWing columns X and Z

			if T==1:

				correlation_coefficient = corrcoef([RWing[R:S,0],RWing[R:S,2]])
	
				if correlation_coefficient[0,1]<0:
					sign=-1
				else:
					sign=1

	
				Mean1= mean(RWing[R:S,0])

				Std1= std(RWing[R:S,0])

				Mean2=mean(RWing[R:S,2])
				Std2=std(RWing[R:S,2])

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
	

	# Calculate Reduced Major Axis Regression using LWing columns X and Z

			elif T==2:

				correlation_coefficient = corrcoef([LWing[R:S,0],LWing[R:S,2]])

				if correlation_coefficient[0,1]<0:
					sign=-1
				else:
					sign=1

				Mean1= mean(LWing[R:S,0])

				Std1= std(LWing[R:S,0])

				Mean2=mean(LWing[R:S,2])
				Std2=std(LWing[R:S,2])

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


			RShoulder2=transpose(dot(RotStrokeAngle,transpose(RShoulder)))
			RWing2=transpose(dot(RotStrokeAngle,transpose(RWing)))
			LShoulder2=transpose(dot(RotStrokeAngle,transpose(LShoulder)))
			LWing2=transpose(dot(RotStrokeAngle,transpose(LWing)))
			Head2=transpose(dot(RotStrokeAngle,transpose(Head)))
			Tail2=transpose(dot(RotStrokeAngle,transpose(Tail)))



	# calculate deviation from stroke plane, distance of shoulder to stroke plane
	
			if T==1:	
				Deviation=RWing2[:,2]-B		
				ShoulderDist=B-RShoulder2[:,2]


			else:
				Deviation=LWing2[:,2]-B
				ShoulderDist=B-LShoulder2[:,2]		






	#position and angle of wing to stroke plane 

		#Project point into XY plane (remember stroke plane has been rotated to be parallel to XY plane)

			if T==1:
				RWing2XYZ=RWing2-RShoulder2
				LengthRWing2XYZ=sqrt((RWing2XYZ[:,0]**2)+(RWing2XYZ[:,1]**2)+(RWing2XYZ[:,2]**2))	
	
				RWing2XY=RWing2-RShoulder2
				RWing2XY[:,2]=0
				LengthRWing2XY=sqrt((RWing2XY[:,0]**2)+(RWing2XY[:,1]**2)+(RWing2XY[:,2]**2))

				WingAngle=arccos((RWing2XYZ[:,0]*RWing2XY[:,0]+RWing2XYZ[:,1]*RWing2XY[:,1])/((LengthRWing2XYZ)*(LengthRWing2XY)))*np.sign([RWing2XYZ[:,2]])


			else:
				LWing2XYZ=LWing2-LShoulder2
				LengthLWing2XYZ=sqrt((LWing2XYZ[:,0]**2)+(LWing2XYZ[:,1]**2)+(LWing2XYZ[:,2]**2))	
	
				LWing2XY=LWing2-LShoulder2
				LWing2XY[:,2]=0
				LengthLWing2XY=sqrt((LWing2XY[:,0]**2)+(LWing2XY[:,1]**2)+(LWing2XY[:,2]**2))

				WingAngle=arccos((LWing2XYZ[:,0]*LWing2XY[:,0]+LWing2XYZ[:,1]*LWing2XY[:,1])/((LengthLWing2XYZ)*(LengthLWing2XY)))*np.sign([LWing2XYZ[:,2]])
	


	# calculate position relative to strokeplane
			NegXaxis=(-1,0,0)

			if T==1:
				Position=arccos((RWing2XY[:,0]*NegXaxis[0]+RWing2XY[:,1]*NegXaxis[1]+RWing2XY[:,2]*NegXaxis[2])/(LengthRWing2XY))
			else:			
				Position=arccos((LWing2XY[:,0]*NegXaxis[0]+LWing2XY[:,1]*NegXaxis[1]+LWing2XY[:,2]*NegXaxis[2])/(LengthLWing2XY))





	# position and angle of wing relative to horizontal line through shoulder
		

		#Transform Shoulder and Wingtip to Shoulder centered Frame Of Reference
		
			RShoulder_Sh = RShoulder-RShoulder
			RWing_Sh = RWing - RShoulder

			LShoulder_Sh = LShoulder-LShoulder
			LWing_Sh = LWing - LShoulder
	


		#Project Wingtip onto XY Plane

			RWing_ShXY = RWing - RShoulder
			RWing_ShXY[:,2]=0	

			LWing_ShXY = LWing - LShoulder
			LWing_ShXY[:,2]=0

			if T==1:
				Length_RWing_Sh = sqrt((RWing_Sh[:,0]**2)+(RWing_Sh[:,1]**2)+(RWing_Sh[:,2]**2))
				Length_RWing_ShXY = sqrt((RWing_ShXY[:,0]**2)+(RWing_ShXY[:,1]**2)+(RWing_ShXY[:,2]**2))


				WingAngle_Ground= arccos((RWing_Sh[:,0]*RWing_ShXY[:,0]+RWing_Sh[:,1]*RWing_ShXY[:,1])/((Length_RWing_Sh)*(Length_RWing_ShXY)))*np.sign([RWing_Sh[:,2]])

				Position_Ground= arccos((RWing_ShXY[:,0]*NegXaxis[0]+RWing_ShXY[:,1]*NegXaxis[1]+RWing_ShXY[:,2]*NegXaxis[2])/(Length_RWing_ShXY))


			else:
				Length_LWing_Sh = sqrt((LWing_Sh[:,0]**2)+(LWing_Sh[:,1]**2)+(LWing_Sh[:,2]**2))
				Length_LWing_ShXY = sqrt((LWing_ShXY[:,0]**2)+(LWing_ShXY[:,1]**2)+(LWing_ShXY[:,2]**2))


				WingAngle_Ground= arccos((LWing_Sh[:,0]*LWing_ShXY[:,0]+LWing_Sh[:,1]*LWing_ShXY[:,1])/((Length_LWing_Sh)*(Length_LWing_ShXY)))*np.sign([LWing_Sh[:,2]])

				Position_Ground= arccos((LWing_ShXY[:,0]*NegXaxis[0]+LWing_ShXY[:,1]*NegXaxis[1]+LWing_ShXY[:,2]*NegXaxis[2])/(Length_LWing_ShXY))
		

			WingAngle_Ground = nan_to_num(WingAngle_Ground)





# Wingtip distance traveled

			Wingtip_Dist_Trav=0

			for n in range(R,S-1):
				if T==1:
				
					Wingtip_Dist_Trav=Wingtip_Dist_Trav+(sqrt(((RWing[n+1,0]-RWing[n,0])**2)+((RWing[n+1,1]-RWing[n,1])**2)+((RWing[n+1,2]-RWing[n,2])**2)))
		
			
				else:
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
	#Create Summary variables

		Number=['']
	
		Body_Angle_DS=['Body_Angle']
		Body_Angle_YZ_DS=['Body_Angle_YZ']

		SA_Right_DS=['SA_Right_DS']
		SA_Left_DS=['SA_Left_DS']
	
		R_Amp_SP_DS=['R_Amp_SP_DS']
		L_Amp_SP_DS=['L_Amp_SP_DS']

		R_Wing_Elevation_Amp_DS=['R_Wing_Angle_Avg_DS']
		L_Wing_Elevation_Amp_DS=['L_Wing_Angle_Avg_DS']

		R_Wing_Angle_Avg_Ground_DS=['R_Wing_Angle_Avg_Ground_DS']
		L_Wing_Angle_Avg_Ground_DS=['L_Wing_Angle_Avg_Ground_DS']

		R_Wingtip_Dist_Trav_DS=['R_Wingtip_Dist_Trav_DS']
		L_Wingtip_Dist_Trav_DS=['L_Wingtip_Dist_Trav_DS']



	
		Body_Angle_US=['Body_Angle']
		Body_Angle_YZ_US=['Body_Angle_YZ']

		SA_Right_US=['SA_Right_US']
		SA_Left_US=['SA_Left_US']

		R_Amp_SP_US=['R_Amp_SP_US']
		L_Amp_SP_US=['L_Amp_SP_US']

		R_Wing_Elevation_Amp_US=['R_Wing_Angle_Avg_US']
		L_Wing_Elevation_Amp_US=['L_Wing_Angle_Avg_US']

		R_Wing_Angle_Avg_Ground_US=['R_Wing_Angle_Avg_Ground_US']
		L_Wing_Angle_Avg_Ground_US=['L_Wing_Angle_Avg_Ground_US']
	
		R_Wingtip_Dist_Trav_US=['R_Wingtip_Dist_Trav_US']
		L_Wingtip_Dist_Trav_US=['L_Wingtip_Dist_Trav_US']
	

	

#####################################################################################################################


# Calculations per upstroke/downstroke
				
		for n in range(len(U)-1):		

	
# right wing		
			if n%2==0:
				Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Right'
			else:
				Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Right'

			StrokeAngle((U[n]-1),(U[n+1]-1),1)

		

			Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
			Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
			Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
			Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
			Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
			Output[(U[n]-1):(U[n+1]-1),7] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistanceTraveled



# left wing
			if n%2==0:
				Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Left'
			else:
				Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Left'

			StrokeAngle((U[n]-1),(U[n+1]-1),2)
			


			Output[(U[n]-1):(U[n+1]-1),8]=Output1[(U[n]-1):(U[n+1]-1),0]	#StrokePlaneAngle
			Output[(U[n]-1):(U[n+1]-1),9]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
			Output[(U[n]-1):(U[n+1]-1),10]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
			Output[(U[n]-1):(U[n+1]-1),11]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
			Output[(U[n]-1):(U[n+1]-1),12]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
			Output[(U[n]-1):(U[n+1]-1),13] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistTraveled

			

		#Downstroke

			if n%2==0:
		
				Number.append(str((n/2)+1))
	
				Body_Angle_DS.append(average(Output[(U[n]-1):(U[n+1]-1),0]))
				Body_Angle_YZ_DS.append(average(Output[(U[n]-1):(U[n+1]-1),1]))

				SA_Right_DS.append(Output[U[n]-1,2])
				SA_Left_DS.append(Output[U[n]-1,8])
			
				R_Wing_Angle_Avg_Ground_DS.append(average(Output[(U[n]-1):(U[n+1]-1),4]))
				L_Wing_Angle_Avg_Ground_DS.append(average(Output[(U[n]-1):(U[n+1]-1),10]))

				R_Amp_SP_DS.append((max(Output[(U[n]-1):(U[n+1]-1),5]))-(min(Output[(U[n]-1):(U[n+1]-1),5])))
				L_Amp_SP_DS.append((max(Output[(U[n]-1):(U[n+1]-1),11]))-(min(Output[(U[n]-1):(U[n+1]-1),11])))

			
				R_Wing_Elevation_Amp_DS.append((max(Output[(U[n]-1):(U[n+1]-1),6]))-(min(Output[(U[n]-1):(U[n+1]-1),6])))
				L_Wing_Elevation_Amp_DS.append((max(Output[(U[n]-1):(U[n+1]-1),12]))-(min(Output[(U[n]-1):(U[n+1]-1),12])))

				R_Wingtip_Dist_Trav_DS.append(Output[U[n]-1,7])
				L_Wingtip_Dist_Trav_DS.append(Output[U[n]-1,13])


			
		#Upstroke
	
			else:	

				Body_Angle_US.append(average(Output[(U[n]-1):(U[n+1]-1),0]))
				Body_Angle_YZ_US.append(average(Output[(U[n]-1):(U[n+1]-1),1]))

				SA_Right_US.append(Output[U[n]-1,2])
				SA_Left_US.append(Output[U[n]-1,8])
			
				R_Wing_Angle_Avg_Ground_US.append(average(Output[(U[n]-1):(U[n+1]-1),4]))
				L_Wing_Angle_Avg_Ground_US.append(average(Output[(U[n]-1):(U[n+1]-1),10]))
			
				R_Amp_SP_US.append((max(Output[(U[n]-1):(U[n+1]-1),5]))-(min(Output[(U[n]-1):(U[n+1]-1),5])))
				L_Amp_SP_US.append((max(Output[(U[n]-1):(U[n+1]-1),11]))-(min(Output[(U[n]-1):(U[n+1]-1),11])))

				R_Wing_Elevation_Amp_US.append((max(Output[(U[n]-1):(U[n+1]-1),6]))-(min(Output[(U[n]-1):(U[n+1]-1),6])))
				L_Wing_Elevation_Amp_US.append((max(Output[(U[n]-1):(U[n+1]-1),12]))-(min(Output[(U[n]-1):(U[n+1]-1),12])))

				R_Wingtip_Dist_Trav_US.append(Output[U[n]-1,7])
				L_Wingtip_Dist_Trav_US.append(Output[U[n]-1,13])

#########################################################################################################################


# Calculate New Pronation and Supinations based on the RIGHT and Left wings and export new pronation supination files
		PronationSupinationHeader=['PronationSupinationHeader']
		NewPronationSupinationR=['NewPronationSupinationR']
		NewPronationSupinationR.append(U[0])
		
		NewPronationSupinationL=['NewPronationSupinationL']
		NewPronationSupinationL.append(U[0])
	
		NewPronationSupinationAVG=['NewPronationSupinationAvg']
		NewPronationSupinationAVG.append(U[0])	
	
		PronationSupinationHeader.append('P')
	
		Z=[]
		Z.append(int(U[0]))


		for n in range(len(U)-1):

		
			if n%2==0: 

				NewPronationSupinationR.append(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))
				NewPronationSupinationL.append(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11]) + (U[n]))
				NewPronationSupinationAVG.append(((np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11]) + (U[n])))/2)
				PronationSupinationHeader.append('S')
			
				Z.append(int((np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11]) + (U[n])))/2)

			
			else:
				NewPronationSupinationR.append(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5])+(U[n]))
				NewPronationSupinationL.append(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11])+(U[n]))
				NewPronationSupinationAVG.append(((np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11]) + (U[n])))/2)
				PronationSupinationHeader.append('P')
		
				Z.append(int((np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),11]) + (U[n])))/2)

		U=[]
		U=Z
		print U

	Writer = csv.writer(open(file[:-4]+"_pron_sup_NEW.csv",'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(PronationSupinationHeader[1:])
	Writer.writerow(NewPronationSupinationAVG[1:])

	Writer = csv.writer(open(file[:-4]+"_pron_sup_RL.csv",'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(PronationSupinationHeader[:])
	Writer.writerow(NewPronationSupinationR[:])
	Writer.writerow(NewPronationSupinationL[:])


###########################################################################################################################

	clf()
	plot(LWING[:,0],LWING[:,1],c='b')
	plot(RWING[:,0],RWING[:,1],c='b')
	scatter(HEAD[:,0],HEAD[:,1],c='m')
		
	for n in range(len(U)-1):
		scatter(LWING[U[n],0],LWING[U[n],1],c='r')
		scatter(RWING[U[n],0],RWING[U[n],1],c='r')		

	
	axes().set_aspect('equal', 'datalim')
	grid(True)
	show()	
#	savefig('stroke_endpoints_'+file[:-4]+'.svg')



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
