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


def usage(error=1):
	usage = """\
Version # 0.0 7-23-2010

Usage: %s [DATA_FILTERED_UPSAMPLED,PRO_SUP_UPSAMPLED]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

RShoulder_X, RShoulder_Y, RShoulder_Z, RWing_X, RWing_Y, RWing_Z, LShoulder_X, LShoulder_Y, LShoulder_Z, LWing_X, LWing_Y, LWing_Z, Head_X, Head_Y, Head_Z, Tail_X, Tail_Y, TAIL_Z

Second file should contain 2 rows, with the data starting in the second row. This should be the frame where Pronation and Supination start. It MUST start with a Pronation and end with a Pronation


Output file: PRONATION_SUPINATION_NEW.CSV

Options:
   -h, --help    Print this message

[written by Paolo Segre, 2010]



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


    	Data= zeros(((len(lines)-1),18), Float)



    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]))
	



	temp2= str(lines2[1]).split(',')
	U=[]
	
	for N in range(0,len(temp2)):	
		U.append(int(temp2[N]))		
		

# Make directory for figures
#	os.mkdir("wingbeat_figures")
#	os.mkdir("angle_figures")
#	os.mkdir("wingbeat_timecourse")
#	os.mkdir("wingbeat_timecourse/Wingtip_Distance_SP")
#	os.mkdir("wingbeat_timecourse/Wingtip_Distance_SP/Graphs")
#	os.mkdir("wingbeat_timecourse/PosDev_SP")
#	os.mkdir("wingbeat_timecourse/PosDev_SP/Graphs")
#	os.mkdir("wingbeat_timecourse/PosDev_horizontal")
#	os.mkdir("wingbeat_timecourse/PosDev_horizontal/Graphs")
# Define Output Arrays


	Output1= zeros(((U[len(U)-1]-1),8))
	Output= zeros(((U[len(U)-1]-1),20))



# Read data from input array


	RSHOULDER= zeros(((len(lines)-1),3))
	RWING= zeros(((len(lines)-1),3))
	LSHOULDER= zeros(((len(lines)-1),3))
	LWING= zeros(((len(lines)-1),3))
	HEAD= zeros(((len(lines)-1),3))
	TAIL= zeros(((len(lines)-1),3))
	

	RSHOULDER[:,0:3]=Data[:,0:3]
	RWING[:,0:3]=Data[:,3:6]
	LSHOULDER[:,0:3]=Data[:,6:9]
	LWING[:,0:3]=Data[:,9:12]
	HEAD[:,0:3]=Data[:,12:15]
	TAIL[:,0:3]=Data[:,15:18]	


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
	

	for n in range((len(U)-1)/2):

		n=n*2
	 	A = ((U[n]-1))
		B = (U[n+2]-1)
		C = (U[n+1]-1)
		Midpoint_Start = (RWing1[A]+LWing1[A])/2
		Midpoint_Start[2]=0

		Midpoint_End = (RWing1[C]+LWing1[C])/2
		Midpoint_End[2] = 0


		Midpoint = (Midpoint_End-Midpoint_Start)

		LengthMidpoint= sqrt(Midpoint[0]**2 + Midpoint[1]**2)

		Xaxis=(-1,0,0)
		

# Calculate rotation angle between Midpoint and Xaxis vector. Create adjustment factor for acos: if Y is positive, subtract angle from 360 degrees to find rotation angle

		if Midpoint[1]<0:
			ZRotationAngle= radians(180)+ acos(((dot(Midpoint,Xaxis))/(LengthMidpoint)))
		
		else: 
			ZRotationAngle=radians(180)+radians(360)-acos(((dot(Midpoint,Xaxis))/(LengthMidpoint)))		

	

#	Create rotation matrix, and multiply times Body1 and RShoulder1 vectors

		RotZ = array(((cos(ZRotationAngle),sin(ZRotationAngle),0),(-sin(ZRotationAngle),cos(ZRotationAngle),0),(0,0,1)))
		
		RShoulder2=matrixmultiply(RotZ,transpose(RShoulder1[A:B,:]))
		RWing2=matrixmultiply(RotZ,transpose(RWing1[A:B,:]))
		LShoulder2=matrixmultiply(RotZ,transpose(LShoulder1[A:B,:]))
		LWing2=matrixmultiply(RotZ,transpose(LWing1[A:B,:]))
		Head2=matrixmultiply(RotZ,transpose(Head1[A:B,:]))
		Tail2=matrixmultiply(RotZ,transpose(Tail1[A:B,:]))

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




# Calculate Angular Velocity from Rotation Angles

		


	Rotation_Angle = ['Rotation_Angle']
	Time_Wingbeat = ['Time_Wingbeat']

	Angular_Velocity_DS = ['Angular_Velocity_DS']
	Angular_Velocity_US = ['Angular_Velocity_US']
	
	Rotation_Angle_DS = ['Rotation_Angle_DS']
	Rotation_Angle_US =['Rotation_Angle_US']
	
	Time_DS =['Time_DS']
	Time_US	=['Time_US']




	# Rotation angle for upstroke/downstroke


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
			ZRotationAngle2= radians(360)-acos(((dot(Mid,Xaxis))/(LengthMid)))
		
		else: 
			ZRotationAngle2= acos(((dot(Mid,Xaxis))/(LengthMid)))


		Rotation_Angle.append(360-(degrees(ZRotationAngle2)))
		Time_Wingbeat.append(B-A)
		


	
	for n in range(1,(len(Rotation_Angle)-1)):
		if n%2==1:
		
			if (Rotation_Angle[n+1]-Rotation_Angle[n])<-180:			
				Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n]+360)
				Angular_Velocity_DS.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n]+360)/(Time_Wingbeat[n]))

			elif (Rotation_Angle[n+1]-Rotation_Angle[n])>180:
				Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n]-360)
				Angular_Velocity_DS.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n]-360)/(Time_Wingbeat[n]))

			else:
				Rotation_Angle_DS.append(Rotation_Angle[n+1]-Rotation_Angle[n])
				Angular_Velocity_DS.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n])/(Time_Wingbeat[n]))



	 	else:	

			if (Rotation_Angle[n+1]-Rotation_Angle[n])<-180:			
				Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n]+360)
				Angular_Velocity_US.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n]+360)/(Time_Wingbeat[n]))
			elif (Rotation_Angle[n+1]-Rotation_Angle[n])>180:
				Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n]-360)
				Angular_Velocity_US.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n]-360)/(Time_Wingbeat[n]))
			else:
				Rotation_Angle_US.append(Rotation_Angle[n+1]-Rotation_Angle[n])	
				Angular_Velocity_US.append(1000*(Rotation_Angle[n+1]-Rotation_Angle[n])/(Time_Wingbeat[n]))			
		
			

	for n in range(1,(len(Time_Wingbeat))):
		if n%2==1:
			Time_DS.append(Time_Wingbeat[n])
		
		else:
			Time_US.append(Time_Wingbeat[n])
	
		

# Fit Reduced Major Axis Regression line to Head, Body(Avg:RShoulder, LShoulder), and Tail in XZ


	Body= ((RShoulder+LShoulder)/2)
	J=vstack((Head,Body,Tail))

	correlation_coefficient = corrcoef([J[:,0],J[:,2]])

	if correlation_coefficient[0,1]<0:
		sign=-1
	else:
		sign=1


	Mean1= mean(J[:,0])

	Std1= std(J[:,0])

	Mean2=mean(J[:,2])
	Std2=std(J[:,2])

	A= sign*Std2/Std1
	B= Mean2-(A*Mean1)

	x=array((-100,0,100))	
	z=(A*x)+B
	z2=(A*x)


#	Angle to Vertical

	Zaxis=array((0,0,1))
	
	BodyXZ=(x[2],0,z2[2])

	LengthBodyXZ=sqrt((BodyXZ[0]**2)+(BodyXZ[2]**2))

	if BodyXZ[0]>0:	
		BodyAngleXZ= acos((dot(BodyXZ,Zaxis))/(LengthBodyXZ))
	
	else:
		BodyAngleXZ= -acos((dot(BodyXZ,Zaxis))/(LengthBodyXZ))





# Fit Reduced Major Axis Regression line to Head, Body(Avg:RShoulder, LShoulder), and Tail in YZ



	correlation_coefficient = corrcoef([J[:,1],J[:,2]])

	if correlation_coefficient[0,1]<0:
		sign=-1
	else:
		sign=1


	Mean1= mean(J[:,1])

	Std1= std(J[:,1])

	Mean2=mean(J[:,2])
	Std2=std(J[:,2])

	A= sign*Std2/Std1
	B= Mean2-(A*Mean1)
	
	w=(A*x)+B
	w2=(A*x)


#	Angle to Vertical


	Zaxis=array((0,0,1))
	
	BodyYZ=(0,x[2],w2[2])

	LengthBodyYZ=sqrt((BodyYZ[1]**2)+(BodyYZ[2]**2))

	if BodyYZ[1]>0:	
		BodyAngleYZ= acos((dot(BodyYZ,Zaxis))/(LengthBodyYZ))-radians(180)
	
	else:
		BodyAngleYZ= radians(180)-acos((dot(BodyYZ,Zaxis))/(LengthBodyYZ))

	Output[:,0]=(degrees(BodyAngleXZ))
	Output[:,1]=(degrees(BodyAngleYZ))



#Body Angle calculation completed	



# plot all points 


	clf()
	plot(x,z)
	scatter(LWing[:,0],LWing[:,2],c='r')
	scatter(LShoulder[:,0],LShoulder[:,2],c='y')
	scatter(RWing[:,0],RWing[:,2],c='g')
	scatter(RShoulder[:,0],RShoulder[:,2],c='b')
	scatter(Head[:,0],Head[:,2],c='k')
	scatter(Tail[:,0],Tail[:,2],c='c')	
	axis((-60,40,0,100))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
#	savefig('XZ_global_'+file[:-4]+'.svg')


	clf()
	plot(x,w)
	scatter(LWing[:,1],LWing[:,2],c='r')
	scatter(LShoulder[:,1],LShoulder[:,2],c='y')
	scatter(RWing[:,1],RWing[:,2],c='g')
	scatter(RShoulder[:,1],RShoulder[:,2],c='b')
	scatter(Head[:,1],Head[:,2],c='k')
	scatter(Tail[:,1],Tail[:,2],c='c')
	axis((-75,75,0,100))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
#	savefig('YZ_global_'+file[:-4]+'.svg')

	clf()
	scatter(LWing[:,0],LWing[:,1],c='r')
	scatter(LShoulder[:,0],LShoulder[:,1],c='y')
	scatter(RWing[:,0],RWing[:,1],c='g')
	scatter(RShoulder[:,0],RShoulder[:,1],c='b')
	scatter(Head[:,0],Head[:,1],c='k')
	scatter(Tail[:,0],Tail[:,1],c='c')
	axis((-70,50,-75,75))
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
#	savefig('XY_global_'+file[:-4]+'.svg')


#	Write Transformed Coordinates
#	Writer = csv.writer(open("trans_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(['RShoulder_X','RShoulder_Y','RShoulder_Z','RWing_X','RWing_Y','RWing_Z','LShoulder_X','LShoulder_Y','LShoulder_Z','LWing_X', 'LWing_Y','LWing_Z','Head_X','Head_Y','Head_Z','Tail_X','Tail_Y','Tail_Z'])
#	for N in range(0,U[len(U)-1]-1):
#		Writer.writerow(Transformed[N])











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


		RShoulder2=transpose(matrixmultiply(RotStrokeAngle,transpose(RShoulder)))
		RWing2=transpose(matrixmultiply(RotStrokeAngle,transpose(RWing)))
		LShoulder2=transpose(matrixmultiply(RotStrokeAngle,transpose(LShoulder)))
		LWing2=transpose(matrixmultiply(RotStrokeAngle,transpose(LWing)))
		Head2=transpose(matrixmultiply(RotStrokeAngle,transpose(Head)))
		Tail2=transpose(matrixmultiply(RotStrokeAngle,transpose(Tail)))



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
		






				

# Plot per wingbeat XZ graphs 
		
		figure(1)
		clf()
		plot(x,y)
		plot(x,z)
			
		if T==2:
			scatter(LWing[R:S,0],LWing[R:S,2],c='r')
			scatter(LShoulder[R:S,0],LShoulder[R:S,2],c='c')
			

		elif T==1:
			scatter(RWing[R:S,0],RWing[R:S,2],c='g')
			scatter(RShoulder[R:S,0],RShoulder[R:S,2],c='c')


		axis((-75,50,0,100))		
		axes().set_aspect('equal', 'datalim')
		grid(True)
#		show()
#		savefig("wingbeat_figures/"+Q+".svg")



# Wingtip distance traveled and velocity

		Wingtip_Velocity=0

		for n in range(R,S-1):
			if T==1:
				
				Wingtip_Velocity=Wingtip_Velocity+(sqrt(((RWing[n+1,0]-RWing[n,0])**2)+((RWing[n+1,1]-RWing[n,1])**2)+((RWing[n+1,2]-RWing[n,2])**2)))
		
			
			else:
				Wingtip_Velocity=Wingtip_Velocity+(sqrt(((LWing[n+1,0]-LWing[n,0])**2)+((LWing[n+1,1]-LWing[n,1])**2)+((LWing[n+1,2]-LWing[n,2])**2)))
	
				

#	Write to output arrays
		Output1[:,0]=(degrees(StrokePlaneAngle))
		Output1[:,1]=(Deviation)
		Output1[:,2]=(ShoulderDist)
		Output1[:,3]=(degrees(Position))
		Output1[:,4]=(degrees(WingAngle))
		Output1[:,5]=(degrees(Position_Ground))
		Output1[:,6]=(degrees(WingAngle_Ground))
		Output1[:,7]=(Wingtip_Velocity)
	
	
#Call programs
	#Create Summary variables

	Number=['']
	
	Body_Angle=['Body_Angle']
	Body_Angle_YZ=['Body_Angle_YZ']

	SA_Right_DS=['SA_Right_DS']
	SA_Left_DS=['SA_Left_DS']
	SA_Right_Body_DS=['SA_Body_Right_DS']
	SA_Left_Body_DS=['SA_Body_Left_DS']
	R_Wingtip_Distance_SP_Max_DS=['R_Wingtip_Distance_SP_Max_DS']
	R_Wingtip_Distance_SP_Min_DS=['R_Wingtip_Distance_SP_Min_DS']
	R_Wingtip_Distance_SP_AbsValue_DS=['R_Wingtip_Distance_SP_AbsValue_DS']
	L_Wingtip_Distance_SP_Max_DS=['L_Wingtip_Distance_SP_Max_DS']
	L_Wingtip_Distance_SP_Min_DS=['L_Wingtip_Distance_SP_Min_DS']
	L_Wingtip_Distance_SP_AbsValue_DS=['L_Wingtip_Distance_SP_AbsValue_DS']
	R_Shoulder_Distance_Avg_DS=['R_Shoulder_Distance_Avg_DS']
	L_Shoulder_Distance_Avg_DS=['L_Shoulder_Distance_Avg_DS']
	R_Amp_SP_DS=['R_Amp_SP_DS']
	L_Amp_SP_DS=['L_Amp_SP_DS']
	R_Wing_Angle_Avg_DS=['R_Wing_Angle_Avg_DS']
	L_Wing_Angle_Avg_DS=['L_Wing_Angle_Avg_DS']
	R_Wing_Angle_Avg_Ground_DS=['R_Wing_Angle_Avg_Ground_DS']
	L_Wing_Angle_Avg_Ground_DS=['L_Wing_Angle_Avg_Ground_DS']
	R_Wingtip_Dist_Trav_DS=['R_Wingtip_Dist_Trav_DS']
	L_Wingtip_Dist_Trav_DS=['L_Wingtip_Dist_Trav_DS']
	

	SA_Right_US=['SA_Right_US']
	SA_Left_US=['SA_Left_US']
	SA_Right_Body_US=['SA_Body_Right_US']
	SA_Left_Body_US=['SA_Body_Left_US']
	R_Wingtip_Distance_SP_Max_US=['R_Wingtip_Distance_SP_Max_US']
	R_Wingtip_Distance_SP_Min_US=['R_Wingtip_Distance_SP_Min_US']
	R_Wingtip_Distance_SP_AbsValue_US=['R_Wingtip_Distance_SP_AbsValue_US']
	L_Wingtip_Distance_SP_Max_US=['L_Wingtip_Distance_SP_Max_US']
	L_Wingtip_Distance_SP_Min_US=['L_Wingtip_Distance_SP_Min_US']
	L_Wingtip_Distance_SP_AbsValue_US=['L_Wingtip_Distance_SP_AbsValue_US']
	R_Shoulder_Distance_Avg_US=['R_Shoulder_Distance_Avg_US']
	L_Shoulder_Distance_Avg_US=['L_Shoulder_Distance_Avg_US']
	R_Amp_SP_US=['R_Amp_SP_US']
	L_Amp_SP_US=['L_Amp_SP_US']
	R_Wing_Angle_Avg_US=['R_Wing_Angle_Avg_US']
	L_Wing_Angle_Avg_US=['L_Wing_Angle_Avg_US']
	R_Wing_Angle_Avg_Ground_US=['R_Wing_Angle_Avg_Ground_US']
	L_Wing_Angle_Avg_Ground_US=['L_Wing_Angle_Avg_Ground_US']
	R_Wingtip_Dist_Trav_US=['R_Wingtip_Dist_Trav_US']
	L_Wingtip_Dist_Trav_US=['L_Wingtip_Dist_Trav_US']
	




# Calculations per upstroke/downstroke
				
	for n in range(len(U)-1):		

	
# right wing		
		if n%2==0:
			Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Right'
		else:
			Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Right'

		StrokeAngle((U[n]-1),(U[n+1]-1),1)

		

		Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
		Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#WingtipDistance
		Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#ShoulderDistance
		Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
		Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
		Output[(U[n]-1):(U[n+1]-1),7]=Output1[(U[n]-1):(U[n+1]-1),5]	#PositionGround
		Output[(U[n]-1):(U[n+1]-1),8]=Output1[(U[n]-1):(U[n+1]-1),6]	#WingAngleGround
#		#Amplitude = Output[:9]
		Output[(U[n]-1):(U[n+1]-1),10] = Output1[(U[n]-1):(U[n+1]-1),7]	#WingtipDistanceTraveled



# left wing
		if n%2==0:
			Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Left'
		else:
			Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Left'

		StrokeAngle((U[n]-1),(U[n+1]-1),2)
			


		Output[(U[n]-1):(U[n+1]-1),11]=Output1[(U[n]-1):(U[n+1]-1),0]	#StrokePlaneAngle
		Output[(U[n]-1):(U[n+1]-1),12]=Output1[(U[n]-1):(U[n+1]-1),1]	#WingtipDistance
		Output[(U[n]-1):(U[n+1]-1),13]=Output1[(U[n]-1):(U[n+1]-1),2]	#ShoulderDistance
		Output[(U[n]-1):(U[n+1]-1),14]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
		Output[(U[n]-1):(U[n+1]-1),15]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
		Output[(U[n]-1):(U[n+1]-1),16]=Output1[(U[n]-1):(U[n+1]-1),5]	#PositionGround
		Output[(U[n]-1):(U[n+1]-1),17]=Output1[(U[n]-1):(U[n+1]-1),6]	#WingAngleGround
#		#Amplitude = Output[:9]
		Output[(U[n]-1):(U[n+1]-1),19] = Output1[(U[n]-1):(U[n+1]-1),7]	#WingtipDistTraveled

			

		#Downstroke

		if n%2==0:
			Number.append(str((n/2)+1))
			Body_Angle.append(Output[U[n]-1,0])
			Body_Angle_YZ.append(Output[U[n]-1,1])	
			SA_Right_DS.append(Output[U[n]-1,2])
			SA_Right_Body_DS.append((Output[U[n]-1,0])+90-(Output[U[n]-1,2]))
			SA_Left_DS.append(Output[U[n]-1,11])
			SA_Left_Body_DS.append((Output[U[n]-1,0])+90-(Output[U[n]-1,11]))
			R_Wingtip_Distance_SP_Max_DS.append(max(Output[(U[n]-1):(U[n+1]-1),3]))		
			R_Wingtip_Distance_SP_Min_DS.append(min(Output[(U[n]-1):(U[n+1]-1),3]))
			R_Wingtip_Distance_SP_AbsValue_DS.append((max(Output[(U[n]-1):(U[n+1]-1),3]))-(min(Output[(U[n]-1):(U[n+1]-1),3])))
			L_Wingtip_Distance_SP_Max_DS.append(max(Output[(U[n]-1):(U[n+1]-1),12]))
			L_Wingtip_Distance_SP_Min_DS.append(min(Output[(U[n]-1):(U[n+1]-1),12]))
			L_Wingtip_Distance_SP_AbsValue_DS.append((max(Output[(U[n]-1):(U[n+1]-1),12]))-(min(Output[(U[n]-1):(U[n+1]-1),12])))
			R_Shoulder_Distance_Avg_DS.append(average(Output[(U[n]-1):(U[n+1]-1),4]))
			L_Shoulder_Distance_Avg_DS.append(average(Output[(U[n]-1):(U[n+1]-1),13]))
			R_Wing_Angle_Avg_DS.append(average(Output[(U[n]-1):(U[n+1]-1),6]))
			L_Wing_Angle_Avg_DS.append(average(Output[(U[n]-1):(U[n+1]-1),15]))
			R_Wing_Angle_Avg_Ground_DS.append(average(Output[(U[n]-1):(U[n+1]-1),8]))
			L_Wing_Angle_Avg_Ground_DS.append(average(Output[(U[n]-1):(U[n+1]-1),17]))
			R_Wingtip_Dist_Trav_DS.append(Output[U[n]-1,10])
			L_Wingtip_Dist_Trav_DS.append(Output[U[n]-1,19])
			
		#Upstroke
	
		else:	
			SA_Right_US.append(Output[U[n]-1,2])
			SA_Right_Body_US.append((Output[U[n]-1,0])+90-(Output[U[n]-1,2]))
			SA_Left_US.append(Output[U[n]-1,11])
			SA_Left_Body_US.append((Output[U[n]-1,0])+90-(Output[U[n]-1,11]))
			R_Wingtip_Distance_SP_Max_US.append(max(Output[(U[n]-1):(U[n+1]-1),3]))		
			R_Wingtip_Distance_SP_Min_US.append(min(Output[(U[n]-1):(U[n+1]-1),3]))
			R_Wingtip_Distance_SP_AbsValue_US.append((max(Output[(U[n]-1):(U[n+1]-1),3]))-(min(Output[(U[n]-1):(U[n+1]-1),3])))
			L_Wingtip_Distance_SP_Max_US.append(max(Output[(U[n]-1):(U[n+1]-1),12]))
			L_Wingtip_Distance_SP_Min_US.append(min(Output[(U[n]-1):(U[n+1]-1),12]))
			L_Wingtip_Distance_SP_AbsValue_US.append((max(Output[(U[n]-1):(U[n+1]-1),12]))-(min(Output[(U[n]-1):(U[n+1]-1),12])))
			R_Shoulder_Distance_Avg_US.append(average(Output[(U[n]-1):(U[n+1]-1),4]))
			L_Shoulder_Distance_Avg_US.append(average(Output[(U[n]-1):(U[n+1]-1),13]))
			R_Wing_Angle_Avg_US.append(average(Output[(U[n]-1):(U[n+1]-1),6]))
			L_Wing_Angle_Avg_US.append(average(Output[(U[n]-1):(U[n+1]-1),15]))
			R_Wing_Angle_Avg_Ground_US.append(average(Output[(U[n]-1):(U[n+1]-1),8]))
			L_Wing_Angle_Avg_Ground_US.append(average(Output[(U[n]-1):(U[n+1]-1),17]))
			R_Wingtip_Dist_Trav_US.append(Output[U[n]-1,10])
			L_Wingtip_Dist_Trav_US.append(Output[U[n]-1,19])

#########################################################################################################################


# Calculate New Pronation and Supinations based on the RIGHT wing and export new pronation supination file
	PronationSupinationHeader=['PronationSupinationHeader']
	NewPronationSupinationR=['NewPronationSupinationR']
	NewPronationSupinationR.append(U[0])
	
	NewPronationSupinationL=['NewPronationSupinationL']
	NewPronationSupinationL.append(U[0])

	NewPronationSupinationAVG=['NewPronationSupinationAvg']
	NewPronationSupinationAVG.append(U[0])	

	PronationSupinationHeader.append('P')

	for n in range(len(U)-1):

		
		if n%2==0: 

			NewPronationSupinationR.append(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))
			NewPronationSupinationL.append(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),14]) + (U[n]))
			NewPronationSupinationAVG.append(((np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmax(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),14]) + (U[n])))/2)
			PronationSupinationHeader.append('S')

			
		else:
			NewPronationSupinationR.append(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5])+(U[n]))
			NewPronationSupinationL.append(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),14])+(U[n]))
			NewPronationSupinationAVG.append(((np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),5]) + (U[n]))+(np.argmin(Output[(U[n]-1):(U[n+1]+((U[n+1]-U[n])/2)),14]) + (U[n])))/2)
			PronationSupinationHeader.append('P')


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


	for n in range(len(U)-1):
	
		AmplitudeR= max(Output[(U[n]-1):(U[n+1]),5])-min(Output[(U[n]-1):(U[n+1]),5])
		Output[(U[n]-1):(U[n+1]-1),9]=AmplitudeR
		
		AmplitudeL= max(Output[(U[n]-1):(U[n+1]),14])-min(Output[(U[n]-1):(U[n+1]),14])
		Output[(U[n]-1):(U[n+1]-1),18]=AmplitudeL

		if n%2==0:
			R_Amp_SP_DS.append(Output[U[n]-1,9])
			L_Amp_SP_DS.append(Output[U[n]-1,18])
		else:		
			R_Amp_SP_US.append(Output[U[n]-1,9])
			L_Amp_SP_US.append(Output[U[n]-1,18])


	
############################################################################################################################	

#	Writer = csv.writer(open("Angles_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(['Body_Angle_XZ','Body_Angle_YZ','R_Stroke_Plane_Angle','R_Wingtip_Distance_SP', 'R_Shoulder_Distance', 'R_Wingtip_Position', 'R_Wing_Angle', "R_Position_Horizontal", "R_Wing_Angle_Horizontal", 'R_Amplitude_SP','Wingtip_Distance_traveled','L_Stroke_Plane_Angle','L_Wingtip_Distance_SP', 'L_Shoulder_Distance', 'L_Wingtip_Position','L_Wing_Angle',"L_Position_Horizontal","L_Wing_Angle_Horizontal",'L_Amplitude_SP',"Wingtip_Distance_Traveled"])
#	for N in range(0,U[len(U)-1]-1):
#		Writer.writerow(Output[N])

# store output in array



	Output2 = zeros((len(Body_Angle)-1,57))

	Output2[:,0] = Number[1:]
	Output2[:,1] = Body_Angle[1:]
	Output2[:,2] = Body_Angle_YZ[1:]
	Output2[:,3] = Angular_Velocity_DS[1:]
	Output2[:-1,4] = Angular_Velocity_US[1:]	

	Output2[:,5] = Number[1:]

	Output2[:,6] = SA_Right_DS[1:]
	Output2[:,7] = SA_Right_Body_DS[1:]
	Output2[:,8] = SA_Left_DS[1:]
	Output2[:,9] = SA_Left_Body_DS[1:]
	Output2[:,10] = R_Wingtip_Distance_SP_Max_DS[1:]
	Output2[:,11] = R_Wingtip_Distance_SP_Min_DS[1:]
	Output2[:,12] = R_Wingtip_Distance_SP_AbsValue_DS[1:]
	Output2[:,13]= L_Wingtip_Distance_SP_Max_DS[1:]
	Output2[:,14]= L_Wingtip_Distance_SP_Min_DS[1:]
	Output2[:,15]= L_Wingtip_Distance_SP_AbsValue_DS[1:]
	Output2[:,16]= R_Shoulder_Distance_Avg_DS[1:]
	Output2[:,17]= L_Shoulder_Distance_Avg_DS[1:]
	Output2[:,18]= R_Amp_SP_DS[1:]
	Output2[:,19]= L_Amp_SP_DS[1:]
	Output2[:,20]= R_Wing_Angle_Avg_DS[1:]
	Output2[:,21]= L_Wing_Angle_Avg_DS[1:]
	Output2[:,22]= R_Wing_Angle_Avg_Ground_DS[1:]
	Output2[:,23]= L_Wing_Angle_Avg_Ground_DS[1:]
	Output2[:,24]= R_Wingtip_Dist_Trav_DS[1:]
	Output2[:,25]= L_Wingtip_Dist_Trav_DS[1:]

	Output2[:,26] = Number[1:]

	Output2[:,27] = SA_Right_US[1:]
	Output2[:,28] = SA_Right_Body_US[1:]
	Output2[:,29] = SA_Left_US[1:]
	Output2[:,30] = SA_Left_Body_DS[1:]
	Output2[:,31] = R_Wingtip_Distance_SP_Max_US[1:]
	Output2[:,32] = R_Wingtip_Distance_SP_Min_US[1:]
	Output2[:,33] = R_Wingtip_Distance_SP_AbsValue_US[1:]
	Output2[:,34]= L_Wingtip_Distance_SP_Max_US[1:]
	Output2[:,35]= L_Wingtip_Distance_SP_Min_US[1:]
	Output2[:,36]= L_Wingtip_Distance_SP_AbsValue_US[1:]
	Output2[:,37]= R_Shoulder_Distance_Avg_US[1:]
	Output2[:,38]= L_Shoulder_Distance_Avg_US[1:]
	Output2[:,39]= R_Amp_SP_US[1:]
	Output2[:,40]= L_Amp_SP_US[1:]
	Output2[:,41]= R_Wing_Angle_Avg_US[1:]
	Output2[:,42]= L_Wing_Angle_Avg_US[1:]
	Output2[:,43]= R_Wing_Angle_Avg_Ground_US[1:]
	Output2[:,44]= L_Wing_Angle_Avg_Ground_US[1:]
	Output2[:,45]= R_Wingtip_Dist_Trav_US[1:]
	Output2[:,46]= L_Wingtip_Dist_Trav_US[1:]

	Output2[:,47]=Time_DS[1:]
	Output2[:,48]=Time_US[1:]
	Output2[:,49]=Rotation_Angle_DS[1:]
	Output2[:-1,50]=Rotation_Angle_US[1:]

	Output2[:,51]=(1000*Output2[:,24]/Output2[:,47])
	Output2[:,52]=(1000*Output2[:,25]/Output2[:,47])

	Output2[:,53]=(1000*Output2[:,45]/Output2[:,48])
	Output2[:,54]=(1000*Output2[:,46]/Output2[:,48])

	Output2[:-1,55]=(Output2[:-1,3]+Output2[:-1,4])/2
	Output2[:-1,56]=(Output2[:-1,49]+Output2[:-1,50])

	

#write to file



#	Writer = csv.writer(open("Angles_Summary_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(["Wingbeat#","Body_Angle","Body_Angle_YZ","Angular_Velocity_DS","Angular_Velocity_US","","R_Stroke_Plane_Angle","R_Stroke_Plane_Angle_Body","L_Stroke_Plane_Angle","L_Stroke_Plane_Angle_Body","R_Wingtip_Distance_SP_Max_DS","R_Wingtip_Distance_SP_Min_DS","R_Wingtip_Distance_SP_AbsValue_DS","L_Wingtip_Distance_SP_Max_DS", "L_Wingtip_Distance_SP_Min_DS","L_Wingtip_Distance_SP_AbsValue_DS","R_Shoulder_Distance_Avg_DS","L_Shoulder_Distance_Avg_DS","R_Amp_SP_DS","L_Amp_SP_DS","R_Wing_Angle_Avg_DS","L_Wing_Angle_Avg_DS","R_Wing_Angle_Avg_Ground_DS","L_Wing_Angle_Avg_Ground_DS","R_Wingtip_Dist_Trav_DS","L_Wingtip_Dist_Trav_DS","","R_Stroke_Plane_Angle_US","R_Stroke_Plane_Angle_Body_US","L_Stroke_Plane_Angle_US","L_Stroke_Plane_Angle_Body_US","R_Wingtip_Distance_SP_Max_US","R_Wingtip_Distance_SP_Min_US","R_Wingtip_Distance_SP_AbsValue_US","L_Wingtip_Distance_SP_Max_US", "L_Wingtip_Distance_SP_Min_US","L_Wingtip_Distance_SP_AbsValue_US","R_Shoulder_Distance_Avg_US","L_Shoulder_Distance_Avg_US","R_Amp_SP_US","L_Amp_SP_US","R_Wing_Angle_Avg_US","L_Wing_Angle_Avg_US","R_Wing_Angle_Avg_Ground_US","L_Wing_Angle_Avg_Ground_US","R_Wingtip_Dist_Trav_US","L_Wingtip_Dist_Trav_US","Time_DS","Time_US","Rotation_Angle_DS","Rotation_Angle_US","R_Wingtip_Velocity_DS","L_Wingtip_Velocity_DS","R_Wingtip_Velocity_US","L_Wingtip_Velocity_US","Angular_Velocity_Wingbeat","Rotation_Angle_Wingbeat"])

#	for N in range(len(Body_Angle)-1):
#		Writer.writerow(Output2[N])









###################################################################################


# Left minus Right

	Output3 = zeros((len(Body_Angle)-1,27))
	Output3[:,0] = Number[1:]
	Output3[:,1] = Body_Angle[1:]
	Output3[:,2] = Body_Angle_YZ[1:]
	Output3[:,3] = Angular_Velocity_DS[1:]
	Output3[:-1,4] = Angular_Velocity_US[1:]
	
	Output3[:,5] = Number[1:]

	Output3[:,6] = Output2[:,8] - Output2[:,6]
	Output3[:,7] = Output2[:,9] - Output2[:,7]
	Output3[:,8] = Output2[:,15] - Output2[:,12]
	Output3[:,9] = Output2[:,17] - Output2[:,16]
	Output3[:,10] = Output2[:,19] - Output2[:,18]
	Output3[:,11] = Output2[:,21] - Output2[:,20]
	Output3[:,12] = Output2[:,23] - Output2[:,22]
	Output3[:,13] = Output2[:,25] - Output2[:,24]

	Output3[:,14] = Number[1:]

	Output3[:,15] = Output2[:,29] - Output2[:,27]
	Output3[:,16] = Output2[:,30] - Output2[:,28]
	Output3[:,17] = Output2[:,36] - Output2[:,33]
	Output3[:,18] = Output2[:,38] - Output2[:,37]
	Output3[:,19] = Output2[:,40] - Output2[:,39]
	Output3[:,20] = Output2[:,42] - Output2[:,41]
	Output3[:,21] = Output2[:,44] - Output2[:,43]
	Output3[:,22] = Output2[:,46] - Output2[:,45]

	Output3[:,23] = Output2[:,52] - Output2[:,51]
	Output3[:,24] = Output2[:,54] - Output2[:,53]

	Output3[:,25] = Output2[:,55]
	Output3[:,26] = Output2[:,56]

	

#	Writer = csv.writer(open("Angles_Summary_LeftMinusRight_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(["Wingbeat#","Body_Angle","Body_Angle_YZ","Angular_Velocity_DS","Angular_Velocity_US","","Stroke_Plane_Angle_DS","Stroke_Plane_Angle_Body_DS","Wingtip_Distance_Abs_DS","Shoulder_Distance_Avg_DS","Amp_SP_DS","Wing_Angle_Avg_DS","Wing_Angle_Avg_Ground_DS","Wingtip_Dist_Trav_DS","","Stroke_Plane_Angle_US","Stroke_Plane_Angle_Body_US","Wingtip_Distance_Abs_US","Shoulder_Distance_Avg_US","Amp_SP_US","Wing_Angle_Avg_US","Wing_Angle_Avg_Ground_US","Wingtip_Dist_Trav_US","Wingtip_Velocity_DS","Wingtip_Velocity_US","Angular_Velocity_Wingbeat","Rotation_Angle_Wingbeat"])


#	for N in range(len(Body_Angle)-1):
#		Writer.writerow(Output3[N])


	
# Graph wingbeat timeseries 
	
	for n in range(3,27):
		clf()
		scatter(Output3[:,0],Output3[:,n],c='r')
		plot(Output3[:,0],Output3[:,n],c='b')		
		grid(True)
		xlim(0,len(Body_Angle))
		if n ==3:
			ylim(-1000,1000)
#			savefig("angle_figures/1_Angular_Velocity_DS_"+file[:-4]+".svg")

		if n ==4:
			clf()
			scatter(Output3[:-1,0],Output3[:-1,n],c='r')
			plot(Output3[:-1,0],Output3[:-1,n],c='b')		
			grid(True)
			xlim(0,len(Body_Angle))
			ylim(-1000,1000)
#			savefig("angle_figures/2_Angular_Velocity_US_"+file[:-4]+".svg")


		if n ==6:
			ylim(-30,30)
#			savefig("angle_figures/3_Stroke_Angle_DS_"+file[:-4]+".svg")

		if n ==7:
			ylim(-30,30)
#			savefig("angle_figures/4_Stroke_Angle_Body_DS_"+file[:-4]+".svg")

		if n ==8:
			ylim(-20,20)
#			savefig("angle_figures/5_Wingtip_Distance_Sp_Abs_DS_"+file[:-4]+".svg")

		if n ==9:
			ylim(-20,20)
#			savefig("angle_figures/6_Shoulder_Distance_Avg_DS_"+file[:-4]+".svg")

		if n ==10:
			ylim(-20,20)
#			savefig("angle_figures/7_Amp_DS_"+file[:-4]+".svg")

		if n ==11:
			ylim(-20,20)
#			savefig("angle_figures/8_Wing_Angle_Avg_DS_"+file[:-4]+".svg")

		if n ==12:
			ylim(-20,20)
#			savefig("angle_figures/9_Wing_Angle__Ground_Avg_DS_"+file[:-4]+".svg")

		if n ==13:
			ylim(-20,20)
#			savefig("angle_figures/10_Wingtip_Distance_Traveled_DS_"+file[:-4]+".svg")
		

		if n ==15:
			ylim(-30,30)
#			savefig("angle_figures/11_Stroke_Angle_US_"+file[:-4]+".svg")

		if n ==16:
			ylim(-30,30)
			#savefig("angle_figures/12_Stroke_Angle_Body_US_"+file[:-4]+".svg")

		if n ==17:
			ylim(-20,20)
			#savefig("angle_figures/13_Wingtip_Distance_Sp_Abs_US_"+file[:-4]+".svg")

		if n ==18:
			ylim(-20,20)
			#savefig("angle_figures/15_Shoulder_Distance_Avg_US_"+file[:-4]+".svg")

		if n ==19:
			ylim(-20,20)
			#savefig("angle_figures/16_Amp_US_"+file[:-4]+".svg")

		if n ==20:
			ylim(-20,20)
			#savefig("angle_figures/17_Wing_Angle_Avg_US_"+file[:-4]+".svg")

		if n ==21:
			ylim(-20,20)
			#savefig("angle_figures/18_Wing_Angle__Ground_Avg_US_"+file[:-4]+".svg")

		if n ==22:
			ylim(-20,20)
			#savefig("angle_figures/19_Wingtip_Distance_Traveled_US_"+file[:-4]+".svg")

		if n ==23:
			ylim(-1000,1000)
			#savefig("angle_figures/14_Wingtip_Velocity_DS_"+file[:-4]+".svg")

		if n ==24:
			ylim(-1000,1000)
			#savefig("angle_figures/20_Wingtip_Velocity_US_"+file[:-4]+".svg")

		if n ==25:
			clf()
			scatter(Output3[:-1,0],Output3[:-1,n],c='r')
			plot(Output3[:-1,0],Output3[:-1,n],c='b')		
			grid(True)
			xlim(0,len(Body_Angle))
			ylim(-1000,1000)
			#savefig("angle_figures/21_Angular_Velocity_Wingbeat_"+file[:-4]+".svg")

		if n ==26:
			clf()
			scatter(Output3[:-1,0],Output3[:-1,n],c='r')
			plot(Output3[:-1,0],Output3[:-1,n],c='b')		
			grid(True)
			xlim(0,len(Body_Angle))
			ylim(-25,25)
			#savefig("angle_figures/22_Rotation_Angle_Wingbeat_"+file[:-4]+".svg")

		

###################################################################################################		


	

# Per Wingbeat Calculations
	clf()
	def PerWingbeat(O,P,Q,R):

		b=Output[(O):(P),(Q)]
		a=range(1,len(b)+1)		

		c= interpolate.splrep(a,b)
		d= linspace(1,(len(b)+1),num=100)
		
		
		R[:,0] = linspace(1,25,num=100)		
		R[:,((n/2)+3)] = interpolate.splev(d,c)



# Wingtip Distance from Stroke Plane

	e= zeros((100,((len(U)-1)/2)+3))		
	f= zeros((100,((len(U)-1)/2)+3))
	
	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),3,e)
	RDistance_SP=e


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),12,f)
	LDistance_SP=f


#	Calculate Averages and StDevs and #save as columns 2 and 3

	for n in range(0,100):
		
		RDistance_SP[n,1]=average(RDistance_SP[n,3:])
		RDistance_SP[n,2]=std(RDistance_SP[n,3:])
		LDistance_SP[n,1]=average(LDistance_SP[n,3:])
		LDistance_SP[n,2]=std(LDistance_SP[n,3:])

# 	graph		

	clf()
	scatter(RDistance_SP[:,0],RDistance_SP[:,1],c='g')
	scatter(LDistance_SP[:,0],LDistance_SP[:,1],c='r')
	axis((1,25,-15,15))
	#savefig('wingbeat_timecourse/Wingtip_Distance_SP/LR_Wingtip_Distance_SP_'+file[:-4])
#	show()

	
#	graph individual wingbeats

	for n in range(3,len(RDistance_SP[1,:])):	
		clf()
		scatter(RDistance_SP[:,0],RDistance_SP[:,n],c='g')
		scatter(LDistance_SP[:,0],LDistance_SP[:,n],c='r')
		axis((1,25,-15,15))
		#savefig('wingbeat_timecourse/Wingtip_Distance_SP/Graphs/LRWingtip_Distance_SP_'+str(n-2)+"_"+file[:-4])
		


#	Write Output

	header = ['Time','Average','StDev']
	for n in range(3,len(RDistance_SP[1,:])):
		header.append(n-2)

#	Writer = csv.writer(open("wingbeat_timecourse/Wingtip_Distance_SP/R_Wingtip_Distance_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(RDistance_SP[N])


#	Writer = csv.writer(open("wingbeat_timecourse/Wingtip_Distance_SP/L_Wingtip_Distance_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(LDistance_SP[N])



# Position and Deviation from Stroke Plane

	g= zeros((100,((len(U)-1)/2)+3))		
	h= zeros((100,((len(U)-1)/2)+3))
	i= zeros((100,((len(U)-1)/2)+3))		
	j= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),5,g)
	RPosition_SP=g


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),6,h)
	RDeviation_SP=h


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),14,i)
	LPosition_SP=i


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),15,j)
	LDeviation_SP=j


#	Calculate Averages and StDevs and #save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_SP[n,1]=average(RPosition_SP[n,3:])
		RDeviation_SP[n,1]=average(RDeviation_SP[n,3:])
		RPosition_SP[n,2]=std(RPosition_SP[n,3:])
		RDeviation_SP[n,2]=std(RDeviation_SP[n,3:])

		LPosition_SP[n,1]=average(LPosition_SP[n,3:])
		LDeviation_SP[n,1]=average(LDeviation_SP[n,3:])
		LPosition_SP[n,2]=std(LPosition_SP[n,3:])
		LDeviation_SP[n,2]=std(LDeviation_SP[n,3:])


# 	graph		

	clf()
	scatter(RDeviation_SP[:,0],RDeviation_SP[:,1],c='g')
	scatter(LDeviation_SP[:,0],LDeviation_SP[:,1],c='r')
	axis((1,25,-45,45))
	#savefig('wingbeat_timecourse/PosDev_SP/LRDeviation_SP_'+file[:-4])
#	show()

	clf()
	scatter(RPosition_SP[:,0],RPosition_SP[:,1],c='g')
	scatter(LPosition_SP[:,0],LPosition_SP[:,1],c='r')
	axis((1,25,-10,190))
	#savefig('wingbeat_timecourse/PosDev_SP/LRPosition_SP_'+file[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(RDeviation_SP[1,:])):	
		clf()
		scatter(RDeviation_SP[:,0],RDeviation_SP[:,n],c='g')
		scatter(LDeviation_SP[:,0],LDeviation_SP[:,n],c='r')
		axis((1,25,-45,45))
		#savefig('wingbeat_timecourse/PosDev_SP/Graphs/LRDeviation_SP_'+str(n-2)+"_"+file[:-4])

		clf()
		scatter(RPosition_SP[:,0],RPosition_SP[:,n],c='g')
		scatter(LPosition_SP[:,0],LPosition_SP[:,n],c='r')
		axis((1,25,-10,190))
		#savefig('wingbeat_timecourse/PosDev_SP/Graphs/LRPosition_SP_'+str(n-2)+"_"+file[:-4])



#	Write Output

#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_SP/RPosition_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(RPosition_SP[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_SP/RDeviation_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(RDeviation_SP[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_SP/LPosition_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(LPosition_SP[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_SP/LDeviation_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(LDeviation_SP[N])



# Position and Deviation from Horizontal

	k= zeros((100,((len(U)-1)/2)+3))		
	l= zeros((100,((len(U)-1)/2)+3))
	m= zeros((100,((len(U)-1)/2)+3))		
	o= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),7,k)
	RPosition_horizontal=k


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),8,l)
	RDeviation_horizontal=l


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),16,m)
	LPosition_horizontal=m


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+2]-1),17,o)
	LDeviation_horizontal=o


#	Calculate Averages and StDevs and #save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_horizontal[n,1]=average(RPosition_horizontal[n,3:])
		RDeviation_horizontal[n,1]=average(RDeviation_horizontal[n,3:])
		RPosition_horizontal[n,2]=std(RPosition_horizontal[n,3:])
		RDeviation_horizontal[n,2]=std(RDeviation_horizontal[n,3:])

		LPosition_horizontal[n,1]=average(LPosition_horizontal[n,3:])
		LDeviation_horizontal[n,1]=average(LDeviation_horizontal[n,3:])
		LPosition_horizontal[n,2]=std(LPosition_horizontal[n,3:])
		LDeviation_horizontal[n,2]=std(LDeviation_horizontal[n,3:])


# 	graph		

	clf()
	scatter(RDeviation_horizontal[:,0],RDeviation_horizontal[:,1],c='g')
	scatter(LDeviation_horizontal[:,0],LDeviation_horizontal[:,1],c='r')
	axis((1,25,-45,45))
	#savefig('wingbeat_timecourse/PosDev_horizontal/LRDeviation_horizontal_'+file[:-4])
#	show()

	clf()
	scatter(RPosition_horizontal[:,0],RPosition_horizontal[:,1],c='g')
	scatter(LPosition_horizontal[:,0],LPosition_horizontal[:,1],c='r')
	axis((1,25,-10,190))
	#savefig('wingbeat_timecourse/PosDev_horizontal/LRPosition_horizontal_'+file[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(RDeviation_SP[1,:])):	
		clf()
		scatter(RDeviation_horizontal[:,0],RDeviation_horizontal[:,n],c='g')
		scatter(LDeviation_horizontal[:,0],LDeviation_horizontal[:,n],c='r')
		axis((1,25,-45,45))
		#savefig('wingbeat_timecourse/PosDev_horizontal/Graphs/LRDeviation_horizontal_'+str(n-2)+"_"+file[:-4])

		clf()
		scatter(RPosition_horizontal[:,0],RPosition_horizontal[:,n],c='g')
		scatter(LPosition_horizontal[:,0],LPosition_horizontal[:,n],c='r')
		axis((1,25,-10,190))
		#savefig('wingbeat_timecourse/PosDev_horizontal/Graphs/LRPosition_horizontal_'+str(n-2)+"_"+file[:-4])



#	Write Output

#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_horizontal/RPosition_horizontal_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(RPosition_horizontal[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_horizontal/RDeviation_horizontal_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(RDeviation_horizontal[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_horizontal/LPosition_horizontal_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(LPosition_horizontal[N])


#	Writer = csv.writer(open("wingbeat_timecourse/PosDev_horizontal/LDeviation_horizontal_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#	Writer.writerow(header)
#	for N in range(0,100):
#		Writer.writerow(LDeviation_horizontal[N])





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
