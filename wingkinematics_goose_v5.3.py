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
Version # goose_5.3 4-7-2012

Usage: %s [INPUT_FILE_NAME]

Input values should be saved in the second line of a comma_separated_value (.csv) file as follows:

LShoulder_X,Y,Z, LWrist_X,Y,Z, LWing_X,Y,Z,LSecond_X,Y,Z,LRoot_X,Y,Z,Head_X,Y,Z,Tail_X,Y,Z

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

# input files

	inFile = open(file,"r")
    	lines = inFile.readlines()	

	inFile2 = open(time,"r")
	lines2 = inFile2.readlines()	


    	Data= zeros(((len(lines)-1),21), Float)




    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]),float(temp[18]),float(temp[19]),float(temp[20]))	


	temp2= str(lines2[1]).split(',')
	U=[]
	
	for N in range(0,len(temp2)):	
		U.append(int(temp2[N]))		
		

# Make directory for figures
	if 1:
		os.mkdir("wingbeat_figures")
		os.mkdir("angle_figures")
		os.mkdir("wingbeat_timecourse")
		os.mkdir("wingbeat_timecourse/PosElev_SP")
		os.mkdir("wingbeat_timecourse/PosElev_SP/Graphs")
		os.mkdir("wingbeat_timecourse/PosElev_GR")
		os.mkdir("wingbeat_timecourse/PosElev_GR/Graphs")
		os.mkdir("average_graphs")
# Define Output Arrays


	Output1= zeros(((U[len(U)-1]-1),7))
	Output= zeros(((U[len(U)-1]-1),8))



# Read data from input array


	LSHOULDER= zeros((((len(lines)-2))+1,3))
	LWRIST= zeros((((len(lines)-2))+1,3))
	LWING= zeros((((len(lines)-2))+1,3))
	LSECOND= zeros((((len(lines)-2))+1,3))
	LROOT= zeros((((len(lines)-2))+1,3))	
	HEAD= zeros((((len(lines)-2))+1,3))
	TAIL= zeros((((len(lines)-2))+1,3))
	

	LSHOULDER[:,0:3]=Data[:,0:3]
	LWRIST[:,0:3]=Data[:,3:6]
	LWING[:,0:3]=Data[:,6:9]
	LSECOND[:,0:3]=Data[:,9:12]
	LROOT[:,0:3]=Data[:,12:15]
	HEAD[:,0:3]=Data[:,15:18]	
	TAIL[:,0:3]=Data[:,18:21]

	


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
	Tail1[:,1]=0



# Define global output data matrices
	LShoulder= zeros(((U[len(U)-1]-1),3))
	LWrist= zeros(((U[len(U)-1]-1),3))
	LWing= zeros(((U[len(U)-1]-1),3))
	LSecond= zeros(((U[len(U)-1]-1),3))
	LRoot= zeros(((U[len(U)-1]-1),3))
	Head= zeros(((U[len(U)-1]-1),3))
	Tail= zeros(((U[len(U)-1]-1),3))




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
	#Output[:,1]=(degrees(BodyAngleYZ[:,0]))






##########################################################################################################




#plot global XY

	clf()
	scatter(-LSHOULDER[:,0],-LSHOULDER[:,1],c='y')
	scatter(-LWRIST[:,0],-LWRIST[:,1],c='r')
	scatter(-LWING[:,0],-LWING[:,1],c='b')
	scatter(-LSECOND[:,0],-LSECOND[:,1],c='g')
	scatter(-LROOT[:,0],-LROOT[:,1],c='c')
	scatter(-HEAD[:,0],-HEAD[:,1],c='m')
	scatter(-TAIL[:,0],-TAIL[:,1],c='#6600CC')
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('true_global_XY_'+file[:-4]+'.svg')

###########################################################

# plot all points 


	clf()
	scatter(LShoulder[:,0],LShoulder[:,2],c='y')
	scatter(LWrist[:,0],LWrist[:,2],c='r')
	scatter(LWing[:,0],LWing[:,2],c='b')
	scatter(LSecond[:,0],LSecond[:,2],c='g')
	scatter(LRoot[:,0],LRoot[:,2],c='c')
	scatter(Head[:,0],Head[:,2],c='m')
	scatter(Tail[:,0],Tail[:,2],c='#6600CC')	
	axis((20,-60,-40,40))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('XZ_global_'+file[:-4]+'.svg')


	clf()
	scatter(LShoulder[:,1],LShoulder[:,2],c='y')
	scatter(LWrist[:,1],LWrist[:,2],c='r')
	scatter(LWing[:,1],LWing[:,2],c='b')
	scatter(LSecond[:,1],LSecond[:,2],c='g')
	scatter(LRoot[:,1],LRoot[:,2],c='c')
	scatter(Head[:,1],Head[:,2],c='m')
	scatter(Tail[:,1],Tail[:,2],c='#6600CC')
	axis((75,-5,-40,40))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('YZ_global_'+file[:-4]+'.svg')

	clf()
	scatter(LShoulder[:,0],LShoulder[:,1],c='y')
	scatter(LWrist[:,0],LWrist[:,1],c='r')
	scatter(LWing[:,0],LWing[:,1],c='b')
	scatter(LSecond[:,0],LSecond[:,1],c='g')
	scatter(LRoot[:,0],LRoot[:,1],c='c')
	scatter(Head[:,0],Head[:,1],c='m')
	scatter(Tail[:,0],Tail[:,1],c='#6600CC')
#	plot(x,y)
	
	axis((20,-60,75,-5))
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('XY_global_'+file[:-4]+'.svg')


#	Write Transformed Coordinates

	Transformed=hstack((LShoulder, LWrist, LWing, LSecond, LRoot, Head, Tail))

	Writer = csv.writer(open("trans_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['shoulder_x','shoulder_y','shoulder_z','wrist_x','wrist_y','wrist_z','tip_x','tip_y','tip_z','secondary_x','secondary_y','secondary_z','root_x','root_y','root_z','head_x','head_y','head_z','tail_x','tail_y','tail_z'])
	for N in range(0,U[len(U)-1]-1):
		Writer.writerow(Transformed[N])





##########################################################################################################





## Calculate Angles relative to all strokeplanes

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
	

#	wing_angle_of_attack at mid stroke
			
	
			z=(R+S)/2
			angle_of_attack=degrees(atan((LWrist[z,2]-LSecond[z,2])/(LWrist[z,0]-LSecond[z,0])))



#	Write to output arrays
			Output1[:,0]=(degrees(StrokePlaneAngle))
			Output1[:,1]=(degrees(Position_Ground))
			Output1[:,2]=(degrees(WingAngle_Ground))
			Output1[:,3]=(degrees(Position))
			Output1[:,4]=(degrees(WingAngle))
			Output1[:,5]=(Wingtip_Dist_Trav)
			Output1[:,6]=(angle_of_attack)

			

# Plot per wingbeat XZ graphs 
			x0=[average(Head[R:S,0]),average(Tail[R:S,0])]
			y0=[average(Head[R:S,2]),average(Tail[R:S,2])]	

			#figure(1)
			clf()
			plot(x,y, c='g')
			plot(x0,y0, c='m')
			
			if T == 0:

				scatter(LWing[R:S,0],LWing[R:S,2],c='r')
				scatter(LShoulder[R:S,0],LShoulder[R:S,2],c='g')

			else:
				scatter(LWing[R:S,0],LWing[R:S,2],c='b')
				scatter(LShoulder[R:S,0],LShoulder[R:S,2],c='g')
			

			axis((20,-60,-40,40))		
			axes().set_aspect('equal', 'datalim')
			grid(True)
#			show()
			savefig("wingbeat_figures/"+Q+".svg")




##################################################################################################	


	
#Call programs
	#Create Summary variables

		Number=['']
	
		Body_Angle_DS=['Body_Angle']
		Body_Angle_YZ_DS=['Body_Angle_YZ']

		SA_Left_DS=['SA_Left_DS']
	
		L_Amp_SP_DS=['L_Amp_SP_DS']

		L_Wing_Elevation_Amp_DS=['L_Wing_Angle_Avg_DS']

		L_Wing_Angle_Avg_Ground_DS=['L_Wing_Angle_Avg_Ground_DS']

		L_Wingtip_Dist_Trav_DS=['L_Wingtip_Dist_Trav_DS']

		Body_X_Dist_DS=['Body_X_Dist_DS']
		Body_Y_Dist_DS=['Body_Y_Dist_DS']
		Body_Z_Dist_DS=['Body_Z_Dist_DS']

		Body_X_Vel_DS=['Body_X_Vel_DS']
		Body_Y_Vel_DS=['Body_Y_Vel_DS']
		Body_Z_Vel_DS=['Body_Z_Vel_DS']



	
		Body_Angle_US=['Body_Angle']
		Body_Angle_YZ_US=['Body_Angle_YZ']


		SA_Left_US=['SA_Left_US']

		L_Amp_SP_US=['L_Amp_SP_US']

		L_Wing_Elevation_Amp_US=['L_Wing_Angle_Avg_US']

		L_Wing_Angle_Avg_Ground_US=['L_Wing_Angle_Avg_Ground_US']
	
		L_Wingtip_Dist_Trav_US=['L_Wingtip_Dist_Trav_US']	

		Body_X_Dist_US=['Body_X_Dist_US']
		Body_Y_Dist_US=['Body_Y_Dist_US']
		Body_Z_Dist_US=['Body_Z_Dist_US']

		Body_X_Vel_US=['Body_X_Vel_US']
		Body_Y_Vel_US=['Body_Y_Vel_US']
		Body_Z_Vel_US=['Body_Z_Vel_US']	

#####################################################################################################################

# Calculations per upstroke/downstroke
		
	for n in range(len(U)-1):		
					

# left wing
		if n%2==0:
			Q = 'Down_'+str(n+1)+'_'+file[:-4]+'_Left'
			T = 0
		else:
			Q = 'Up_'+str(n+1)+'_'+file[:-4]+'_Left'
			T = 1
			

#		print Q

		StrokeAngle((U[n]-1),(U[n+1]-1))


		Output[(U[n]-1):(U[n+1]-1),1]=Output1[(U[n]-1):(U[n+1]-1),6]	#Angle of attack
		Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
		Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
		Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
		Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
		Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
		Output[(U[n]-1):(U[n+1]-1),7] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistanceTraveled
		
# Goose distance traveled


		BodyMotion=(HEAD[(U[n+1]-1),:]-HEAD[(U[n]-1),:])
		


	#Downstroke

		if n%2==0:
		
			Number.append(str((n/2)+1))
	
			Body_Angle_DS.append(average(Output[(U[n]-1):(U[n+1]-1),0]))
			Body_Angle_YZ_DS.append(average(Output[(U[n]-1):(U[n+1]-1),1]))



			SA_Left_DS.append(Output[U[n]-1,2])

			
			L_Wing_Angle_Avg_Ground_DS.append(average(Output[(U[n]-1):(U[n+1]-1),3]))

			L_Amp_SP_DS.append((max(Output[(U[n]-1):(U[n+1]-1),5]))-(min(Output[(U[n]-1):(U[n+1]-1),5])))

			L_Wing_Elevation_Amp_DS.append((max(Output[(U[n]-1):(U[n+1]-1),6]))-(min(Output[(U[n]-1):(U[n+1]-1),6])))

			L_Wingtip_Dist_Trav_DS.append(Output[U[n]-1,7])

			Body_X_Dist_DS.append(BodyMotion[0])
			Body_Y_Dist_DS.append(BodyMotion[1])
			Body_Z_Dist_DS.append(BodyMotion[2])
	

			
	#Upstroke
	
		else:	

			Body_Angle_US.append(average(Output[(U[n]-1):(U[n+1]-1),0]))
			Body_Angle_YZ_US.append(average(Output[(U[n]-1):(U[n+1]-1),1]))

			SA_Left_US.append(Output[U[n]-1,2])
			
			L_Wing_Angle_Avg_Ground_US.append(average(Output[(U[n]-1):(U[n+1]-1),3]))
			
			L_Amp_SP_US.append((max(Output[(U[n]-1):(U[n+1]-1),5]))-(min(Output[(U[n]-1):(U[n+1]-1),5])))

			L_Wing_Elevation_Amp_US.append((max(Output[(U[n]-1):(U[n+1]-1),6]))-(min(Output[(U[n]-1):(U[n+1]-1),6])))

			L_Wingtip_Dist_Trav_US.append(Output[U[n]-1,7])

			Body_X_Dist_US.append(BodyMotion[0])
			Body_Y_Dist_US.append(BodyMotion[1])
			Body_Z_Dist_US.append(BodyMotion[2])



############################################################################################################################	

	Writer = csv.writer(open("Angles_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['Body_Angle_lateral','Angle_of_attack_MidStroke','Stroke_Plane_Angle', 'Position_Angle_Ground','Elevation_Angle_Ground','Position_Angle_Stroke_Plane','Elevation_Angle_Stroke_Plane','Wingtip_Distance_Traveled(mm)'])
	for N in range(0,U[len(U)-1]-1):
		Writer.writerow(Output[N])

# store output in array

	# Change to convert wingtip velocity from m/frame to whatever you want (1250 = [125fps*10 upsampled frames])
	FrameMult=1250

	#############

	
	Output2 = zeros((len(Body_Angle_DS)-1,32))
	
	Output2[:,0] = Number[1:]
	Output2[:,1] = Time_DS[1:]
	Output2[:,2] = Body_Angle_DS[1:]
	Output2[:,3] = Body_Angle_YZ_DS[1:]
	Output2[:,4] = SA_Left_DS[1:]
	Output2[:,5] = L_Wing_Angle_Avg_Ground_DS[1:]
	Output2[:,6] = L_Amp_SP_DS[1:]
	Output2[:,7] = L_Wing_Elevation_Amp_DS[1:]

	Output2[:,8] = L_Wingtip_Dist_Trav_DS[1:]
	Output2[:,9] = (FrameMult*Output2[:,8]/Output2[:,1])

	Output2[:,10] = Body_X_Dist_DS[1:]
	Output2[:,11] = Body_Y_Dist_DS[1:]
	Output2[:,12] = Body_Z_Dist_DS[1:]

	Output2[:,13] = (FrameMult*Output2[:,10]/Output2[:,1])
	Output2[:,14] = (FrameMult*Output2[:,11]/Output2[:,1])
	Output2[:,15] = (FrameMult*Output2[:,12]/Output2[:,1])


	Output2[:,16] = Number[1:]
	Output2[:,17] = Time_US[1:]
	Output2[:,18] = Body_Angle_US[1:]
	Output2[:,19] = Body_Angle_YZ_US[1:]
	Output2[:,20] = SA_Left_US[1:]
	Output2[:,21] = L_Wing_Angle_Avg_Ground_US[1:]
	Output2[:,22] = L_Amp_SP_US[1:]
	Output2[:,23] = L_Wing_Elevation_Amp_US[1:]
	Output2[:,24] = L_Wingtip_Dist_Trav_US[1:]
	Output2[:,25] = (FrameMult*Output2[:,24]/Output2[:,17])

	Output2[:,26] = Body_X_Dist_US[1:]
	Output2[:,27] = Body_Y_Dist_US[1:]
	Output2[:,28] = Body_Z_Dist_US[1:]

	Output2[:,29] = (FrameMult*Output2[:,26]/Output2[:,17])
	Output2[:,30] = (FrameMult*Output2[:,27]/Output2[:,17])
	Output2[:,31] = (FrameMult*Output2[:,28]/Output2[:,17])


#write to file



	Writer = csv.writer(open("Angles_Summary_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Wingbeat#","Wingbeat_Length_DS (upsampled frames)", "Body_Angle_Lateral_DS","Angle_of_attack_DS","L_Stroke_Plane_Angle_DS","L_Avg_Position_Angle_Ground_DS", "L_Amplitude_Stroke_Plane_DS","L_Wing_Elevation_Amplitude_Stroke_Plane_DS","L_Wingtip_Dist_Traveled_DS(cm)","L_Wingtip_Velocity_DS(cm/sec)","Body_Dist_X_DS(cm)","Body_Dist_Y_DS(cm)","Body_Dist_Z_DS(cm)","Body_Vel_X_DS(cm/s)","Body_Vel_Y_DS(cm/s)","Body_Vel_Z_DS(cm/s)","Wingbeat#","Wingbeat_Length_US (upsampled frames)", "Body_Angle_Lateral_US","Angle_of_attack_US","L_Stroke_Plane_Angle_US","L_Avg_Position_Angle_Ground_US", "L_Amplitude_Stroke_Plane_US","L_Wing_Elevation_Amplitude_Stroke_Plane_US","L_Wingtip_Dist_Traveled_US (cm)","L_Wingtip_Velocity_US(cm)","Body_Dist_X_US(cm)","Body_Dist_Y_US(cm)","Body_Dist_Z_US(cm/s)","Body_Vel_X_US(cm/s)","Body_Vel_Y_US(cm/s)","Body_Vel_Z_US(cm/s)"])

	for N in range(len(Body_Angle_DS)-1):
		Writer.writerow(Output2[N])



###################################################################################

	
# Graph wingbeat timeseries 


	clf()
	plot(Output2[:,0],Output2[:,2],'bo')
	plot(Output2[:,0]+.5,Output2[:,18],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,20)
	savefig("angle_figures/1_Body_Angle_Lateral_"+file[:-4]+".svg")

	clf()
	plot(Output2[:,0],Output2[:,3],'bo')
	plot(Output2[:,0]+.5,Output2[:,19],'co')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,20)
	savefig("angle_figures/2_Angle_Attack_MDS_"+file[:-4]+".svg")

	clf()
	subplot(111)
	plot(Output2[:,0],Output2[:,4],'ro')
	plot(Output2[:,0]+.5,Output2[:,20],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,90)

	savefig("angle_figures/3_Stroke_Angle_"+file[:-4]+".svg")



	clf()
	subplot(111)
	plot(Output2[:,0],Output2[:,5],'ro')
	plot(Output2[:,0]+.5,Output2[:,21],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(60,120)

	savefig("angle_figures/4_Avg_Position_Angle_Ground_"+file[:-4]+".svg")


	clf()
	subplot(111)
	plot(Output2[:,0],Output2[:,6],'ro')
	plot(Output2[:,0]+.5,Output2[:,22],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,180)

	savefig("angle_figures/5_Amplitude_SP_"+file[:-4]+".svg")



	clf()
	subplot(111)
	plot(Output2[:,0],Output2[:,7],'ro')
	plot(Output2[:,0]+.5,Output2[:,23],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-25,25)

	savefig("angle_figures/6_Elevation_Amplitude_SP_"+file[:-4]+".svg")




	clf()
	subplot(111)
	plot(Output2[:,0],Output2[:,9],'ro')
	plot(Output2[:,0]+.5,Output2[:,25],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(0,1000)

	savefig("angle_figures/7_Wingtip_Velocity_"+file[:-4]+".svg")


	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,10],'ro')
	plot(Output2[:,0]+.5,Output2[:,26],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-5,5)

	subplot(312)
	plot(Output2[:,0],Output2[:,11],'ro')
	plot(Output2[:,0]+.5,Output2[:,27],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-5,5)

	subplot(313)
	plot(Output2[:,0],Output2[:,12],'ro')
	plot(Output2[:,0]+.5,Output2[:,28],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-5,5)

	savefig("angle_figures/8_Body_Movement_"+file[:-4]+".svg")


	clf()
	subplot(311)
	plot(Output2[:,0],Output2[:,13],'ro')
	plot(Output2[:,0]+.5,Output2[:,29],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-50,50)

	subplot(312)
	plot(Output2[:,0],Output2[:,14],'ro')
	plot(Output2[:,0]+.5,Output2[:,30],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-50,50)

	subplot(313)
	plot(Output2[:,0],Output2[:,15],'ro')
	plot(Output2[:,0]+.5,Output2[:,31],'mo')
	grid(True)
	xlim(0.5,len(Body_Angle_DS))
	ylim(-50,50)

	savefig("angle_figures/9_Body_Velocity_"+file[:-4]+".svg")


	

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
	ax= zeros((100,((len(U)-1)/2)+3))
	at= zeros((100,((len(U)-1)/2)+3))
	au= zeros((100,((len(U)-1)/2)+3))


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
	bs= zeros((100,((len(U)-1)/2)+3))
	bt= zeros((100,((len(U)-1)/2)+3))
	bu= zeros((100,((len(U)-1)/2)+3))

# Downstroke


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),0,aa)
	LShoulder_Avg_DS_X=aa


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),1,ab)
	LShoulder_Avg_DS_Y=ab


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),2,ac)
	LShoulder_Avg_DS_Z=ac





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),3,ad)
	LWrist_Avg_DS_X=ad

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),4,ae)
	LWrist_Avg_DS_Y=ae

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),5,af)
	LWrist_Avg_DS_Z=af





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),6,ag)
	LWing_Avg_DS_X=ag

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),7,ah)
	LWing_Avg_DS_Y=ah

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),8,ai)
	LWing_Avg_DS_Z=ai





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),9,aj)
	LSecond_Avg_DS_X=aj

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),10,ak)
	LSecond_Avg_DS_Y=ak

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),11,al)
	LSecond_Avg_DS_Z=al




	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),12,am)
	LRoot_Avg_DS_X=am

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),13,an)
	LRoot_Avg_DS_Y=an

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),14,ao)
	LRoot_Avg_DS_Z=ao





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),15,ap)
	Head_Avg_DS_X=ap

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),16,aq)
	Head_Avg_DS_Y=aq

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),17,ar)
	Head_Avg_DS_Z=ar





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),18,ax)
	Tail_Avg_DS_X=ax

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),19,at)
	Tail_Avg_DS_Y=at

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n]-1),(U[n+1]-1),20,au)
	Tail_Avg_DS_Z=au
	


	for n in range (0,100):
		LShoulder_Avg_DS_X[n,1]=average(LShoulder_Avg_DS_X[n,3:])
		LShoulder_Avg_DS_Y[n,1]=average(LShoulder_Avg_DS_Y[n,3:])
		LShoulder_Avg_DS_Z[n,1]=average(LShoulder_Avg_DS_Z[n,3:])

		LWrist_Avg_DS_X[n,1]=average(LWrist_Avg_DS_X[n,3:])
		LWrist_Avg_DS_Y[n,1]=average(LWrist_Avg_DS_Y[n,3:])
		LWrist_Avg_DS_Z[n,1]=average(LWrist_Avg_DS_Z[n,3:])

		LWing_Avg_DS_X[n,1]=average(LWing_Avg_DS_X[n,3:])
		LWing_Avg_DS_Y[n,1]=average(LWing_Avg_DS_Y[n,3:])
		LWing_Avg_DS_Z[n,1]=average(LWing_Avg_DS_Z[n,3:])

		LSecond_Avg_DS_X[n,1]=average(LSecond_Avg_DS_X[n,3:])
		LSecond_Avg_DS_Y[n,1]=average(LSecond_Avg_DS_Y[n,3:])
		LSecond_Avg_DS_Z[n,1]=average(LSecond_Avg_DS_Z[n,3:])

		LRoot_Avg_DS_X[n,1]=average(LRoot_Avg_DS_X[n,3:])
		LRoot_Avg_DS_Y[n,1]=average(LRoot_Avg_DS_Y[n,3:])
		LRoot_Avg_DS_Z[n,1]=average(LRoot_Avg_DS_Z[n,3:])

		Head_Avg_DS_X[n,1]=average(Head_Avg_DS_X[n,3:])
		Head_Avg_DS_Y[n,1]=average(Head_Avg_DS_Y[n,3:])
		Head_Avg_DS_Z[n,1]=average(Head_Avg_DS_Z[n,3:])

		Tail_Avg_DS_X[n,1]=average(Tail_Avg_DS_X[n,3:])
		Tail_Avg_DS_Y[n,1]=average(Tail_Avg_DS_Y[n,3:])
		Tail_Avg_DS_Z[n,1]=average(Tail_Avg_DS_Z[n,3:])




		#StErr
		LShoulder_Avg_DS_X[n,2]=(std(LShoulder_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_DS_Y[n,2]=(std(LShoulder_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_DS_Z[n,2]=(std(LShoulder_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LWrist_Avg_DS_X[n,2]=(std(LWrist_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWrist_Avg_DS_Y[n,2]=(std(LWrist_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWrist_Avg_DS_Z[n,2]=(std(LWrist_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LWing_Avg_DS_X[n,2]=(std(LWing_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWing_Avg_DS_Y[n,2]=(std(LWing_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWing_Avg_DS_Z[n,2]=(std(LWing_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LSecond_Avg_DS_X[n,2]=(std(LSecond_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LSecond_Avg_DS_Y[n,2]=(std(LSecond_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LSecond_Avg_DS_Z[n,2]=(std(LSecond_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LRoot_Avg_DS_X[n,2]=(std(LRoot_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LRoot_Avg_DS_Y[n,2]=(std(LRoot_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LRoot_Avg_DS_Z[n,2]=(std(LRoot_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		Head_Avg_DS_X[n,2]=(std(Head_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Head_Avg_DS_Y[n,2]=(std(Head_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Head_Avg_DS_Z[n,2]=(std(Head_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		Tail_Avg_DS_X[n,2]=(std(Tail_Avg_DS_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Tail_Avg_DS_Y[n,2]=(std(Tail_Avg_DS_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Tail_Avg_DS_Z[n,2]=(std(Tail_Avg_DS_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

#Upstroke


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),0,ba)	
	LShoulder_Avg_US_X=ba


	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),1,bb)
	LShoulder_Avg_US_Y=bb

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),2,bc)
	LShoulder_Avg_US_Z=bc





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),3,bd)
	LWrist_Avg_US_X=bd

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),4,be)
	LWrist_Avg_US_Y=be

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),5,bf)
	LWrist_Avg_US_Z=bf





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),6,bg)
	LWing_Avg_US_X=bg

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),7,bh)
	LWing_Avg_US_Y=bh

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),8,bi)
	LWing_Avg_US_Z=bi





	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),9,bj)
	LSecond_Avg_US_X=bj

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),10,bk)
	LSecond_Avg_US_Y=bk

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),11,bl)
	LSecond_Avg_US_Z=bl




	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),12,bm)
	LRoot_Avg_US_X=bm

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),13,bn)
	LRoot_Avg_US_Y=bn

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),14,bo)
	LRoot_Avg_US_Z=bo




	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),15,bp)
	Head_Avg_US_X=bp

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),16,bq)
	Head_Avg_US_Y=bq

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),17,br)
	Head_Avg_US_Z=br



	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),18,bs)
	Tail_Avg_US_X=bs

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),19,bt)
	Tail_Avg_US_Y=bt

	for n in range((len(U)-1)/2):
		n=n*2
		WingbeatAverage((U[n+1]-1),(U[n+2]-1),20,bu)
	Tail_Avg_US_Z=bu







	for n in range (0,100):
		LShoulder_Avg_US_X[n,1]=average(LShoulder_Avg_US_X[n,3:])
		LShoulder_Avg_US_Y[n,1]=average(LShoulder_Avg_US_Y[n,3:])
		LShoulder_Avg_US_Z[n,1]=average(LShoulder_Avg_US_Z[n,3:])

		LWrist_Avg_US_X[n,1]=average(LWrist_Avg_US_X[n,3:])
		LWrist_Avg_US_Y[n,1]=average(LWrist_Avg_US_Y[n,3:])
		LWrist_Avg_US_Z[n,1]=average(LWrist_Avg_US_Z[n,3:])

		LWing_Avg_US_X[n,1]=average(LWing_Avg_US_X[n,3:])
		LWing_Avg_US_Y[n,1]=average(LWing_Avg_US_Y[n,3:])
		LWing_Avg_US_Z[n,1]=average(LWing_Avg_US_Z[n,3:])

		LSecond_Avg_US_X[n,1]=average(LSecond_Avg_US_X[n,3:])
		LSecond_Avg_US_Y[n,1]=average(LSecond_Avg_US_Y[n,3:])
		LSecond_Avg_US_Z[n,1]=average(LSecond_Avg_US_Z[n,3:])

		LRoot_Avg_US_X[n,1]=average(LRoot_Avg_US_X[n,3:])
		LRoot_Avg_US_Y[n,1]=average(LRoot_Avg_US_Y[n,3:])
		LRoot_Avg_US_Z[n,1]=average(LRoot_Avg_US_Z[n,3:])

		Head_Avg_US_X[n,1]=average(Head_Avg_US_X[n,3:])
		Head_Avg_US_Y[n,1]=average(Head_Avg_US_Y[n,3:])
		Head_Avg_US_Z[n,1]=average(Head_Avg_US_Z[n,3:])

		Tail_Avg_US_X[n,1]=average(Tail_Avg_US_X[n,3:])
		Tail_Avg_US_Y[n,1]=average(Tail_Avg_US_Y[n,3:])
		Tail_Avg_US_Z[n,1]=average(Tail_Avg_US_Z[n,3:])



##########

		LShoulder_Avg_US_X[n,2]=(std(LShoulder_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_US_Y[n,2]=(std(LShoulder_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LShoulder_Avg_US_Z[n,2]=(std(LShoulder_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LWrist_Avg_US_X[n,2]=(std(LWrist_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWrist_Avg_US_Y[n,2]=(std(LWrist_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWrist_Avg_US_Z[n,2]=(std(LWrist_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LWing_Avg_US_X[n,2]=(std(LWing_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWing_Avg_US_Y[n,2]=(std(LWing_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LWing_Avg_US_Z[n,2]=(std(LWing_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LSecond_Avg_US_X[n,2]=(std(LSecond_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LSecond_Avg_US_Y[n,2]=(std(LSecond_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LSecond_Avg_US_Z[n,2]=(std(LSecond_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		LRoot_Avg_US_X[n,2]=(std(LRoot_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LRoot_Avg_US_Y[n,2]=(std(LRoot_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		LRoot_Avg_US_Z[n,2]=(std(LRoot_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		Head_Avg_US_X[n,2]=(std(Head_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Head_Avg_US_Y[n,2]=(std(Head_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Head_Avg_US_Z[n,2]=(std(Head_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		Tail_Avg_US_X[n,2]=(std(Tail_Avg_US_X[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Tail_Avg_US_Y[n,2]=(std(Tail_Avg_US_Y[n,3:],ddof=1))/(sqrt((len(U)-1)/2))
		Tail_Avg_US_Z[n,2]=(std(Tail_Avg_US_Z[n,3:],ddof=1))/(sqrt((len(U)-1)/2))

		
################


	AvgWingbeat = column_stack((LShoulder_Avg_DS_X[:,1], LShoulder_Avg_DS_Y[:,1], LShoulder_Avg_DS_Z[:,1], LWrist_Avg_DS_X[:,1], LWrist_Avg_DS_Y[:,1], LWrist_Avg_DS_Z[:,1],LWing_Avg_DS_X[:,1],LWing_Avg_DS_Y[:,1],LWing_Avg_DS_Z[:,1], LSecond_Avg_DS_X[:,1], LSecond_Avg_DS_Y[:,1], LSecond_Avg_DS_Z[:,1],LRoot_Avg_DS_X[:,1],LRoot_Avg_DS_Y[:,1],LRoot_Avg_DS_Z[:,1], Head_Avg_DS_X[:,1], Head_Avg_DS_Y[:,1], Head_Avg_DS_Z[:,1], Tail_Avg_DS_X[:,1], Tail_Avg_DS_Y[:,1], Tail_Avg_DS_Z[:,1],LShoulder_Avg_US_X[:,1], LShoulder_Avg_US_Y[:,1], LShoulder_Avg_US_Z[:,1], LWrist_Avg_US_X[:,1], LWrist_Avg_US_Y[:,1], LWrist_Avg_US_Z[:,1],LWing_Avg_US_X[:,1],LWing_Avg_US_Y[:,1],LWing_Avg_US_Z[:,1], LSecond_Avg_US_X[:,1], LSecond_Avg_US_Y[:,1], LSecond_Avg_US_Z[:,1],LRoot_Avg_US_X[:,1],LRoot_Avg_US_Y[:,1],LRoot_Avg_US_Z[:,1], Head_Avg_US_X[:,1], Head_Avg_US_Y[:,1], Head_Avg_US_Z[:,1], Tail_Avg_US_X[:,1], Tail_Avg_US_Y[:,1], Tail_Avg_US_Z[:,1]))

	AvgWingbeatStEr = column_stack((LShoulder_Avg_DS_X[:,2], LShoulder_Avg_DS_Y[:,2], LShoulder_Avg_DS_Z[:,2], LWrist_Avg_DS_X[:,2], LWrist_Avg_DS_Y[:,2], LWrist_Avg_DS_Z[:,2],LWing_Avg_DS_X[:,2],LWing_Avg_DS_Y[:,2],LWing_Avg_DS_Z[:,2], LSecond_Avg_DS_X[:,2], LSecond_Avg_DS_Y[:,2], LSecond_Avg_DS_Z[:,2],LRoot_Avg_DS_X[:,2],LRoot_Avg_DS_Y[:,2],LRoot_Avg_DS_Z[:,2], Head_Avg_DS_X[:,2], Head_Avg_DS_Y[:,2], Head_Avg_DS_Z[:,2], Tail_Avg_DS_X[:,2], Tail_Avg_DS_Y[:,2], Tail_Avg_DS_Z[:,2],LShoulder_Avg_US_X[:,2], LShoulder_Avg_US_Y[:,2], LShoulder_Avg_US_Z[:,2], LWrist_Avg_US_X[:,2], LWrist_Avg_US_Y[:,2], LWrist_Avg_US_Z[:,2],LWing_Avg_US_X[:,2],LWing_Avg_US_Y[:,2],LWing_Avg_US_Z[:,2], LSecond_Avg_US_X[:,2], LSecond_Avg_US_Y[:,2], LSecond_Avg_US_Z[:,2],LRoot_Avg_US_X[:,2],LRoot_Avg_US_Y[:,2],LRoot_Avg_US_Z[:,2], Head_Avg_US_X[:,2], Head_Avg_US_Y[:,2], Head_Avg_US_Z[:,2], Tail_Avg_US_X[:,2], Tail_Avg_US_Y[:,2], Tail_Avg_US_Z[:,2]))

	Writer = csv.writer(open("average_graphs/WingbeatAverage_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['LShoulder_DS_X','LShoulder_DS_Y','LShoulder_DS_Z','LWrist_DS_X','LWrist_DS_Y','LWrist_DS_Z','LWing_DS_X','LWing_DS_Y','LWing_DS_Z','LSecond_DS_X', 'LSecond_DS_Y','LSecond_DS_Z','LRoot_DS_X','LRoot_DS_Y','LRoot_DS_Z','Head_DS_X','Head_DS_Y','Head_DS_Z','Tail_DS_X','Tail_DS_Y','Tail_DS_Z','LShoulder_US_X','LShoulder_US_Y','LShoulder_US_Z','LWrist_US_X','LWrist_US_Y','LWrist_US_Z','LWing_US_X','LWing_US_Y','LWing_US_Z','LSecond_US_X', 'LSecond_US_Y','LSecond_US_Z','LRoot_US_X','LRoot_US_Y','LRoot_US_Z','Head_US_X','Head_US_Y','Head_US_Z','Tail_US_X','Tail_US_Y','Tail_US_Z'])
	for N in range(0,100):
		Writer.writerow(AvgWingbeat[N])

	Writer = csv.writer(open("average_graphs/WingbeatAvgStErr_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(['LShoulder_DS_X','LShoulder_DS_Y','LShoulder_DS_Z','LWrist_DS_X','LWrist_DS_Y','LWrist_DS_Z','LWing_DS_X','LWing_DS_Y','LWing_DS_Z','LSecond_DS_X', 'LSecond_DS_Y','LSecond_DS_Z','LRoot_DS_X','LRoot_DS_Y','LRoot_DS_Z','Head_DS_X','Head_DS_Y','Head_DS_Z','Tail_DS_X','Tail_DS_Y','Tail_DS_Z','LShoulder_US_X','LShoulder_US_Y','LShoulder_US_Z','LWrist_US_X','LWrist_US_Y','LWrist_US_Z','LWing_US_X','LWing_US_Y','LWing_US_Z','LSecond_US_X', 'LSecond_US_Y','LSecond_US_Z','LRoot_US_X','LRoot_US_Y','LRoot_US_Z','Head_US_X','Head_US_Y','Head_US_Z','Tail_US_X','Tail_US_Y','Tail_US_Z'])
	for N in range(0,100):
		Writer.writerow(AvgWingbeatStEr[N])


	
# plot all points 


	clf()
	plot(LWing_Avg_DS_X[:,1],LWing_Avg_DS_Z[:,1],c='b')
	plot(LWing_Avg_US_X[:,1],LWing_Avg_US_Z[:,1],c='b')

	plot(LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Z[:,1],c='y')
	plot(LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Z[:,1],c='y')

	plot(LWrist_Avg_DS_X[:,1],LWrist_Avg_DS_Z[:,1],c='r')
	plot(LWrist_Avg_US_X[:,1],LWrist_Avg_US_Z[:,1],c='r')

	plot(LSecond_Avg_DS_X[:,1],LSecond_Avg_DS_Z[:,1],c='g')
	plot(LSecond_Avg_US_X[:,1],LSecond_Avg_US_Z[:,1],c='g')

	plot(LRoot_Avg_DS_X[:,1],LRoot_Avg_DS_Z[:,1],c='c')
	plot(LRoot_Avg_US_X[:,1],LRoot_Avg_US_Z[:,1],c='c')

	scatter(Head_Avg_DS_X[:,1],Head_Avg_DS_Z[:,1],c='m')
	scatter(Head_Avg_US_X[:,1],Head_Avg_US_Z[:,1],c='m')

	plot(Tail_Avg_DS_X[:,1],Tail_Avg_DS_Z[:,1],c='#6600CC')
	plot(Tail_Avg_US_X[:,1],Tail_Avg_US_Z[:,1],c='#6600CC')	

	axis((20,-60,-40,40))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('average_graphs/XZ_avg_'+file[:-4]+'.svg')


	clf()
	plot(LWing_Avg_DS_Y[:,1],LWing_Avg_DS_Z[:,1],c='b')
	plot(LWing_Avg_US_Y[:,1],LWing_Avg_US_Z[:,1],c='b')

	plot(LShoulder_Avg_DS_Y[:,1],LShoulder_Avg_DS_Z[:,1],c='y')
	plot(LShoulder_Avg_US_Y[:,1],LShoulder_Avg_US_Z[:,1],c='y')

	plot(LWrist_Avg_DS_Y[:,1],LWrist_Avg_DS_Z[:,1],c='r')
	plot(LWrist_Avg_US_Y[:,1],LWrist_Avg_US_Z[:,1],c='r')

	plot(LSecond_Avg_DS_Y[:,1],LSecond_Avg_DS_Z[:,1],c='g')
	plot(LSecond_Avg_US_Y[:,1],LSecond_Avg_US_Z[:,1],c='g')

	plot(LRoot_Avg_DS_Y[:,1],LRoot_Avg_DS_Z[:,1],c='c')
	plot(LRoot_Avg_US_Y[:,1],LRoot_Avg_US_Z[:,1],c='c')

	scatter(Head_Avg_DS_Y[:,1],Head_Avg_DS_Z[:,1],c='m')
	scatter(Head_Avg_US_Y[:,1],Head_Avg_US_Z[:,1],c='m')

	plot(Tail_Avg_DS_Y[:,1],Tail_Avg_DS_Z[:,1],c='#6600CC')
	plot(Tail_Avg_US_Y[:,1],Tail_Avg_US_Z[:,1],c='#6600CC')

	axis((-5,75,-40,40))	
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('average_graphs/YZ_avg_'+file[:-4]+'.svg')





	clf()
	plot(LWing_Avg_DS_X[:,1],LWing_Avg_DS_Y[:,1],c='b')
	plot(LWing_Avg_US_X[:,1],LWing_Avg_US_Y[:,1],c='b')

	plot(LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Y[:,1],c='y')
	plot(LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Y[:,1],c='y')

	plot(LWrist_Avg_DS_X[:,1],LWrist_Avg_DS_Y[:,1],c='r')
	plot(LWrist_Avg_US_X[:,1],LWrist_Avg_US_Y[:,1],c='r')

	plot(LSecond_Avg_DS_X[:,1],LSecond_Avg_DS_Y[:,1],c='g')
	plot(LSecond_Avg_US_X[:,1],LSecond_Avg_US_Y[:,1],c='g')

	plot(LRoot_Avg_DS_X[:,1],LRoot_Avg_DS_Y[:,1],c='c')
	plot(LRoot_Avg_US_X[:,1],LRoot_Avg_US_Y[:,1],c='c')

	scatter(Head_Avg_DS_X[:,1],Head_Avg_DS_Y[:,1],c='m')
	scatter(Head_Avg_US_X[:,1],Head_Avg_US_Y[:,1],c='m')

	plot(Tail_Avg_DS_X[:,1],Tail_Avg_DS_Y[:,1],c='#6600CC')
	plot(Tail_Avg_US_X[:,1],Tail_Avg_US_Y[:,1],c='#6600CC')

	axis((20,-60,75,-5))
	axes().set_aspect('equal', 'datalim')
	grid(True)
#	show()	
	savefig('average_graphs/XY_avg_'+file[:-4]+'.svg')



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
#		Output[(U[n]-1):(U[n+1]-1),2]=Output1[(U[n]-1):(U[n+1]-1),0]    #StrokePlaneAngle
#		Output[(U[n]-1):(U[n+1]-1),3]=Output1[(U[n]-1):(U[n+1]-1),1]	#PositionGround
#		Output[(U[n]-1):(U[n+1]-1),4]=Output1[(U[n]-1):(U[n+1]-1),2]	#WingAngleGround
#		Output[(U[n]-1):(U[n+1]-1),5]=Output1[(U[n]-1):(U[n+1]-1),3]	#Position
#		Output[(U[n]-1):(U[n+1]-1),6]=Output1[(U[n]-1):(U[n+1]-1),4]	#WingAngle
#		Output[(U[n]-1):(U[n+1]-1),7] = Output1[(U[n]-1):(U[n+1]-1),5]	#WingtipDistanceTraveled

# Position and Deviation from Stroke Plane 
#Downstroke

	i= zeros((100,((len(U)-1)/2)+3))		
	j= zeros((100,((len(U)-1)/2)+3))	



	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),5,i)
	LPosition_SP_DS=i


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),6,j)
	LDeviation_SP_DS=j


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		

		LPosition_SP_DS[n,1]=average(LPosition_SP_DS[n,3:])
		LDeviation_SP_DS[n,1]=average(LDeviation_SP_DS[n,3:])
		LPosition_SP_DS[n,2]=std(LPosition_SP_DS[n,3:],ddof=1)
		LDeviation_SP_DS[n,2]=std(LDeviation_SP_DS[n,3:],ddof=1)

		


################################# --- same for upstroke



	r= zeros((100,((len(U)-1)/2)+3))		
	s= zeros((100,((len(U)-1)/2)+3))	




	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),5,r)
	LPosition_SP_US=r


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),6,s)
	LDeviation_SP_US=s


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		LPosition_SP_US[n,1]=average(LPosition_SP_US[n,3:])
		LDeviation_SP_US[n,1]=average(LDeviation_SP_US[n,3:])
		LPosition_SP_US[n,2]=std(LPosition_SP_US[n,3:],ddof=1)
		LDeviation_SP_US[n,2]=std(LDeviation_SP_US[n,3:],ddof=1)

# Consolidate


	LPosition_SP = vstack((LPosition_SP_DS,LPosition_SP_US))
	LDeviation_SP = vstack((LDeviation_SP_DS,LDeviation_SP_US))

	LPosition_SP[:,0] = arange(200)
	LDeviation_SP[:,0] = arange(200)



# 	graph		

	clf()
	scatter(LDeviation_SP[:,0],LDeviation_SP[:,1],c='r')
	axis((0,200,-45,45))

	savefig('wingbeat_timecourse/PosElev_SP/LElevation_SP_'+file[:-4])
#	show()

	clf()
	scatter(LPosition_SP[:,0],LPosition_SP[:,1],c='r')
	axis((0,200,-10,190))
	savefig('wingbeat_timecourse/PosElev_SP/LPosition_SP_'+file[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(LDeviation_SP[1,:])):	
		clf()
		scatter(LDeviation_SP[:,0],LDeviation_SP[:,n],c='r')
		axis((0,200,-45,45))
		savefig('wingbeat_timecourse/PosElev_SP/Graphs/LElevation_SP_'+str(n-2)+"_"+file[:-4])

		clf()
		scatter(LPosition_SP[:,0],LPosition_SP[:,n],c='r')
		axis((0,200,-10,190))
		savefig('wingbeat_timecourse/PosElev_SP/Graphs/LPosition_SP_'+str(n-2)+"_"+file[:-4])



#	Write Output


	header = ['Time','Average','StDev']
	for n in range(3,len(LDeviation_SP[1,:])):
		header.append(n-2)

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_SP/LPosition_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LPosition_SP[N])

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_SP/LElevation_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LDeviation_SP[N])




#######################
	#summary file

	LPosElev_SP_Summary=zeros((100,8))
	LPosElev_SP_Summary[:,0]=LDeviation_SP_DS[:,1]
	LPosElev_SP_Summary[:,1]=LDeviation_SP_DS[:,2]
	LPosElev_SP_Summary[:,2]=LDeviation_SP_US[:,1]
	LPosElev_SP_Summary[:,3]=LDeviation_SP_US[:,2]
	

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_SP/Summary_LPosElev_SP_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Left_Downstroke_Avg","Left_Downstroke_StErr","Left_Upstroke_Avg","Left_Upstroke_StErr"])
	for N in range(0,100):
		Writer.writerow(LPosElev_SP_Summary[N])
######################################################################################################################

# Position and Deviation from Horizontal

	i= zeros((100,((len(U)-1)/2)+3))		
	j= zeros((100,((len(U)-1)/2)+3))	


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),3,i)
	LPosition_GR_DS=i


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n]-1),(U[n+1]-1),4,j)
	LDeviation_GR_DS=j


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):
		
		LPosition_GR_DS[n,1]=average(LPosition_GR_DS[n,3:])
		LDeviation_GR_DS[n,1]=average(LDeviation_GR_DS[n,3:])
		LPosition_GR_DS[n,2]=std(LPosition_GR_DS[n,3:],ddof=1)
		LDeviation_GR_DS[n,2]=std(LDeviation_SP_DS[n,3:],ddof=1)


##################upstroke

	m= zeros((100,((len(U)-1)/2)+3))		
	o= zeros((100,((len(U)-1)/2)+3))


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),3,m)
	LPosition_GR_US=m


	for n in range((len(U)-1)/2):
		n=n*2
		PerWingbeat((U[n+1]-1),(U[n+2]-1),4,o)
	LDeviation_GR_US=o


#	Calculate Averages and StDevs and save as columns 2 and 3

	for n in range(0,100):

		LPosition_GR_US[n,1]=average(LPosition_GR_US[n,3:])
		LDeviation_GR_US[n,1]=average(LDeviation_GR_US[n,3:])
		LPosition_GR_US[n,2]=std(LPosition_GR_US[n,3:],ddof=1)
		LDeviation_GR_US[n,2]=std(LDeviation_GR_US[n,3:],ddof=1)

# Consolidate

	LPosition_GR = vstack((LPosition_GR_DS,LPosition_GR_US))
	LDeviation_GR = vstack((LDeviation_GR_DS,LDeviation_GR_US))

	LPosition_GR[:,0] = arange(200)
	LDeviation_GR[:,0] = arange(200)



# 	graph		

	clf()
	scatter(LDeviation_GR[:,0],LDeviation_GR[:,1],c='r')
	axis((0,200,-50,50))

	savefig('wingbeat_timecourse/PosElev_GR/LElevation_GR_'+file[:-4])
#	show()

	clf()
	scatter(LPosition_GR[:,0],LPosition_GR[:,1],c='r')
	axis((0,200,-10,190))
	savefig('wingbeat_timecourse/PosElev_GR/LPosition_GR_'+file[:-4])
#	show()


#	graph individual wingbeats

	for n in range(3,len(LDeviation_GR[1,:])):	
		clf()
		scatter(LDeviation_GR[:,0],LDeviation_GR[:,n],c='r')
		axis((0,200,-50,50))
		savefig('wingbeat_timecourse/PosElev_GR/Graphs/LElevation_GR_'+str(n-2)+"_"+file[:-4])

		clf()
		scatter(LPosition_GR[:,0],LPosition_GR[:,n],c='r')
		axis((0,200,-10,190))
		savefig('wingbeat_timecourse/PosElev_GR/Graphs/LPosition_GR_'+str(n-2)+"_"+file[:-4])



#	Write Output


	header = ['Time','Average','StDev']
	for n in range(3,len(LDeviation_GR[1,:])):
		header.append(n-2)

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_GR/LPosition_GR_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LPosition_GR[N])

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_GR/LElevation_GR_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(header)
	for N in range(0,200):
		Writer.writerow(LDeviation_GR[N])

################################
	LPosElev_GR_Summary=zeros((100,8))
	LPosElev_GR_Summary[:,0]=LDeviation_GR_DS[:,1]
	LPosElev_GR_Summary[:,1]=LDeviation_GR_DS[:,2]
	LPosElev_GR_Summary[:,2]=LDeviation_GR_US[:,1]
	LPosElev_GR_Summary[:,3]=LDeviation_GR_US[:,2]
	

	Writer = csv.writer(open("wingbeat_timecourse/PosElev_GR/Summary_LRPosElev_GR_"+file, 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	Writer.writerow(["Left_Downstroke_Avg","Left_Downstroke_StErr","Left_Upstroke_Avg","Left_Upstroke_StErr"])
	for N in range(0,100):
		Writer.writerow(LPosElev_GR_Summary[N])

################################ 3d plots:

	clf()
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	
	plot(TAIL[:,0],TAIL[:,1],TAIL[:,2],c='#6600CC')
	plot(LSECOND[:,0],LSECOND[:,1],LSECOND[:,2],c='g')
	plot(LROOT[:,0],LROOT[:,1],LROOT[:,2],c='c')
	plot(LWRIST[:,0],LWRIST[:,1],LWRIST[:,2],c='r')
	plot(LSHOULDER[:,0],LSHOULDER[:,1],LSHOULDER[:,2],c='y')
	plot(LWING[:,0],LWING[:,1],LWING[:,2],c='b')
	plot(HEAD[:,0],HEAD[:,1],HEAD[:,2],c='m')

	for n in range(len(U)-1):
		ax.scatter(LWING[U[n],0],LWING[U[n],1],LWING[U[n],2], c="r")

	show_aa=input("show angle of attack? (0=no,1=yes)")

	if show_aa==1:
	    for n in range(len(U)-1):
		ax.scatter(LWING[(U[n+1]+U[n])/2,0],LWING[(U[n+1]+U[n])/2,1],LWING[(U[n+1]+U[n])/2,2], c="g")		
		ax.scatter(LWRIST[(U[n+1]+U[n])/2,0],LWRIST[(U[n+1]+U[n])/2,1],LWRIST[(U[n+1]+U[n])/2,2], c="g")
		ax.scatter(LSECOND[(U[n+1]+U[n])/2,0],LSECOND[(U[n+1]+U[n])/2,1],LSECOND[(U[n+1]+U[n])/2,2], c="r")

		plot([LWRIST[(U[n+1]+U[n])/2,0],LSECOND[(U[n+1]+U[n])/2,0]],[LWRIST[(U[n+1]+U[n])/2,1],LSECOND[(U[n+1]+U[n])/2,1]],[LWRIST[(U[n+1]+U[n])/2,2],LSECOND[(U[n+1]+U[n])/2,2]], c="y")
	

	ax.set_aspect('equal','datalim')



	fig2 = plt.figure()
	ax = fig2.add_subplot(111,projection='3d')
	
	plot(LWing_Avg_DS_X[:,1],LWing_Avg_DS_Y[:,1],LWing_Avg_DS_Z[:,1],c='b')
	plot(LWing_Avg_US_X[:,1],LWing_Avg_US_Y[:,1],LWing_Avg_US_Z[:,1],c='b')

	plot(LShoulder_Avg_DS_X[:,1],LShoulder_Avg_DS_Y[:,1],LShoulder_Avg_DS_Z[:,1],c='y')
	plot(LShoulder_Avg_US_X[:,1],LShoulder_Avg_US_Y[:,1],LShoulder_Avg_US_Z[:,1],c='y')

	plot(LWrist_Avg_DS_X[:,1],LWrist_Avg_DS_Y[:,1],LWrist_Avg_DS_Z[:,1],c='r')
	plot(LWrist_Avg_US_X[:,1],LWrist_Avg_US_Y[:,1],LWrist_Avg_US_Z[:,1],c='r')

	plot(LSecond_Avg_DS_X[:,1],LSecond_Avg_DS_Y[:,1],LSecond_Avg_DS_Z[:,1],c='g')
	plot(LSecond_Avg_US_X[:,1],LSecond_Avg_US_Y[:,1],LSecond_Avg_US_Z[:,1],c='g')

	plot(LRoot_Avg_DS_X[:,1],LRoot_Avg_DS_Y[:,1],LRoot_Avg_DS_Z[:,1],c='c')
	plot(LRoot_Avg_US_X[:,1],LRoot_Avg_US_Y[:,1],LRoot_Avg_US_Z[:,1],c='c')

	ax.scatter(Head_Avg_DS_X[:,1],Head_Avg_DS_Y[:,1],Head_Avg_DS_Z[:,1],c='m')
	ax.scatter(Head_Avg_US_X[:,1],Head_Avg_US_Y[:,1],Head_Avg_DS_Z[:,1],c='m')

	plot(Tail_Avg_DS_X[:,1],Tail_Avg_DS_Y[:,1],Tail_Avg_DS_Z[:,1],c='#6600CC')
	plot(Tail_Avg_US_X[:,1],Tail_Avg_US_Y[:,1],Tail_Avg_US_Z[:,1],c='#6600CC')


	x=[average(vstack((Head_Avg_DS_X[:,1],Head_Avg_US_X[:,1]))),average(vstack((Tail_Avg_DS_X[:,1],Tail_Avg_US_X[:,1])))]
	y=[average(vstack((Head_Avg_DS_Y[:,1],Head_Avg_US_Y[:,1]))),average(vstack((Tail_Avg_DS_Y[:,1],Tail_Avg_US_Y[:,1])))]
	z=[average(vstack((Head_Avg_US_Y[:,1],Head_Avg_DS_Z[:,1]))),average(vstack((Tail_Avg_DS_Z[:,1],Tail_Avg_US_Z[:,1])))]	

	plot(x,y,z,c='m')

	ax.set_aspect('equal','datalim')


	show(fig)
	

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
