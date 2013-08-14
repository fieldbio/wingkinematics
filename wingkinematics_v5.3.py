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
Version # 5.1 5-23-2011

Usage: %s [INPUT_FILE_NAME]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

RShoulder_X, RShoulder_Y, RShoulder_Z, RWing_X, RWing_Y, RWing_Z, LShoulder_X, LShoulder_Y, LShoulder_Z, LWing_X, LWing_Y, LWing_Z, Head_X, Head_Y, Head_Z, Tail_X, Tail_Y, TAIL_Z

Second file should contain 2 rows, with the data starting in the second row. This should be the frame where Pronation and Supination start. It MUST start with a Pronation and end with a Pronation

---note: Change FrameMult (line 847) to convert wingtip velocity from mm/frame to whatever you want (e.g.: 10 = [1000fps*10 upsampled frames]/[1000mm/m])
	

Output file: trans_[INPUT_FILE_NAME].CSV

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
	seterr(all='ignore')
	(path, filename) = os.path.split(file)

# input files

	inFile = open(file,"r")
    	lines = inFile.readlines()	

	inFile2 = open(time,"r")
	lines2 = inFile2.readlines()	


    	Data= zeros(((len(lines)-1),18), float)



    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]))
	


	temp2= str(lines2[1]).split(',')
	U=[]
	
	for N in range(0,len(temp2)):	
		U.append(int(temp2[N]))		
		

# Make directory for figures
	os.system("mkdir %s"%(path+"/wingbeat_figures"))
	os.system("mkdir %s"%(path+"/angle_figures"))
	os.system("mkdir %s"%(path+"/wingbeat_timecourse"))
	os.system("mkdir %s"%(path+"/wingbeat_timecourse/PosElev_SP"))
	os.system("mkdir %s"%(path+"/wingbeat_timecourse/PosElev_SP/Graphs"))
	os.system("mkdir %s"%(path+"/wingbeat_timecourse/PosElev_GR"))
	os.system("mkdir %s"%(path+"/wingbeat_timecourse/PosElev_GR/Graphs"))
	os.system("mkdir %s"%(path+"/average_graphs"))
# Define Output Arrays


	Output1= zeros(((U[len(U)-1]-1),6))
	Output= zeros(((U[len(U)-1]-1),14))



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


	Avg_Rot = average(Rotation_Angle[1:])	
	x = [-100,0,100]
	y = [-100*tan(radians(Avg_Rot)),0,100*tan(radians(Avg_Rot))]


	for n in range(1,(len(Rotation_Angle))):
		if n%2==1:

			Rotation_Angle_DS.append(90-Rotation_Angle[n])
		
	 	else:	

			Rotation_Angle_US.append(90-Rotation_Angle[n])		
				

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


###########################################################

#plot global XY

	clf()
	plot(LWING[:,0],LWING[:,1],c='r')
	plot(LSHOULDER[:,0],LSHOULDER[:,1],c='y')
	plot(RWING[:,0],RWING[:,1],c='b')
	plot(RSHOULDER[:,0],RSHOULDER[:,1],c='g')
	plot(HEAD[:,0],HEAD[:,1],c='m')
	plot(TAIL[:,0],TAIL[:,1],c='c')
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/true_global_XY_'+filename[:-4]+'.svg')

###########################################################

# plot all points 


	clf()
	plot(LWing[U[0]:U[-1],0],LWing[U[0]:U[-1],2],c='r')
	plot(LShoulder[U[0]:U[-1],0],LShoulder[U[0]:U[-1],2],c='y')
	plot(RWing[U[0]:U[-1],0],RWing[U[0]:U[-1],2],c='b')
	plot(RShoulder[U[0]:U[-1],0],RShoulder[U[0]:U[-1],2],c='g')
	plot(Head[U[0]:U[-1],0],Head[U[0]:U[-1],2],c='m')
	plot(Tail[U[0]:U[-1],0],Tail[U[0]:U[-1],2],c='c')	
	axis((-85,65,0,150))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/XZ_global_'+filename[:-4]+'.svg')


	clf()
	plot(LWing[U[0]:U[-1],1],LWing[U[0]:U[-1],2],c='r')
	plot(LShoulder[U[0]:U[-1],1],LShoulder[U[0]:U[-1],2],c='y')
	plot(RWing[U[0]:U[-1],1],RWing[U[0]:U[-1],2],c='b')
	plot(RShoulder[U[0]:U[-1],1],RShoulder[U[0]:U[-1],2],c='g')
	plot(Head[U[0]:U[-1],1],Head[U[0]:U[-1],2],c='m')
	plot(Tail[U[0]:U[-1],1],Tail[U[0]:U[-1],2],c='c')
	axis((-75,75,0,150))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/YZ_global_'+filename[:-4]+'.svg')

	clf()
	plot(LWing[U[0]:U[-1],0],LWing[U[0]:U[-1],1],c='r')
	plot(LShoulder[U[0]:U[-1],0],LShoulder[U[0]:U[-1],1],c='y')
	plot(RWing[U[0]:U[-1],0],RWing[U[0]:U[-1],1],c='b')
	plot(RShoulder[U[0]:U[-1],0],RShoulder[U[0]:U[-1],1],c='g')
	plot(Head[U[0]:U[-1],0],Head[U[0]:U[-1],1],c='m')
	plot(Tail[U[0]:U[-1],0],Tail[U[0]:U[-1],1],c='c')
	plot(x,y)
	
	axis((-85,65,-75,75))
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/XY_global_'+filename[:-4]+'.svg')


#	Write Transformed Coordinates
	Writer = csv.writer(open(path+"/trans_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['RShoulder_X','RShoulder_Y','RShoulder_Z','RWing_X','RWing_Y','RWing_Z','LShoulder_X','LShoulder_Y','LShoulder_Z','LWing_X', 'LWing_Y','LWing_Z','Head_X','Head_Y','Head_Z','Tail_X','Tail_Y','Tail_Z'])
	for N in range(0,U[len(U)-1]-1):
		Writer.writerow(Transformed[N])





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




				

# Plot per wingbeat XZ graphs 
		
		figure(1)
		clf()
		plot(x,y, c='g')
			
		if T==2:
			scatter(LWing[R:S,0],LWing[R:S,2],c='r')
			scatter(LShoulder[R:S,0],LShoulder[R:S,2],c='y')
			

		elif T==1:
			scatter(RWing[R:S,0],RWing[R:S,2],c='b')
			scatter(RShoulder[R:S,0],RShoulder[R:S,2],c='g')


		axis((-85,65,0,150))		
		axes().set_aspect('equal', 'datalim')
		grid(True)
#		show()
		savefig(path+"/wingbeat_figures/"+Q+".svg")



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

	Translation_X_DS=['Translation_X_DS']
	Translation_Y_DS=['Translation_Y_DS']
	Translation_Z_DS=['Translation_Z_DS']

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

	Translation_X_US=['Translation_X_US']
	Translation_Y_US=['Translation_Y_US']
	Translation_Z_US=['Translation_Z_US']

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
			Q = 'Down_'+str(n+1)+'_'+filename[:-4]+'_Right'
		else:
			Q = 'Up_'+str(n+1)+'_'+filename[:-4]+'_Right'

		StrokeAngle((U[n]-1),(U[n+1]-1),1)

		

		Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
		Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
		Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
		Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
		Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
		Output[(U[n]-1):(U[n+1]-1),7] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistanceTraveled



# left wing
		if n%2==0:
			Q = 'Down_'+str(n+1)+'_'+filename[:-4]+'_Left'
		else:
			Q = 'Up_'+str(n+1)+'_'+filename[:-4]+'_Left'

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
			Translation_X_DS.append(HEAD[(U[n+1]-1),0]-HEAD[(U[n]-1),0])
			Translation_Y_DS.append(HEAD[(U[n+1]-1),1]-HEAD[(U[n]-1),1])
			Translation_Z_DS.append(HEAD[(U[n+1]-1),2]-HEAD[(U[n]-1),2])

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
			Translation_X_US.append(HEAD[(U[n+1]-1),0]-HEAD[(U[n]-1),0])
			Translation_Y_US.append(HEAD[(U[n+1]-1),1]-HEAD[(U[n]-1),1])
			Translation_Z_US.append(HEAD[(U[n+1]-1),2]-HEAD[(U[n]-1),2])


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




############################################################################################################################	

	Writer = csv.writer(open(path+"/Angles_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['Body_Angle_lateral','Body_Angle_dorsal','R_Stroke_Plane_Angle', 'R_Position_Angle_Ground','R_Elevation_Angle_Ground','R_Position_Angle_Stroke_Plane','R_Elevation_Angle_Stroke_Plane','R_Wingtip_Distance_Traveled(mm)','L_Stroke_Plane_Angle', 'L_Position_Angle_Ground','L_Elevation_Angle_Ground','L_Position_Angle_Stroke_Plane','L_Elevation_Angle_Stroke_Plane','L_Wingtip_Distance_Traveled(mm)'])
	for N in range(0,U[len(U)-1]-1):
		Writer.writerow(Output[N])

# store output in array

	# Change to convert wingtip velocity from mm/frame to whatever you want (10 = [1000fps*10 upsampled frames]/[1000mm/m])
	FrameMult=10
	#############

	Output2 = zeros((len(Body_Angle_DS)-1,42))

	Output2[:,0] = Number[1:]
	Output2[:,1] = Time_DS[1:]
	Output2[:,2] = Rotation_Angle_DS[1:]
	Output2[:,3] = Body_Angle_DS[1:]
	Output2[:,4] = Body_Angle_YZ_DS[1:]
	Output2[:,5] = SA_Right_DS[1:]
	Output2[:,6] = SA_Left_DS[1:]
	Output2[:,7] = R_Wing_Angle_Avg_Ground_DS[1:]
	Output2[:,8] = L_Wing_Angle_Avg_Ground_DS[1:]
	Output2[:,9] = R_Amp_SP_DS[1:]
	Output2[:,10] = L_Amp_SP_DS[1:]
	Output2[:,11] = R_Wing_Elevation_Amp_DS[1:]
	Output2[:,12] = L_Wing_Elevation_Amp_DS[1:]


	Output2[:,13] = R_Wingtip_Dist_Trav_DS[1:]
	Output2[:,14] = (FrameMult*Output2[:,13]/Output2[:,1])
	Output2[:,15] = L_Wingtip_Dist_Trav_DS[1:]
	Output2[:,16] = (FrameMult*Output2[:,15]/Output2[:,1])


	Output2[:,17] = Number[1:]
	Output2[:,18] = Time_US[1:]
	Output2[:,19] = Rotation_Angle_US[1:]
	Output2[:,20] = Body_Angle_US[1:]
	Output2[:,21] = Body_Angle_YZ_US[1:]
	Output2[:,22] = SA_Right_US[1:]
	Output2[:,23] = SA_Left_US[1:]
	Output2[:,24] = R_Wing_Angle_Avg_Ground_US[1:]
	Output2[:,25] = L_Wing_Angle_Avg_Ground_US[1:]
	Output2[:,26] = R_Amp_SP_US[1:]
	Output2[:,27] = L_Amp_SP_US[1:]
	Output2[:,28] = R_Wing_Elevation_Amp_US[1:]
	Output2[:,29] = L_Wing_Elevation_Amp_US[1:]
	Output2[:,30] = R_Wingtip_Dist_Trav_US[1:]
	Output2[:,31] = (FrameMult*Output2[:,30]/Output2[:,18])
	Output2[:,32] = L_Wingtip_Dist_Trav_US[1:]
	Output2[:,33] = (FrameMult*Output2[:,32]/Output2[:,18])

	Output2[:,34] = Translation_X_DS[1:]
	Output2[:,34] = (FrameMult*Output2[:,34]/Output2[:,1])
	Output2[:,35] = Translation_Y_DS[1:]
	Output2[:,35] = (FrameMult*Output2[:,35]/Output2[:,1])
	Output2[:,36] = Translation_Z_DS[1:]
	Output2[:,36] = (FrameMult*Output2[:,36]/Output2[:,1])
	Output2[:,37] = sqrt(Output2[:,34]**2+Output2[:,35]**2+Output2[:,36]**2)

	Output2[:,38] = Translation_X_US[1:]
	Output2[:,38] = (FrameMult*Output2[:,38]/Output2[:,18])
	Output2[:,39] = Translation_Y_US[1:]
	Output2[:,39] = (FrameMult*Output2[:,39]/Output2[:,18])
	Output2[:,40] =	Translation_Z_US[1:]
	Output2[:,40] = (FrameMult*Output2[:,40]/Output2[:,18])
	Output2[:,41] = sqrt(Output2[:,38]**2+Output2[:,39]**2+Output2[:,40]**2)


#write to file



	Writer = csv.writer(open(path+"/Angles_Summary_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Wingbeat#","Wingbeat_Length_DS", "Travel_Angle_DS", "Body_Angle_Lateral_DS","Body_Angle_Dorsal_DS","R_Stroke_Plane_Angle_DS","L_Stroke_Plane_Angle_DS","R_Avg_Elevation_Angle_Ground_DS","L_Avg_Elevation_Angle_Ground_DS", "R_Amplitude_Stroke_Plane_DS","L_Amplitude_Stroke_Plane_DS","R_Wing_Elevation_Amplitude_Stroke_Plane_DS","L_Wing_Elevation_Amplitude_Stroke_Plane_DS","R_Wingtip_Dist_Traveled_DS(mm)","R_Wingtip_Velocity_DS","L_Wingtip_Dist_Traveled_DS(mm)","L_Wingtip_Velocity_DS","Wingbeat#","Wingbeat_Length_US", "Travel_Angle_US", "Body_Angle_Lateral_US","Body_Angle_Dorsal_US","R_Stroke_Plane_Angle_US","L_Stroke_Plane_Angle_US","R_Avg_Elevation_Angle_Ground_US","L_Avg_Elevation_Angle_Ground_US", "R_Amplitude_Stroke_Plane_US","L_Amplitude_Stroke_Plane_US","R_Wing_Elevation_Amplitude_Stroke_Plane_US","L_Wing_Elevation_Amplitude_Stroke_Plane_US","R_Wingtip_Dist_Traveled_US","R_Wingtip_Velocity_US","L_Wingtip_Dist_Traveled_US","L_Wingtip_Velocity_US","X_vel_DS","Y_vel_DS","Z_vel_DS","Total_vel_DS","X_vel_US","Y_vel_US","Z_vel_US","Total_vel_US"])

	for N in range(len(Body_Angle_DS)-1):
		Writer.writerow(Output2[N])



###################################################################################


# Left minus Right

	Output3 = zeros((len(Body_Angle_DS)-1,22))

	Output3[:,0] = Number[1:]	
	Output3[:,1] = Time_DS[1:]
	Output3[:,2] = Rotation_Angle_DS[1:]
	Output3[:,3] = Body_Angle_DS[1:]
	Output3[:,4] = Body_Angle_YZ_DS[1:]
	Output3[:,5] = Output2[:,6]-Output2[:,5]
	Output3[:,6] = Output2[:,8]-Output2[:,7]
	Output3[:,7] = Output2[:,10]-Output2[:,9]
	Output3[:,8] = Output2[:,12]-Output2[:,11]
	Output3[:,9] = Output2[:,15]-Output2[:,13]
	Output3[:,10] = Output2[:,16]-Output2[:,14]

	Output3[:,11] = Number[1:]  
	Output3[:,12] = Time_US[1:]
	Output3[:,13] = Rotation_Angle_US[1:]
	Output3[:,14] = Body_Angle_US[1:]
	Output3[:,15] = Body_Angle_YZ_US[1:]
	Output3[:,16] = Output2[:,23]-Output2[:,22]
	Output3[:,17] = Output2[:,25]-Output2[:,24]
	Output3[:,18] = Output2[:,27]-Output2[:,26]
	Output3[:,19] = Output2[:,29]-Output2[:,28]
	Output3[:,20] = Output2[:,32]-Output2[:,30]
	Output3[:,21] = Output2[:,33]-Output2[:,31]


	Writer = csv.writer(open(path+"/Angles_Summary_LeftMinusRight_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Wingbeat#","Wingbeat_Length_DS", "Travel_Angle_DS", "Body_Angle_Lateral_DS","Body_Angle_Dorsal_DS","Stroke_Plane_Angle_DS","Avg_Elevation_Angle_Ground_DS", "Amplitude_Stroke_Plane_DS","Wing_Elevation_Amplitude_Stroke_Plane_DS","Wingtip_Dist_Traveled_DS(mm)","Wingtip_Velocity_DS","Wingbeat#","Wingbeat_Length_US", "Travel_Angle_US", "Body_Angle_Lateral_US","Body_Angle_Dorsal_US","Stroke_Plane_Angle_US","Avg_Elevation_Angle_Ground_US", "Amplitude_Stroke_Plane_US","Wing_Elevation_Amplitude_Stroke_Plane_US","Wingtip_Dist_Traveled_US(mm)","Wingtip_Velocity_US"])
	for N in range(len(Body_Angle_DS)-1):
		Writer.writerow(Output3[N])


	
# Graph wingbeat timeseries 

	clf()
	plot(Output3[:,0],Output3[:,2],'bo')
	plot((Output3[:,0]+.5),Output3[:,13],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)
	savefig(path+"/angle_figures/1_Travel_Angle_"+filename[:-4]+".svg")



	clf()
	plot(Output3[:,0],Output3[:,3],'bo')
	plot(Output3[:,0]+.5,Output3[:,14],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,90)
	savefig(path+"/angle_figures/2_Body_Angle_Lateral_"+filename[:-4]+".svg")


	clf()
	plot(Output3[:,0],Output3[:,4],'bo')
	plot((Output3[:,0]+.5),Output3[:,15],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)
	savefig(path+"/angle_figures/3_Body_Angle_Dorsal_"+filename[:-4]+".svg")


	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,5],'ro')
	plot(Output2[:,0]+.5,Output2[:,22],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,25)

	subplot(312)	
	plot(Output2[:,0],Output2[:,6],'bo')
	plot(Output2[:,0]+.5,Output2[:,23],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,25)
	
	subplot(313)
	plot(Output3[:,0],Output3[:,5],'go')
	plot((Output3[:,0]+.5),Output3[:,16],'ko')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)

	savefig(path+"/angle_figures/4_Stroke_Angle_"+filename[:-4]+".svg")



	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,7],'ro')
	plot(Output2[:,0]+.5,Output2[:,24],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,20)

	subplot(312)	
	plot(Output2[:,0],Output2[:,8],'bo')
	plot(Output2[:,0]+.5,Output2[:,25],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,20)

	subplot(313)
	plot(Output3[:,0],Output3[:,6],'go')
	plot((Output3[:,0]+.5),Output3[:,17],'ko')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)
	savefig(path+"/angle_figures/5_Avg_Elevation_Angle_Ground_"+filename[:-4]+".svg")


	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,9],'ro')
	plot(Output2[:,0]+.5,Output2[:,26],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,180)

	subplot(312)	
	plot(Output2[:,0],Output2[:,10],'bo')
	plot(Output2[:,0]+.5,Output2[:,27],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,180)

	subplot(313)
	plot(Output3[:,0],Output3[:,7],'go')
	plot((Output3[:,0]+.5),Output3[:,18],'ko')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)
	savefig(path+"/angle_figures/6_Amplitude_SP_"+filename[:-4]+".svg")



	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,11],'ro')
	plot(Output2[:,0]+.5,Output2[:,28],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-25,25)

	subplot(312)	
	plot(Output2[:,0],Output2[:,12],'bo')
	plot(Output2[:,0]+.5,Output2[:,29],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-25,25)

	subplot(313)
	plot(Output3[:,0],Output3[:,8],'go')
	plot((Output3[:,0]+.5),Output3[:,19],'ko')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)

	savefig(path+"/angle_figures/7_Elevation_Amplitude_SP_"+filename[:-4]+".svg")




	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,14],'ro')
	plot(Output2[:,0]+.5,Output2[:,31],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,15)

	subplot(312)	
	plot(Output2[:,0],Output2[:,16],'bo')
	plot(Output2[:,0]+.5,Output2[:,33],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,15)

	subplot(313)
	plot(Output3[:,0],Output3[:,10],'go')
	plot((Output3[:,0]+.5),Output3[:,21],'ko')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-10,10)

	savefig(path+"/angle_figures/8_Wingtip_Velocity_"+filename[:-4]+".svg")

	

###################################################################################################		

# Wingbeat Average Calculations
	clf()
	def WingbeatAverage(O,P,Q,R):

		b=Transformed[(O):(P),(Q)]
		a=range(1,len(b)+1)		

		c= interpolate.splrep(a,b)
		d= linspace(1,(len(b)+1),num=100)
		
		
		R[:,0] = linspace(1,25,num=100)		
		R[:,((n/2)+3)] = interpolate.splev(d,c)



# Average Wingbeat
	
	aa= zeros((100,((len(U)-1)/2)+3))
	ab= zeros((100,((len(U)-1)/2)+3))
	ac= zeros((100,((len(U)-1)/2)+3))
	ad= zeros((100,((len(U)-1)/2)+3))
	ae= zeros((100,((len(U)-1)/2)+3))
	af= zeros((100,((len(U)-1)/2)+3))
	ag= zeros((100,((len(U)-1)/2)+3))
	ah= zeros((100,((len(U)-1)/2)+3))
	ai= zeros((100,((len(U)-1)/2)+3))
	aj= zeros((100,((len(U)-1)/2)+3))
	ak= zeros((100,((len(U)-1)/2)+3))
	al= zeros((100,((len(U)-1)/2)+3))
	am= zeros((100,((len(U)-1)/2)+3))
	an= zeros((100,((len(U)-1)/2)+3))
	ao= zeros((100,((len(U)-1)/2)+3))
	ap= zeros((100,((len(U)-1)/2)+3))
	aq= zeros((100,((len(U)-1)/2)+3))
	ar= zeros((100,((len(U)-1)/2)+3))


	ba= zeros((100,((len(U)-1)/2)+3))
	bb= zeros((100,((len(U)-1)/2)+3))
	bc= zeros((100,((len(U)-1)/2)+3))
	bd= zeros((100,((len(U)-1)/2)+3))
	be= zeros((100,((len(U)-1)/2)+3))
	bf= zeros((100,((len(U)-1)/2)+3))
	bg= zeros((100,((len(U)-1)/2)+3))
	bh= zeros((100,((len(U)-1)/2)+3))
	bi= zeros((100,((len(U)-1)/2)+3))
	bj= zeros((100,((len(U)-1)/2)+3))
	bk= zeros((100,((len(U)-1)/2)+3))
	bl= zeros((100,((len(U)-1)/2)+3))
	bm= zeros((100,((len(U)-1)/2)+3))
	bn= zeros((100,((len(U)-1)/2)+3))
	bo= zeros((100,((len(U)-1)/2)+3))
	bp= zeros((100,((len(U)-1)/2)+3))
	bq= zeros((100,((len(U)-1)/2)+3))
	br= zeros((100,((len(U)-1)/2)+3))

# Downstroke

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),0,aa)
	RShoulder_Avg_DS_X=aa

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),1,ab)
	RShoulder_Avg_DS_Y=ab

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),2,ac)
	RShoulder_Avg_DS_Z=ac





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),3,ad)
	RWing_Avg_DS_X=ad

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),4,ae)
	RWing_Avg_DS_Y=ae

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),5,af)
	RWing_Avg_DS_Z=af





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),6,ag)
	LShoulder_Avg_DS_X=ag

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),7,ah)
	LShoulder_Avg_DS_Y=ah

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),8,ai)
	LShoulder_Avg_DS_Z=ai





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),9,aj)
	LWing_Avg_DS_X=aj

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),10,ak)
	LWing_Avg_DS_Y=ak

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),11,al)
	LWing_Avg_DS_Z=al




	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),12,am)
	Head_Avg_DS_X=am

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),13,an)
	Head_Avg_DS_Y=an

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),14,ao)
	Head_Avg_DS_Z=ao





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),15,ap)
	Tail_Avg_DS_X=ap

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),16,aq)
	Tail_Avg_DS_Y=aq

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),17,ar)
	Tail_Avg_DS_Z=ar




	for n in range (0,100):
		RShoulder_Avg_DS_X[n,1]=average(RShoulder_Avg_DS_X[n,3:])
		RShoulder_Avg_DS_Y[n,1]=average(RShoulder_Avg_DS_Y[n,3:])
		RShoulder_Avg_DS_Z[n,1]=average(RShoulder_Avg_DS_Z[n,3:])

		RWing_Avg_DS_X[n,1]=average(RWing_Avg_DS_X[n,3:])
		RWing_Avg_DS_Y[n,1]=average(RWing_Avg_DS_Y[n,3:])
		RWing_Avg_DS_Z[n,1]=average(RWing_Avg_DS_Z[n,3:])

		LShoulder_Avg_DS_X[n,1]=average(LShoulder_Avg_DS_X[n,3:])
		LShoulder_Avg_DS_Y[n,1]=average(LShoulder_Avg_DS_Y[n,3:])
		LShoulder_Avg_DS_Z[n,1]=average(LShoulder_Avg_DS_Z[n,3:])

		LWing_Avg_DS_X[n,1]=average(LWing_Avg_DS_X[n,3:])
		LWing_Avg_DS_Y[n,1]=average(LWing_Avg_DS_Y[n,3:])
		LWing_Avg_DS_Z[n,1]=average(LWing_Avg_DS_Z[n,3:])

		Head_Avg_DS_X[n,1]=average(Head_Avg_DS_X[n,3:])
		Head_Avg_DS_Y[n,1]=average(Head_Avg_DS_Y[n,3:])
		Head_Avg_DS_Z[n,1]=average(Head_Avg_DS_Z[n,3:])

		Tail_Avg_DS_X[n,1]=average(Tail_Avg_DS_X[n,3:])
		Tail_Avg_DS_Y[n,1]=average(Tail_Avg_DS_Y[n,3:])
		Tail_Avg_DS_Z[n,1]=average(Tail_Avg_DS_Z[n,3:])




		#StErr
		RShoulder_Avg_DS_X[n,2]=(std(RShoulder_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		RShoulder_Avg_DS_Y[n,2]=(std(RShoulder_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		RShoulder_Avg_DS_Z[n,2]=(std(RShoulder_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

		RWing_Avg_DS_X[n,2]=(std(RWing_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		RWing_Avg_DS_Y[n,2]=(std(RWing_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		RWing_Avg_DS_Z[n,2]=(std(RWing_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

		LShoulder_Avg_DS_X[n,2]=(std(LShoulder_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_DS_Y[n,2]=(std(LShoulder_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_DS_Z[n,2]=(std(LShoulder_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

		LWing_Avg_DS_X[n,2]=(std(LWing_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		LWing_Avg_DS_Y[n,2]=(std(LWing_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		LWing_Avg_DS_Z[n,2]=(std(LWing_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

		Head_Avg_DS_X[n,2]=(std(Head_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		Head_Avg_DS_Y[n,2]=(std(Head_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		Head_Avg_DS_Z[n,2]=(std(Head_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

		Tail_Avg_DS_X[n,2]=(std(Tail_Avg_DS_X[n,3:]))/(sqrt((len(U)-1)/2))
		Tail_Avg_DS_Y[n,2]=(std(Tail_Avg_DS_Y[n,3:]))/(sqrt((len(U)-1)/2))
		Tail_Avg_DS_Z[n,2]=(std(Tail_Avg_DS_Z[n,3:]))/(sqrt((len(U)-1)/2))

#Upstroke


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),0,ba)	
	RShoulder_Avg_US_X=ba


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),1,bb)
	RShoulder_Avg_US_Y=bb

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),2,bc)
	RShoulder_Avg_US_Z=bc





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),3,bd)
	RWing_Avg_US_X=bd

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),4,be)
	RWing_Avg_US_Y=be

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),5,bf)
	RWing_Avg_US_Z=bf





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),6,bg)
	LShoulder_Avg_US_X=bg

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),7,bh)
	LShoulder_Avg_US_Y=bh

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),8,bi)
	LShoulder_Avg_US_Z=bi





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),9,bj)
	LWing_Avg_US_X=bj

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),10,bk)
	LWing_Avg_US_Y=bk

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),11,bl)
	LWing_Avg_US_Z=bl




	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),12,bm)
	Head_Avg_US_X=bm

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),13,bn)
	Head_Avg_US_Y=bn

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),14,bo)
	Head_Avg_US_Z=bo





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),15,bp)
	Tail_Avg_US_X=bp

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),16,bq)
	Tail_Avg_US_Y=bq

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),17,br)
	Tail_Avg_US_Z=br




	for n in range (0,100):
		RShoulder_Avg_US_X[n,1]=average(RShoulder_Avg_US_X[n,3:])
		RShoulder_Avg_US_Y[n,1]=average(RShoulder_Avg_US_Y[n,3:])
		RShoulder_Avg_US_Z[n,1]=average(RShoulder_Avg_US_Z[n,3:])

		RWing_Avg_US_X[n,1]=average(RWing_Avg_US_X[n,3:])
		RWing_Avg_US_Y[n,1]=average(RWing_Avg_US_Y[n,3:])
		RWing_Avg_US_Z[n,1]=average(RWing_Avg_US_Z[n,3:])

		LShoulder_Avg_US_X[n,1]=average(LShoulder_Avg_US_X[n,3:])
		LShoulder_Avg_US_Y[n,1]=average(LShoulder_Avg_US_Y[n,3:])
		LShoulder_Avg_US_Z[n,1]=average(LShoulder_Avg_US_Z[n,3:])

		LWing_Avg_US_X[n,1]=average(LWing_Avg_US_X[n,3:])
		LWing_Avg_US_Y[n,1]=average(LWing_Avg_US_Y[n,3:])
		LWing_Avg_US_Z[n,1]=average(LWing_Avg_US_Z[n,3:])

		Head_Avg_US_X[n,1]=average(Head_Avg_US_X[n,3:])
		Head_Avg_US_Y[n,1]=average(Head_Avg_US_Y[n,3:])
		Head_Avg_US_Z[n,1]=average(Head_Avg_US_Z[n,3:])

		Tail_Avg_US_X[n,1]=average(Tail_Avg_US_X[n,3:])
		Tail_Avg_US_Y[n,1]=average(Tail_Avg_US_Y[n,3:])
		Tail_Avg_US_Z[n,1]=average(Tail_Avg_US_Z[n,3:])



##########

		RShoulder_Avg_US_X[n,2]=(std(RShoulder_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		RShoulder_Avg_US_Y[n,2]=(std(RShoulder_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		RShoulder_Avg_US_Z[n,2]=(std(RShoulder_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))

		RWing_Avg_US_X[n,2]=(std(RWing_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		RWing_Avg_US_Y[n,2]=(std(RWing_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		RWing_Avg_US_Z[n,2]=(std(RWing_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))

		LShoulder_Avg_US_X[n,2]=(std(LShoulder_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_US_Y[n,2]=(std(LShoulder_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_US_Z[n,2]=(std(LShoulder_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))

		LWing_Avg_US_X[n,2]=(std(LWing_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		LWing_Avg_US_Y[n,2]=(std(LWing_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		LWing_Avg_US_Z[n,2]=(std(LWing_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))

		Head_Avg_US_X[n,2]=(std(Head_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		Head_Avg_US_Y[n,2]=(std(Head_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		Head_Avg_US_Z[n,2]=(std(Head_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))

		Tail_Avg_US_X[n,2]=(std(Tail_Avg_US_X[n,3:]))/(sqrt((len(U)-1)/2))
		Tail_Avg_US_Y[n,2]=(std(Tail_Avg_US_Y[n,3:]))/(sqrt((len(U)-1)/2))
		Tail_Avg_US_Z[n,2]=(std(Tail_Avg_US_Z[n,3:]))/(sqrt((len(U)-1)/2))
		
################


	AvgWingbeat = column_stack((RShoulder_Avg_DS_X[:,1], RShoulder_Avg_DS_Y[:,1], RShoulder_Avg_DS_Z[:,1], RWing_Avg_DS_X[:,1], RWing_Avg_DS_Y[:,1], RWing_Avg_DS_Z[:,1],LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Y[:,1],LShoulder_Avg_DS_Z[:,1], LWing_Avg_DS_X[:,1], LWing_Avg_DS_Y[:,1], LWing_Avg_DS_Z[:,1],Head_Avg_DS_X[:,1],Head_Avg_DS_Y[:,1],Head_Avg_DS_Z[:,1], Tail_Avg_DS_X[:,1], Tail_Avg_DS_Y[:,1], Tail_Avg_DS_Z[:,1],RShoulder_Avg_US_X[:,1], RShoulder_Avg_US_Y[:,1], RShoulder_Avg_US_Z[:,1], RWing_Avg_US_X[:,1], RWing_Avg_US_Y[:,1], RWing_Avg_US_Z[:,1],LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Y[:,1],LShoulder_Avg_US_Z[:,1], LWing_Avg_US_X[:,1], LWing_Avg_US_Y[:,1], LWing_Avg_US_Z[:,1],Head_Avg_US_X[:,1],Head_Avg_US_Y[:,1],Head_Avg_US_Z[:,1], Tail_Avg_US_X[:,1], Tail_Avg_US_Y[:,1], Tail_Avg_US_Z[:,1]))

	AvgWingbeatStEr = column_stack((RShoulder_Avg_DS_X[:,2], RShoulder_Avg_DS_Y[:,2], RShoulder_Avg_DS_Z[:,2], RWing_Avg_DS_X[:,2], RWing_Avg_DS_Y[:,2], RWing_Avg_DS_Z[:,2],LShoulder_Avg_DS_X[:,2],LShoulder_Avg_DS_Y[:,2],LShoulder_Avg_DS_Z[:,2], LWing_Avg_DS_X[:,2], LWing_Avg_DS_Y[:,2], LWing_Avg_DS_Z[:,2],Head_Avg_DS_X[:,2],Head_Avg_DS_Y[:,2],Head_Avg_DS_Z[:,2], Tail_Avg_DS_X[:,2], Tail_Avg_DS_Y[:,2], Tail_Avg_DS_Z[:,2],RShoulder_Avg_US_X[:,2], RShoulder_Avg_US_Y[:,2], RShoulder_Avg_US_Z[:,2], RWing_Avg_US_X[:,2], RWing_Avg_US_Y[:,2], RWing_Avg_US_Z[:,2],LShoulder_Avg_US_X[:,2],LShoulder_Avg_US_Y[:,2],LShoulder_Avg_US_Z[:,2], LWing_Avg_US_X[:,2], LWing_Avg_US_Y[:,2], LWing_Avg_US_Z[:,2],Head_Avg_US_X[:,2],Head_Avg_US_Y[:,2],Head_Avg_US_Z[:,2], Tail_Avg_US_X[:,2], Tail_Avg_US_Y[:,2], Tail_Avg_US_Z[:,2]))

	Writer = csv.writer(open(path+"/average_graphs/WingbeatAverage_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['RShoulder_DS_X','RShoulder_DS_Y','RShoulder_DS_Z','RWing_DS_X','RWing_DS_Y','RWing_DS_Z','LShoulder_DS_X','LShoulder_DS_Y','LShoulder_DS_Z','LWing_DS_X', 'LWing_DS_Y','LWing_DS_Z','Head_DS_X','Head_DS_Y','Head_DS_Z','Tail_DS_X','Tail_DS_Y','Tail_DS_Z','RShoulder_US_X','RShoulder_US_Y','RShoulder_US_Z','RWing_US_X','RWing_US_Y','RWing_US_Z','LShoulder_US_X','LShoulder_US_Y','LShoulder_US_Z','LWing_US_X', 'LWing_US_Y','LWing_US_Z','Head_US_X','Head_US_Y','Head_US_Z','Tail_US_X','Tail_US_Y','Tail_US_Z'])
	for N in range(0,100):
		Writer.writerow(AvgWingbeat[N])

	Writer = csv.writer(open(path+"/average_graphs/WingbeatAvgStErr_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['RShoulder_DS_X','RShoulder_DS_Y','RShoulder_DS_Z','RWing_DS_X','RWing_DS_Y','RWing_DS_Z','LShoulder_DS_X','LShoulder_DS_Y','LShoulder_DS_Z','LWing_DS_X', 'LWing_DS_Y','LWing_DS_Z','Head_DS_X','Head_DS_Y','Head_DS_Z','Tail_DS_X','Tail_DS_Y','Tail_DS_Z','RShoulder_US_X','RShoulder_US_Y','RShoulder_US_Z','RWing_US_X','RWing_US_Y','RWing_US_Z','LShoulder_US_X','LShoulder_US_Y','LShoulder_US_Z','LWing_US_X', 'LWing_US_Y','LWing_US_Z','Head_US_X','Head_US_Y','Head_US_Z','Tail_US_X','Tail_US_Y','Tail_US_Z'])
	for N in range(0,100):
		Writer.writerow(AvgWingbeatStEr[N])


# plot all points 


	clf()
	plot(LWing_Avg_DS_X[:,1],LWing_Avg_DS_Z[:,1],c='r')
	plot(LWing_Avg_US_X[:,1],LWing_Avg_US_Z[:,1],c='r')

	plot(LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Z[:,1],c='y')
	plot(LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Z[:,1],c='y')

	plot(RWing_Avg_DS_X[:,1],RWing_Avg_DS_Z[:,1],c='b')
	plot(RWing_Avg_US_X[:,1],RWing_Avg_US_Z[:,1],c='b')

	plot(RShoulder_Avg_DS_X[:,1],RShoulder_Avg_DS_Z[:,1],c='g')
	plot(RShoulder_Avg_US_X[:,1],RShoulder_Avg_US_Z[:,1],c='g')

	scatter(Head_Avg_DS_X[:,1],Head_Avg_DS_Z[:,1],c='m')
	scatter(Head_Avg_US_X[:,1],Head_Avg_US_Z[:,1],c='m')

	plot(Tail_Avg_DS_X[:,1],Tail_Avg_DS_Z[:,1],c='c')
	plot(Tail_Avg_US_X[:,1],Tail_Avg_US_Z[:,1],c='c')	

	axis((-85,65,0,150))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/average_graphs/XZ_avg_'+filename[:-4]+'.svg')


	clf()
	plot(LWing_Avg_DS_Y[:,1],LWing_Avg_DS_Z[:,1],c='r')
	plot(LWing_Avg_US_Y[:,1],LWing_Avg_US_Z[:,1],c='r')

	plot(LShoulder_Avg_DS_Y[:,1],LShoulder_Avg_DS_Z[:,1],c='y')
	plot(LShoulder_Avg_US_Y[:,1],LShoulder_Avg_US_Z[:,1],c='y')

	plot(RWing_Avg_DS_Y[:,1],RWing_Avg_DS_Z[:,1],c='b')
	plot(RWing_Avg_US_Y[:,1],RWing_Avg_US_Z[:,1],c='b')

	plot(RShoulder_Avg_DS_Y[:,1],RShoulder_Avg_DS_Z[:,1],c='g')
	plot(RShoulder_Avg_US_Y[:,1],RShoulder_Avg_US_Z[:,1],c='g')

	scatter(Head_Avg_DS_Y[:,1],Head_Avg_DS_Z[:,1],c='m')
	scatter(Head_Avg_US_Y[:,1],Head_Avg_US_Z[:,1],c='m')

	plot(Tail_Avg_DS_Y[:,1],Tail_Avg_DS_Z[:,1],c='c')
	plot(Tail_Avg_US_Y[:,1],Tail_Avg_US_Z[:,1],c='c')

	axis((-75,75,0,150))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/average_graphs/YZ_avg_'+filename[:-4]+'.svg')





	clf()
	plot(LWing_Avg_DS_X[:,1],LWing_Avg_DS_Y[:,1],c='r')
	plot(LWing_Avg_US_X[:,1],LWing_Avg_US_Y[:,1],c='r')

	plot(LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Y[:,1],c='y')
	plot(LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Y[:,1],c='y')

	plot(RWing_Avg_DS_X[:,1],RWing_Avg_DS_Y[:,1],c='b')
	plot(RWing_Avg_US_X[:,1],RWing_Avg_US_Y[:,1],c='b')

	plot(RShoulder_Avg_DS_X[:,1],RShoulder_Avg_DS_Y[:,1],c='g')
	plot(RShoulder_Avg_US_X[:,1],RShoulder_Avg_US_Y[:,1],c='g')

	scatter(Head_Avg_DS_X[:,1],Head_Avg_DS_Y[:,1],c='m')
	scatter(Head_Avg_US_X[:,1],Head_Avg_US_Y[:,1],c='m')

	plot(Tail_Avg_DS_X[:,1],Tail_Avg_DS_Y[:,1],c='c')
	plot(Tail_Avg_US_X[:,1],Tail_Avg_US_Y[:,1],c='c')

	axis((-85,65,-75,75))
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig(path+'/average_graphs/XY_avg_'+filename[:-4]+'.svg')



####################################################################################################
	

# Per Wingbeat Calculations
	clf()
	def PerWingbeat(O,P,Q,R):

		b=Output[(O):(P),(Q)]
		a=range(1,len(b)+1)		

		c= interpolate.splrep(a,b)
		d= linspace(1,(len(b)+1),num=100)
		
		
		R[:,0] = linspace(1,25,num=100)		
		R[:,((n/2)+3)] = interpolate.splev(d,c)



###########################################################################################################################

# Position and Deviation from Stroke Plane 
#Downstroke

	g= zeros((100,((len(U)-1)/2)+3))		
	h= zeros((100,((len(U)-1)/2)+3))
	i= zeros((100,((len(U)-1)/2)+3))		
	j= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),5,g)
	RPosition_SP_DS=g


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),6,h)
	RDeviation_SP_DS=h


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),11,i)
	LPosition_SP_DS=i


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),12,j)
	LDeviation_SP_DS=j


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_SP_DS[n,1]=average(RPosition_SP_DS[n,3:])
		RDeviation_SP_DS[n,1]=average(RDeviation_SP_DS[n,3:])
		RPosition_SP_DS[n,2]=std(RPosition_SP_DS[n,3:])
		RDeviation_SP_DS[n,2]=std(RDeviation_SP_DS[n,3:])

		LPosition_SP_DS[n,1]=average(LPosition_SP_DS[n,3:])
		LDeviation_SP_DS[n,1]=average(LDeviation_SP_DS[n,3:])
		LPosition_SP_DS[n,2]=std(LPosition_SP_DS[n,3:])
		LDeviation_SP_DS[n,2]=std(LDeviation_SP_DS[n,3:])

		


################################# --- same for upstroke



	p= zeros((100,((len(U)-1)/2)+3))		
	q= zeros((100,((len(U)-1)/2)+3))
	r= zeros((100,((len(U)-1)/2)+3))		
	s= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),5,p)
	RPosition_SP_US=p


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),6,q)
	RDeviation_SP_US=q


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),11,r)
	LPosition_SP_US=r


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),12,s)
	LDeviation_SP_US=s


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_SP_US[n,1]=average(RPosition_SP_US[n,3:])
		RDeviation_SP_US[n,1]=average(RDeviation_SP_US[n,3:])
		RPosition_SP_US[n,2]=std(RPosition_SP_US[n,3:])
		RDeviation_SP_US[n,2]=std(RDeviation_SP_US[n,3:])

		LPosition_SP_US[n,1]=average(LPosition_SP_US[n,3:])
		LDeviation_SP_US[n,1]=average(LDeviation_SP_US[n,3:])
		LPosition_SP_US[n,2]=std(LPosition_SP_US[n,3:])
		LDeviation_SP_US[n,2]=std(LDeviation_SP_US[n,3:])

# Consolidate

	RPosition_SP = vstack((RPosition_SP_DS,RPosition_SP_US))
	LPosition_SP = vstack((LPosition_SP_DS,LPosition_SP_US))
	RDeviation_SP = vstack((RDeviation_SP_DS,RDeviation_SP_US))
	LDeviation_SP = vstack((LDeviation_SP_DS,LDeviation_SP_US))

	RPosition_SP[:,0] = arange(200)
	LPosition_SP[:,0] = arange(200)
	RDeviation_SP[:,0] = arange(200)
	LDeviation_SP[:,0] = arange(200)



# 	graph		

	clf()
	scatter(RDeviation_SP[:,0],RDeviation_SP[:,1],c='b')
	scatter(LDeviation_SP[:,0],LDeviation_SP[:,1],c='r')
	axis((0,200,-45,45))

	savefig(path+'/wingbeat_timecourse/PosElev_SP/LRElevation_SP_'+filename[:-4])
#	show()

	clf()
	scatter(RPosition_SP[:,0],RPosition_SP[:,1],c='b')
	scatter(LPosition_SP[:,0],LPosition_SP[:,1],c='r')
	axis((0,200,-10,190))
	savefig(path+'/wingbeat_timecourse/PosElev_SP/LRPosition_SP_'+filename[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(RDeviation_SP[1,:])):	
		clf()
		scatter(RDeviation_SP[:,0],RDeviation_SP[:,n],c='b')
		scatter(LDeviation_SP[:,0],LDeviation_SP[:,n],c='r')
		axis((0,200,-45,45))
		savefig(path+'/wingbeat_timecourse/PosElev_SP/Graphs/LRElevation_SP_'+str(n-2)+"_"+filename[:-4])

		clf()
		scatter(RPosition_SP[:,0],RPosition_SP[:,n],c='b')
		scatter(LPosition_SP[:,0],LPosition_SP[:,n],c='r')
		axis((0,200,-10,190))
		savefig(path+'/wingbeat_timecourse/PosElev_SP/Graphs/LRPosition_SP_'+str(n-2)+"_"+filename[:-4])



#	Write Output


	header = ['Time','Average','StDev']
	for n in range(3,len(RDeviation_SP[1,:])):
		header.append(n-2)


	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_SP/RPosition_SP_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(RPosition_SP[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_SP/RElevation_SP_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(RDeviation_SP[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_SP/LPosition_SP_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LPosition_SP[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_SP/LElevation_SP_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LDeviation_SP[N])




#######################
	#summary file

	LRPosElev_SP_Summary=zeros((100,8))
	LRPosElev_SP_Summary[:,0]=LDeviation_SP_DS[:,1]
	LRPosElev_SP_Summary[:,1]=LDeviation_SP_DS[:,2]
	LRPosElev_SP_Summary[:,2]=LDeviation_SP_US[:,1]
	LRPosElev_SP_Summary[:,3]=LDeviation_SP_US[:,2]
	LRPosElev_SP_Summary[:,4]=RDeviation_SP_DS[:,1]
	LRPosElev_SP_Summary[:,5]=RDeviation_SP_DS[:,2]
	LRPosElev_SP_Summary[:,6]=RDeviation_SP_US[:,1]
	LRPosElev_SP_Summary[:,7]=RDeviation_SP_US[:,2]
	

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_SP/Summary_LRPosElev_SP_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Left_Downstroke_Avg","Left_Downstroke_StErr","Left_Upstroke_Avg","Left_Upstroke_StErr","Right_Downstroke_Avg","Right_Downstroke_StErr","Right_Upstroke_Avg","Right_Upstroke_StErr"])
	for N in range(0,100):
		Writer.writerow(LRPosElev_SP_Summary[N])
######################################################################################################################

# Position and Deviation from Horizontal

	g= zeros((100,((len(U)-1)/2)+3))		
	h= zeros((100,((len(U)-1)/2)+3))
	i= zeros((100,((len(U)-1)/2)+3))		
	j= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),3,g)
	RPosition_GR_DS=g


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),4,h)
	RDeviation_GR_DS=h


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),9,i)
	LPosition_GR_DS=i


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),10,j)
	LDeviation_GR_DS=j


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_GR_DS[n,1]=average(RPosition_GR_DS[n,3:])
		RDeviation_GR_DS[n,1]=average(RDeviation_GR_DS[n,3:])
		RPosition_GR_DS[n,2]=std(RPosition_GR_DS[n,3:])
		RDeviation_GR_DS[n,2]=std(RDeviation_GR_DS[n,3:])

		LPosition_GR_DS[n,1]=average(LPosition_GR_DS[n,3:])
		LDeviation_GR_DS[n,1]=average(LDeviation_GR_DS[n,3:])
		LPosition_GR_DS[n,2]=std(LPosition_GR_DS[n,3:])
		LDeviation_GR_DS[n,2]=std(LDeviation_SP_DS[n,3:])


##################upstroke

	k= zeros((100,((len(U)-1)/2)+3))		
	l= zeros((100,((len(U)-1)/2)+3))
	m= zeros((100,((len(U)-1)/2)+3))		
	o= zeros((100,((len(U)-1)/2)+3))


	
	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),3,k)
	RPosition_GR_US=k


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),4,l)
	RDeviation_GR_US=l


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),9,m)
	LPosition_GR_US=m


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),10,o)
	LDeviation_GR_US=o


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		RPosition_GR_US[n,1]=average(RPosition_GR_US[n,3:])
		RDeviation_GR_US[n,1]=average(RDeviation_GR_US[n,3:])
		RPosition_GR_US[n,2]=std(RPosition_GR_US[n,3:])
		RDeviation_GR_US[n,2]=std(RDeviation_GR_US[n,3:])

		LPosition_GR_US[n,1]=average(LPosition_GR_US[n,3:])
		LDeviation_GR_US[n,1]=average(LDeviation_GR_US[n,3:])
		LPosition_GR_US[n,2]=std(LPosition_GR_US[n,3:])
		LDeviation_GR_US[n,2]=std(LDeviation_GR_US[n,3:])

# Consolidate

	RPosition_GR = vstack((RPosition_GR_DS,RPosition_GR_US))
	LPosition_GR = vstack((LPosition_GR_DS,LPosition_GR_US))
	RDeviation_GR = vstack((RDeviation_GR_DS,RDeviation_GR_US))
	LDeviation_GR = vstack((LDeviation_GR_DS,LDeviation_GR_US))

	RPosition_GR[:,0] = arange(200)
	LPosition_GR[:,0] = arange(200)
	RDeviation_GR[:,0] = arange(200)
	LDeviation_GR[:,0] = arange(200)



# 	graph		

	clf()
	scatter(RDeviation_GR[:,0],RDeviation_GR[:,1],c='b')
	scatter(LDeviation_GR[:,0],LDeviation_GR[:,1],c='r')
	axis((0,200,-45,45))

	savefig(path+'/wingbeat_timecourse/PosElev_GR/LRElevation_GR_'+filename[:-4])
#	show()

	clf()
	scatter(RPosition_GR[:,0],RPosition_GR[:,1],c='b')
	scatter(LPosition_GR[:,0],LPosition_GR[:,1],c='r')
	axis((0,200,-10,190))
	savefig(path+'/wingbeat_timecourse/PosElev_GR/LRPosition_GR_'+filename[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(RDeviation_GR[1,:])):	
		clf()
		scatter(RDeviation_GR[:,0],RDeviation_GR[:,n],c='b')
		scatter(LDeviation_GR[:,0],LDeviation_GR[:,n],c='r')
		axis((0,200,-45,45))
		savefig(path+'/wingbeat_timecourse/PosElev_GR/Graphs/LRElevation_GR_'+str(n-2)+"_"+filename[:-4])

		clf()
		scatter(RPosition_GR[:,0],RPosition_GR[:,n],c='b')
		scatter(LPosition_GR[:,0],LPosition_GR[:,n],c='r')
		axis((0,200,-10,190))
		savefig(path+'/wingbeat_timecourse/PosElev_GR/Graphs/LRPosition_GR_'+str(n-2)+"_"+filename[:-4])



#	Write Output


	header = ['Time','Average','StDev']
	for n in range(3,len(RDeviation_GR[1,:])):
		header.append(n-2)


	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_GR/RPosition_GR_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(RPosition_GR[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_GR/RElevation_GR_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(RDeviation_GR[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_GR/LPosition_GR_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LPosition_GR[N])

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_GR/LElevation_GR_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LDeviation_GR[N])

################################
	LRPosElev_GR_Summary=zeros((100,8))
	LRPosElev_GR_Summary[:,0]=LDeviation_GR_DS[:,1]
	LRPosElev_GR_Summary[:,1]=LDeviation_GR_DS[:,2]
	LRPosElev_GR_Summary[:,2]=LDeviation_GR_US[:,1]
	LRPosElev_GR_Summary[:,3]=LDeviation_GR_US[:,2]
	LRPosElev_GR_Summary[:,4]=RDeviation_GR_DS[:,1]
	LRPosElev_GR_Summary[:,5]=RDeviation_GR_DS[:,2]
	LRPosElev_GR_Summary[:,6]=RDeviation_GR_US[:,1]
	LRPosElev_GR_Summary[:,7]=RDeviation_GR_US[:,2]
	

	Writer = csv.writer(open(path+"/wingbeat_timecourse/PosElev_GR/Summary_LRPosElev_GR_"+filename, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Left_Downstroke_Avg","Left_Downstroke_StErr","Left_Upstroke_Avg","Left_Upstroke_StErr","Right_Downstroke_Avg","Right_Downstroke_StErr","Right_Upstroke_Avg","Right_Upstroke_StErr"])
	for N in range(0,100):
		Writer.writerow(LRPosElev_GR_Summary[N])



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
